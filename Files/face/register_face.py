import os
import cv2

# Folder to save registered faces
BASE_DIR = os.path.dirname(__file__)
ENCODING_FOLDER = os.path.join(BASE_DIR, "encodings")

os.makedirs(ENCODING_FOLDER, exist_ok=True)


def register_face(username):

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Unable to open camera.")
        return False

    print("===================================")
    print("Press SPACE to capture your face")
    print("Press ESC to cancel")
    print("===================================")

    while True:

        ret, frame = camera.read()

        if not ret:
            break

        cv2.putText(
            frame,
            "Press SPACE to Capture",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.imshow("Register Face", frame)

        key = cv2.waitKey(1)

        # ESC
        if key == 27:
            camera.release()
            cv2.destroyAllWindows()
            return False

        # SPACE
        elif key == 32:

            filename = os.path.join(
                ENCODING_FOLDER,
                f"{username}.jpg"
            )

            cv2.imwrite(filename, frame)

            camera.release()
            cv2.destroyAllWindows()

            print("Face Registered Successfully.")

            return True


if __name__ == "__main__":

    username = input("Enter Username: ")

    success = register_face(username)

    if success:
        print("Saved Successfully")
    else:
        print("Cancelled")