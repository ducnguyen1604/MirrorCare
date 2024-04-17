import cv2
import threading

def open_camera(camera_index):
    # Create a VideoCapture object
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print(f"Cannot open camera {camera_index}")
        return

    print(f"Camera {camera_index} opened successfully.")
    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            # If frame is read correctly, ret is True
            if not ret:
                print(f"Can't receive frame from camera {camera_index}. Exiting...")
                break

            # Display the resulting frame
            cv2.imshow(f'Camera {camera_index}', frame)

            # Press 'q' on the keyboard to exit
            if cv2.waitKey(1) == ord('q'):
                break
    finally:
        # When everything is done, release the capture
        cap.release()
        cv2.destroyAllWindows()

def main():
    camera_index = 0
    threads = []

    # Try to open cameras sequentially until failure
    while True:
        cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap.release()
            break

        # If the camera is successfully opened, start a thread to manage its stream
        cap.release()
        thread = threading.Thread(target=open_camera, args=(camera_index,))
        thread.start()
        threads.append(thread)
        camera_index += 1

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("All cameras are closed.")

if __name__ == '__main__':
    main()
