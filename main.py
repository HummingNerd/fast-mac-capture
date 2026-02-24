import cv2
import time
import numpy as np
from mss import mss 
from fast_mac_capture import MacScreenCapture



X, Y = 0, 0
WIDTH, HEIGHT = 300, 300

screen = {"left" : X, "top": Y, "width" : WIDTH, "height" : HEIGHT}

def mss_script():


    with mss() as sct:
        last_time = time.time()
        start_time = last_time

        total_frames = 0
        frames = 0

        print("Capturing Using MSS")
        while True:
            img = np.array(sct.grab(screen))

            if img is not None:
                frames += 1
                total_frames += 1
                cv2.imshow("MSS", img)

            

            current_time = time.time()
            if current_time - last_time >= 1.0:
                print(f"FPS: {frames}")
                frames = 0
                last_time = current_time

            if cv2.waitKey(1) % 0xFF == ord('q'):
                break

    cv2.destroyAllWindows() 
    print(f"Average FPS : {total_frames/(time.time() - start_time)}")

def mac_capture_script():
    with MacScreenCapture(x=X, y=Y, width=WIDTH, height=HEIGHT) as sct:
        last_time = time.time()
        start_time = last_time
        
        total_frames = 0
        frames = 0
        
        print("Capturing Using Metal")
        while True:
            # Grab the frame natively as a numpy array
            frame = sct.grab()
            
            if frame is not None:
                frames += 1
                total_frames += 1
                cv2.imshow("Metal Capture", frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
            # Simple FPS counter
            current_time = time.time()
            if current_time - last_time >= 1.0:
                print(f"FPS: {frames}")
                frames = 0
                last_time = current_time

    cv2.destroyAllWindows()
    print(f"Average FPS : {total_frames/(time.time() - start_time)}")


if __name__ == "__main__":
    # Uncommemnt Accordingly 
    #mss_script()
    mac_capture_script()
    pass


# Resolution MSS Metal 
# 300x300 26 68 
# 1280x800 15 56 (My Native Screen Resolution I am Using)