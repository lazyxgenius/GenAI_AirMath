import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import google.generativeai as genai
from PIL import Image
import streamlit as st

st.set_page_config(layout="wide")
col1, col2 = st.columns([2,1]) # 2:1 split

with col1:
    prompt = st.text_input("Enter your prompt:", "")  # Add this line

    if prompt:  # Modify this condition
        # Open camera and proceed with the rest of the logic
        FRAME_WINDOW = st.image([])  # This will now only run if the prompt is provided
    else:
        st.warning("Please enter a prompt and press ENTER to start the camera.")
        # will take around 1 min


with col2:
    output_area = st.title("Answer")
    output_text_area = st.empty()


genai.configure(api_key="api_key_xyz-xyz")
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize the webcam to capture video
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
# Initialize the HandDetector class with the given parameters
detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.7, minTrackCon=0.5)


def getHandinfo(img):
    # Find hands in the current frame
    # The 'draw' parameter draws landmarks and hand outlines on the image if set to True
    # The 'flipType' parameter flips the image, making it easier for some detections
    hands, img = detector.findHands(img, draw=True, flipType=True)

    # Check if any hands are detected
    if hands:
        # Information for the first hand detected
        hand = hands[0]  # Get the first hand detected
        lmList = hand["lmList"]  # List of 21 landmarks for the first hand
        # Count the number of fingers up for the first hand
        fingers = detector.fingersUp(hand)
        print(fingers)  # Print the fingers that are up

        return fingers, lmList
    else:
        return None


def draw(info, prev_pos, canvas):
    fingers, lmlist = info
    current_pos = None
    # everytime there is no detection of any finger,
    # it will reset
    if fingers == [0, 1, 0, 0, 0]:
        # only write when only index finger is detected
        current_pos = lmlist[8][0:2]
        # tip of the index finger is position 8,
        # and we want its x and y coordinate hence 0 and 1
        if prev_pos is None: prev_pos = current_pos
        cv2.line(canvas, current_pos, prev_pos, (255, 0, 255), 10)

    elif fingers == [1, 1, 1, 1, 1]:
        canvas = np.zeros_like(img)

    return current_pos, canvas


def sendToAI(model, canvas, fingers, prompt):
    if fingers == [1, 1, 1, 1, 0]:
        pil_image = Image.fromarray(canvas)
        # convert image into PIL image before sending
        response = model.generate_content([prompt, pil_image])
        return response.text


prev_pos = None
canvas = None
image_combined = None
output_text = ""

# Continuously get frames from the webcam
while True:
    # Capture each frame from the webcam
    # 'success' will be True if the frame is successfully captured, 'img' will contain the frame
    success, img = cap.read()
    img = cv2.flip(img, 1)

    if canvas is None:
        canvas = np.zeros_like(img)
        # create a black canvas, size of img

    info = getHandinfo(img)
    if info:
        fingers, lmlist = info
        # print(fingers)
        prev_pos, canvas = draw(info, prev_pos, canvas)
        output_text = sendToAI(model, canvas, fingers, prompt)
    # Merging the image and canvas
    image_combined = cv2.addWeighted(img, 0.7, canvas, 0.3, 0)

    # Streamlit frontend setup
    FRAME_WINDOW.image(image_combined, channels="BGR")
    if output_text:
        output_text_area.write(output_text)

    # Display the images in a window
    # cv2.imshow("Image", img)
    # cv2.imshow("Canvas", canvas)
    # cv2.imshow("image_combines", image_combined)

    # Keep the window open and update it for each frame; wait for 1 millisecond between frames
    cv2.waitKey(1)


