import os
import cv2
from deepface import DeepFace

BASE_DIR = os.path.dirname(__file__)
ENCODING_FOLDER = os.path.join(BASE_DIR, "encodings")
TEMP_IMAGE = os.path.join(BASE_DIR, "temp.jpg")


def verify_face(username):

    registered_image = os.path.join(
        ENCODING_FOLDER,
        f"{username}.jpg"
    )

    if not os.path.exists(registered_image):
        print("Registered face not found.")
        return False

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Unable to open camera.")
        return False

    print("===========================")
    print("Press SPACE to verify")
    print("Press ESC to cancel")
    print("===========================")

    while True:

        success, frame = camera.read()

        if not success:
            break

        cv2.putText(
            frame,
            "Press SPACE to Verify",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.imshow("Face Verification", frame)

        key = cv2.waitKey(1)

        if key == 27:

            camera.release()
            cv2.destroyAllWindows()

            return False

        elif key == 32:

            cv2.imwrite(
                TEMP_IMAGE,
                frame
            )

            camera.release()
            cv2.destroyAllWindows()

            break

    try:

        result = DeepFace.verify(
            img1_path=registered_image,
            img2_path=TEMP_IMAGE,
            model_name="Facenet512",
            detector_backend="opencv",
            enforce_detection=True
        )

        if os.path.exists(TEMP_IMAGE):
            os.remove(TEMP_IMAGE)

        return result["verified"]

    except Exception as e:

        print("Verification Error:", e)

        if os.path.exists(TEMP_IMAGE):
            os.remove(TEMP_IMAGE)

        return False


if __name__ == "__main__":

    username = input("Username: ")

    if verify_face(username):
        print("Face Verified Successfully")
    else:
        print("Face Verification Failed")