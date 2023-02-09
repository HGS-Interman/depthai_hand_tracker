README = """
このDemoは、HandTracking情報をmouse操作に変換するものです。
"""
import sys
sys.path.append("../..")
import numpy as np
from HandTrackerRenderer import HandTrackerRenderer
from HandTracker import HandTracker
from pynput.mouse import Controller, Button
mouse = Controller()

tracker = HandTracker(use_gesture=True, xyz=True, use_lm='full', use_world_landmarks=True, solo=True)
renderer = HandTrackerRenderer(
        tracker=tracker)

pre_position = None
sensitive  = -2
scroll_sensitive = 0.2
try:
    while True:
        frame, hands, bag = tracker.next_frame()
        if frame is None: break
        data = {'hands':[]}
        frame = renderer.draw(frame, hands, bag)
        key = renderer.waitKey(delay=1)
        if key == 27 or key == ord('q'):
            break
        if hands:
            hand = hands[0]
            if not(500< hand.xyz[2] < 1200):
                print(f"out of range. {hand.xyz[2] }")
                continue
            if pre_position is None:
                pre_position = hand.xyz
            if hand.gesture == "FOUR" or hand.gesture == "FIVE":
                mouse.release(Button.left)
                mouse.release(Button.right)
            if hand.gesture == "ONE":
                mouse.release(Button.left)
                mouse.release(Button.right)
                mouse.move(sensitive*(hand.xyz[0]-pre_position[0]), sensitive*( hand.xyz[1]-pre_position[1]))
            if hand.gesture == "PEACE":
                mouse.release(Button.left)
                mouse.press(Button.left)
                mouse.move(sensitive*(hand.xyz[0]-pre_position[0]), sensitive*( hand.xyz[1]-pre_position[1]))
            if hand.gesture == "FIST":
                mouse.release(Button.left)
                mouse.press(Button.right)
                mouse.move(sensitive*(hand.xyz[0]-pre_position[0]), sensitive*( hand.xyz[1]-pre_position[1]))
                mouse.scroll(0, scroll_sensitive*( hand.xyz[2]-pre_position[2]))
            pre_position = hand.xyz
            print(pre_position)
        else:
            mouse.release(Button.left)
            mouse.release(Button.right)

finally:
    renderer.exit()
    tracker.exit()
