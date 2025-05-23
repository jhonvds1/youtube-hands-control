import cv2
import mediapipe as mp
import pyautogui
import time


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()

camera = cv2.VideoCapture(0)
resolutiox_x = 1920
resolutiox_y = 1080
camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolutiox_x)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolutiox_y)

def find_coord_hand(img, side_inverted = False):
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)
    if result.multi_hand_landmarks:
        for hand_side, hand_landmark in zip(result.multi_handedness, result.multi_hand_landmarks):
            hand_info = {}
            coords = []
            for mark in hand_landmark.landmark:
                coord_x = int(mark.x * resolutiox_x)
                coord_y = int(mark.y * resolutiox_y)
                coord_z = int(mark.z * resolutiox_x)
                coords.append((coord_x, coord_y, coord_z))
                hand_info['coordenadas'] = coords
            if side_inverted:
                if hand_side.classification[0].label == 'left':
                    hand_info['side'] = 'right'
                else:
                    hand_info['side'] = 'left'
            else:
                hand_info['side'] = hand_side.classification[0].label
            all_hands.append(hand_info)
            mp_drawing.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)
    return img, all_hands

def fingers_raised(hand):
    fingers = []
    for finger_tip in [8, 12, 16, 20]:
        if hand['coordenadas'][finger_tip][1] < hand['coordenadas'][finger_tip-2][1]:
            fingers.append(True)
        else:
            fingers.append(False)
    return fingers


while camera.isOpened():
    ret, frame = camera.read()
    all_hands = []
    frame = cv2.flip(frame, 1)
    if not ret:
        print('Frame vazio')
        continue
    img, all_hands = find_coord_hand(frame, False)
    if len(all_hands) == 1:
        info_finger_hand = fingers_raised(all_hands[0])
        if info_finger_hand == [True, False, False, True]:
            break
        elif info_finger_hand == [True, False, False, False]:
            pyautogui.press('space')
            time.sleep(1)
        elif info_finger_hand == [True, True, False, False]:
            pyautogui.hotkey('shift', 'n')
            time.sleep(1)
        elif info_finger_hand == [True, True, True, False]:
            back_img = pyautogui.locateCenterOnScreen('back.png', confidence=0.8)
            pyautogui.click(back_img)
            time.sleep(1)
        elif info_finger_hand == [True, True, True, True]:
            pyautogui.press('up')
            time.sleep(1)
        elif info_finger_hand == [True, False, True, False]:
            pyautogui.press('down') 
            time.sleep(1)
        elif info_finger_hand == [True, False, True, True]:
            pyautogui.press('m')
            time.sleep(1)
        elif info_finger_hand == [False, True, True, True]:
            pyautogui.press('right')
        elif info_finger_hand == [False, False, True, True]:
            pyautogui.press('left')
            time.sleep(1)
    cv2.imshow('Camera', img)
    key = cv2.waitKey(1)
    if key == 27:
        break








