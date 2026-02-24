import ctypes
import numpy as np
import os

class MacScreenCapture:
    def __init__(self, x=0, y=0, width=1080, height=720):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Pre-allocate the memory buffer
        self.frame_buffer = np.zeros((self.height, self.width, 4), dtype=np.uint8)

        # Dynamically find the .dylib relative to THIS file's location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        lib_path = os.path.join(current_dir, 'libcapture.dylib')

        if not os.path.exists(lib_path):
            raise FileNotFoundError(f"Could not find Swift library at {lib_path}")

        # Load the library
        self.lib = ctypes.CDLL(lib_path)

        # Define C-types
        self.lib.start_capture.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.lib.start_capture.restype = ctypes.c_int
        self.lib.grab_frame.argtypes = [ctypes.c_void_p]
        self.lib.grab_frame.restype = ctypes.c_int
        self.lib.stop_capture.argtypes = []
        self.lib.stop_capture.restype = None

        self.is_capturing = False

    def start(self):
        """Starts the ScreenCaptureKit stream."""
        if not self.lib.start_capture(self.x, self.y, self.width, self.height):
            raise RuntimeError("Failed to start capture. Ensure Screen Recording permissions are granted.")
        self.is_capturing = True

    def grab(self):
        """Grabs the latest frame into the numpy array and returns it."""
        if not self.is_capturing:
            raise RuntimeError("Capture stream is not running. Call start() first.")
            
        success = self.lib.grab_frame(self.frame_buffer.ctypes.data_as(ctypes.c_void_p))
        if success:
            return self.frame_buffer
        return None

    def stop(self):
        """Stops the capture stream."""
        if self.is_capturing:
            self.lib.stop_capture()
            self.is_capturing = False

    # Allow usage with the 'with' statement for automatic cleanup
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()