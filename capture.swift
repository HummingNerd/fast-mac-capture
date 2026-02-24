import Foundation
import ScreenCaptureKit
import CoreVideo
import CoreMedia

class FrameManager: NSObject, SCStreamOutput {
    static let shared = FrameManager()
    var stream: SCStream?
    var pixelBuffer: CVPixelBuffer?
    let lock = NSLock()

    func stream(_ stream: SCStream, didOutputSampleBuffer sampleBuffer: CMSampleBuffer, of type: SCStreamOutputType) {
        guard type == .screen else { return }
        guard let buffer = CMSampleBufferGetImageBuffer(sampleBuffer) else { return }

        // Keep only the absolute latest frame in memory
        lock.lock()
        self.pixelBuffer = buffer
        lock.unlock()
    }
}

@_cdecl("start_capture")
public func start_capture(x: Int, y: Int, width: Int, height: Int) -> Int {
    let semaphore = DispatchSemaphore(value: 0)
    var success = 0

    Task {
        do {
            // Fetch available displays (using modern API, falling back to current if needed)
            let content = try await SCShareableContent.excludingDesktopWindows(false, onScreenWindowsOnly: true)
            guard let display = content.displays.first else {
                semaphore.signal()
                return
            }

            let filter = SCContentFilter(display: display, excludingApplications: [], exceptingWindows: [])
            let config = SCStreamConfiguration()
            
            // Set capture region and framerate
            config.width = width
            config.height = height
            config.sourceRect = CGRect(x: CGFloat(x), y: CGFloat(y), width: CGFloat(width), height: CGFloat(height))
            config.minimumFrameInterval = CMTime(value: 1, timescale: 60)
            config.queueDepth = 3 // Keep queue shallow for real-time latency
            config.pixelFormat = kCVPixelFormatType_32BGRA

            let stream = SCStream(filter: filter, configuration: config, delegate: nil)
            
            // Run the stream output on a high-priority background queue
            let queue = DispatchQueue(label: "com.capture.video", qos: .userInteractive)
            try stream.addStreamOutput(FrameManager.shared, type: .screen, sampleHandlerQueue: queue)

            try await stream.startCapture()
            FrameManager.shared.stream = stream
            success = 1
        } catch {
            print("Failed to start capture: \(error)")
        }
        semaphore.signal()
    }

    // Block C-call until async setup finishes
    semaphore.wait()
    return success
}

@_cdecl("grab_frame")
public func grab_frame(destBuffer: UnsafeMutablePointer<UInt8>) -> Int {
    FrameManager.shared.lock.lock()
    defer { FrameManager.shared.lock.unlock() }

    guard let buffer = FrameManager.shared.pixelBuffer else { return 0 }

    CVPixelBufferLockBaseAddress(buffer, .readOnly)
    defer { CVPixelBufferUnlockBaseAddress(buffer, .readOnly) }

    guard let baseAddress = CVPixelBufferGetBaseAddress(buffer) else { return 0 }

    let width = CVPixelBufferGetWidth(buffer)
    let height = CVPixelBufferGetHeight(buffer)
    let bytesPerRow = CVPixelBufferGetBytesPerRow(buffer)

    // Fast memory copy directly into Python's buffer
    if bytesPerRow == width * 4 {
        memcpy(destBuffer, baseAddress, width * height * 4)
    } else {
        // Handle Apple Silicon memory padding if present
        for row in 0..<height {
            let srcRow = baseAddress.advanced(by: row * bytesPerRow)
            let dstRow = destBuffer.advanced(by: row * width * 4)
            memcpy(dstRow, srcRow, width * 4)
        }
    }
    return 1
}

@_cdecl("stop_capture")
public func stop_capture() {
    if let stream = FrameManager.shared.stream {
        Task {
            try? await stream.stopCapture()
        }
    }
}