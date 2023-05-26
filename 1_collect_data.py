import cv2
import mediapipe as mp
import numpy as np
import os

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


def mediapipe_detection(image, model):
    results = model.process(image)
    return image, results


def draw_landmarks(image, results):
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=10),
                                      mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=5)

                                      )


def extract_key_points(results):
    # extract key value points
    pose = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                z = hand_landmarks.landmark[i].z
                co_ordinate = np.array([x, y, z])
                pose.append(co_ordinate)


        pose = np.array(pose).flatten()  # for LSTM (63, )
        print("Hand detected: " + str(pose.shape))

    else:
        pose = np.array(np.zeros(21 * 3))
        print("No hand detected: " + str(pose.shape))

    print("Pose shape:", pose.shape)
    return pose

SET = ['Test','Train', 'Validation']
# path for exported data, numpy array
DATA_PATH = os.path.join('pose_data')

# actions that we try to detect
actions = np.array(['left', 'right', 'forward', 'backward', 'jump'])

# 30 videos worth of data
number_sequences = 30

# each video will be 30 frames long
sequence_length = 37

#%%
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5,max_num_hands=1) as hands:
    for setname in SET:
        for action in actions:
            dirs = os.listdir("./data_selection/"+setname+"/"+action)
            num_dirs = len(dirs)
            for dir_name in dirs:
                save_path = os.path.join(DATA_PATH, setname, action, dir_name)
                #print(save_path)
                imgs_dir = os.path.join("data_selection",setname,action,dir_name)
                imgs = os.listdir(imgs_dir)
                for i in range(sequence_length):
                    image_path = os.path.join(imgs_dir,imgs[i])
                    print(image_path)
                    frame = cv2.imread(image_path)
                    image, results = mediapipe_detection(frame, hands)
                    draw_landmarks(image, results)
                    key_points = extract_key_points(results)
                    os.makedirs(save_path, exist_ok=True)
                    numpy_file_path = os.path.join(save_path, str(i))
                    print(numpy_file_path)
                    np.save(numpy_file_path, key_points)