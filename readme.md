Fast Mac Screen Capture (Metal vs MSS)

High-performance macOS screen capture using a Mac Inbuilt ScreenCaptureKit Framework using swift,
compared against the Python library MSS.

This project demonstrates how a native Metal-based capture pipeline
scales significantly better than CPU-based capture approaches on Apple
Silicon.

  -------------------
  Why This Project?
  -------------------

Screen capture performance becomes a bottleneck in:

-   Real-time computer vision
-   Game automation

  ----------------------
  Installation & Setup
  ----------------------

1.  Clone Repository

git clone https://github.com/HummingNerd/fast-mac-capture.git
cd fast-mac-capture

2.  Compile Swift Backend

swiftc -O -emit-library -o libcapture.dylib capture.swift

This builds the optimized Metal dynamic library.

3.  Install as Editable Package to Call in Any Directory without going through the whole process for every new directory (Optional)

cd global_setup
pip install -e .

Now you can import:

from fast_mac_capture import MacScreenCapture

  ------------------------
  Performance Comparison
  ------------------------

Test Environment: - Apple Silicon (M1) - macOS - OpenCV display loop -
5-second averaged capture - Same resolution and region for both methods

Resolution MSS FPS Metal FPS Speedup

300x300 26 68 2.6x 1280x800 15 56 3.7x

Observations:

-   The performance gap increases with resolution.
-   MSS performance drops faster as pixel count increases.
-   The Metal backend scales more efficiently.
-   Metal maintains near real-time capture at native resolution.

  ---------------------------
  Why Metal Performs Better
  ---------------------------

MSS (CPU-Based): - Uses system APIs - Copies framebuffer data to CPU -
Python-level memory conversions - Higher per-frame overhead

Metal Backend: - GPU-backed pipeline - Reduced memory copy overhead -
Efficient pixel transfer - Better scaling at high resolution

  ----------------
  Why This Helps
  ----------------

On Apple Silicon:

-   2.5x–4x performance improvement
-   Better scaling with resolution
-   Lower CPU overhead
-   More suitable for realtime process relying on reading the screen
