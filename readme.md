
```markdown
# Fast Mac Screen Capture (ScreenCaptureKit vs. MSS)

A high-performance macOS screen capture solution using the native Mac **ScreenCaptureKit** framework (via Swift), compared directly against the popular Python library **MSS**. 

This project demonstrates how a native, GPU-backed capture pipeline scales significantly better than traditional CPU-based capture approaches, especially on Apple Silicon.

---

## Why This Project?

Screen capture performance frequently becomes a severe computing bottleneck in demanding applications, such as:
* Real-time computer vision processing 
* Game automation and AI agents

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/HummingNerd/fast-mac-capture.git](https://github.com/HummingNerd/fast-mac-capture.git)
cd fast-mac-capture

```

### 2. Compile the Swift Backend

This compiles the optimized dynamic library to interface with macOS native APIs.

```bash
swiftc -O -emit-library -o libcapture.dylib capture.swift

```

### 3. Install Globally (Optional but Recommended)

To use this library from *any* directory on your system without duplicating the compiled files for every new project:

```bash
cd global_setup
pip install -e .

```

You can now import it into any Python script like a standard library:

```python
from fast_mac_capture import MacScreenCapture

```

---

## Performance Comparison

**Test Environment:**

* **Hardware:** Apple Silicon (M1)
* **OS:** macOS
* **Conditions:** OpenCV display loop, 5-second averaged capture, identical resolution and screen region for both methods.

| Resolution | MSS (CPU) FPS | Native (ScreenCaptureKit) FPS | Speedup |
| --- | --- | --- | --- |
| **300 x 300** | 26 | 68 | **2.6x** |
| **1280 x 800** | 15 | 56 | **3.7x** |

### Key Observations:

* The performance gap widens significantly as the capture resolution increases.
* MSS performance degrades rapidly as the total pixel count grows.
* The native backend scales much more efficiently, maintaining near real-time capture rates even at higher resolutions.

---

## Why the Native Framework Performs Better

### MSS (CPU-Based Pipeline):

* Relies on older system APIs.
* Forces massive framebuffer data to be copied to the CPU.
* Incurs high per-frame overhead due to Python-level memory conversions.

### Native Backend (ScreenCaptureKit / Metal):

* Utilizes a modern, GPU-backed pipeline.
* Drastically reduces memory copy overhead via shared buffers.
* Transfers pixels efficiently for vastly better scaling at high resolutions.

---

## The Bottom Line

By switching to this native implementation on Apple Silicon, you benefit from:

* **2.5x to 4x** overall performance improvement.
* Superior scaling with high-resolution captures.
* Significantly lower CPU overhead.
* A pipeline genuinely suited for real-time processes relying on reading the screen.
