README = """
このDemoは、HandTracking情報をTCP/IPで通信するものです。
Unity用のScriptをfor Unityフォルダに置いてあります。
"""
import sys
sys.path.append("../..")
import numpy as np
from HandTrackerRenderer import HandTrackerRenderer
from HandTracker import HandTracker
import json
import socket
from concurrent.futures import ThreadPoolExecutor

tracker = HandTracker(use_gesture=True, xyz=True, use_lm='full', use_world_landmarks=True, solo=False)
renderer = HandTrackerRenderer(
        tracker=tracker)

STATUS={'hand':{}, 'running':True}

ip_address = '127.0.0.1'
port = 7010

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip_address, port))
s.listen(5)


def loop():
    while STATUS['running']:
        try:
            conn, addr = s.accept()
            hand = STATUS['hand']
            conn.sendall(json.dumps(hand).encode())
        except Exception as e:
            pass

socket_worker = ThreadPoolExecutor(1)
ft = socket_worker.submit(loop)


def numlist2xyz(items):
    dim = ['x', 'y', 'z']
    return {k:v for k, v in zip(dim, items)}


while True:
    # Run hand tracker on next frame
    # 'bag' contains some information related to the frame
    # and not related to a particular hand like body keypoints in Body Pre Focusing mode
    # Currently 'bag' contains meaningful information only when Body Pre Focusing is used
    frame, hands, bag = tracker.next_frame()
    # conn, addr = s.accept()
    if frame is None: break
    data = {'hands':[]}
    # print  hands info
    for hand in hands:
        hand_dict = {
            'gesture':hand.gesture,
            'handedness':hand.handedness,
            'index_state':hand.index_state,
            'label':hand.label,
            'landmarks': [numlist2xyz(x) for x in hand.landmarks.tolist()],
            'little_state':hand.little_state,
            'lm_score':hand.lm_score,
            'middle_state':hand.middle_state,
            'norm_landmarks':[numlist2xyz(x) for x in hand.norm_landmarks.tolist()],
            'pd_box':hand.pd_box.tolist() if hand.pd_box is not None else None,
            'pd_kps':[numlist2xyz(x) for x in hand.pd_kps] if hand.pd_kps is not None else None,
            'pd_score':hand.pd_score,
            'rect_h_a':hand.rect_h_a,
            'rect_points':[numlist2xyz(x) for x in hand.rect_points],
            'rect_w_a':hand.rect_w_a,
            'rect_x_center_a':hand.rect_x_center_a,
            'rect_y_center_a':hand.rect_y_center_a,
            'ring_state':hand.ring_state,
            'rotation':hand.rotation,
            'thumb_angle':hand.thumb_angle,
            'thumb_state':hand.thumb_state,
            'rota':[numlist2xyz(x) for x in hand.world_landmarks.tolist()],
            'rotated_world_landmarks':[numlist2xyz(x) for x in hand.get_rotated_world_landmarks()],
            'world_landmarks':[numlist2xyz(x) for x in hand.world_landmarks.tolist()],
            'xyz':numlist2xyz(hand.xyz.tolist()),
            'xyz_zone':numlist2xyz( hand.xyz_zone)
        }
        data['hands'].append(hand_dict)
    STATUS['hand'] = data
    # Draw hands
    frame = renderer.draw(frame, hands, bag)
    # frame = renderer.draw(frame,[])
    key = renderer.waitKey(delay=1)
    if key == 27 or key == ord('q'):
        break

STATUS['running'] = False
print('abort connection')
s.close()
print('wait terminate loop')
ft.result()
renderer.exit()
tracker.exit()
