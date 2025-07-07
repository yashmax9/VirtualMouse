import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Initialize Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Screen size
screen_width, screen_height = pyautogui.size()

# Webcam setup
cap = cv2.VideoCapture(0)

# Previous finger position
prev_x, prev_y = 0, 0

# Sensitivity factor for speed control
sensitivity = 2.5

# Click states
left_click = False
right_click = False
dragging = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Mirror image
    frame_height, frame_width, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark

            # Get fingertip positions
            index = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            thumb = landmarks[mp_hands.HandLandmark.THUMB_TIP]

            index_x, index_y = int(index.x * frame_width), int(index.y * frame_height)
            middle_x, middle_y = int(middle.x * frame_width), int(middle.y * frame_height)
            thumb_x, thumb_y = int(thumb.x * frame_width), int(thumb.y * frame_height)

            # Draw fingertip markers
            cv2.circle(frame, (index_x, index_y), 8, (255, 0, 255), -1)
            cv2.circle(frame, (thumb_x, thumb_y), 8, (0, 255, 255), -1)

            # Cursor movement by direction (relative)
            if prev_x != 0 and prev_y != 0:
                dx = (index_x - prev_x) * sensitivity
                dy = (index_y - prev_y) * sensitivity

                mouse_x, mouse_y = pyautogui.position()

                new_x = mouse_x + dx
                new_y = mouse_y + dy

                new_x = np.clip(new_x, 0, screen_width - 1)
                new_y = np.clip(new_y, 0, screen_height - 1)

                pyautogui.moveTo(new_x, new_y)

            prev_x, prev_y = index_x, index_y

            # Calculate distances for gestures
            dist_index_thumb = np.hypot(index_x - thumb_x, index_y - thumb_y)
            dist_middle_thumb = np.hypot(middle_x - thumb_x, middle_y - thumb_y)

            # ---- Left Click (Index + Thumb) ----
            if dist_index_thumb < 30:
                if not left_click:
                    left_click = True
                    pyautogui.click()
                    cv2.putText(frame, 'Left Click', (index_x, index_y - 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                left_click = False

            # ---- Right Click (Middle + Thumb) ----
            if dist_middle_thumb < 30:
                if not right_click:
                    right_click = True
                    pyautogui.rightClick()
                    cv2.putText(frame, 'Right Click', (middle_x, middle_y - 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            else:
                right_click = False

            # ---- Drag and Drop (Hold Index + Thumb) ----
            if dist_index_thumb < 30:
                if not dragging:
                    dragging = True
                    pyautogui.mouseDown()
                    cv2.putText(frame, 'Dragging', (index_x, index_y + 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            else:
                if dragging:
                    dragging = False
                    pyautogui.mouseUp()

            # ---- Scroll ----
            # Scroll if middle finger is folded (i.e. distance to thumb is large) and move hand up/down
            if dist_middle_thumb > 100:
                if index_y < frame_height // 3:
                    pyautogui.scroll(20)  # Scroll Up
                    cv2.putText(frame, 'Scroll Up', (index_x, index_y - 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                elif index_y > frame_height * 2 // 3:
                    pyautogui.scroll(-20)  # Scroll Down
                    cv2.putText(frame, 'Scroll Down', (index_x, index_y + 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    else:
        prev_x, prev_y = 0, 0  # Reset if no hand detected
        if dragging:
            dragging = False
            pyautogui.mouseUp()

    cv2.imshow("Virtual Mouse with Gestures", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
