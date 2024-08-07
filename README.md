# AirMath

Application that allows you to write mathematical equations in the air using hand gestures, captures the equation using your webcam, and then solves it using a generative AI model. The results are displayed in real-time on a web interface powered by Streamlit.

## Features

- **Airwriting Recognition:** Use your webcam to write equations in the air.
- **Hand Tracking:** Real-time hand tracking to capture the equation using `cvzone` and `OpenCV`.
- **AI-Powered Solutions:** Utilizes Google's generative AI model to solve the equations.
- **Web Interface:** A simple and interactive interface using Streamlit.



**Set up Google Generative AI:**
    - Replace `"gemini_API_Key"` in the `main.py` file with your actual API key.

## Usage

1. **Run the application:**
    ```bash
    streamlit run main.py
    ```

2. **Use the interface:**
    - Check the "Run" checkbox to start the webcam and begin airwriting.
    - The equation will be recognized and processed by the AI model.
    - The solution will be displayed in the "Answer" section.

## Project Structure

- `main.py`: The main script that handles the application logic, hand tracking, AI integration, and web interface.


## Dependencies

- `cvzone`
- `cv2`
- `numpy`
- `streamlit`
- `google.generativeai`
- `PIL`
