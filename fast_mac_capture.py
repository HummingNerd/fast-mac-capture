import ctypes
import os
import numpy as np

# 1. Locate and load the compiled dynamic library
lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libcapture.dylib')
_lib = ctypes.CDLL(lib_path)

# 2. Define the C-function signatures so Python knows what data types to pass/expect
_lib.start_capture.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
_lib.start_capture.restype = ctypes.c_int

_lib.grab_frame.argtypes = [ctypes.POINTER(ctypes.c_uint8)]
_lib.grab_frame.restype = ctypes.c_int

_lib.stop_capture.argtypes = []
_lib.stop_capture.restype = None

# 3. Create a clean Python class to manage the capture lifecycle
class MacScreenCapture:
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.buffer_size = width * height * 4
        
        # Pre-allocate the memory buffer in Python to receive the C-data
        self.FrameBuffer = ctypes.c_uint8 * self.buffer_size
        self.frame_buffer = self.FrameBuffer()
        
        # Start the Swift ScreenCaptureKit stream
        success = _lib.start_capture(x, y, width, height)
        if not success:
            raise RuntimeError("Failed to initialize ScreenCaptureKit stream.")

    def grab(self):
        """Copies the latest frame into Python memory and returns a NumPy array."""
        success = _lib.grab_frame(self.frame_buffer)
        if not success:
            return None
            
        # Convert the raw byte buffer into a structured image array (BGRA format)
        return np.frombuffer(self.frame_buffer, dtype=np.uint8).reshape((self.height, self.width, 4))

    def stop(self):
        _lib.stop_capture()

    # Allow usage with the "with" statement for safe cleanup
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()