#%%
import cv2
import mediapipe as mp
import pickle
import numpy as np
import requests
import json
import time

# model_dict = pickle.load(open('./model.p', 'rb')) # model_ori.p
# model = model_dict['model']

#%%
cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
#mp_drawing_styles = mp.solutions.drawing_stylesq
mp_drawing_styles = mp.solutions.drawing_styles


hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3,max_num_hands=1)

labels_dict = {0: 'Left', 1: 'Right', 2: 'Forward', 3: 'Back', 4: 'Jump'}
while True:

    data_aux = []
    x_ = []
    y_ = []
    z_ = []

    ret, frame = cap.read()

    H, W, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    #print(type(results.multi_hand_landmarks))
    if results.multi_hand_landmarks:
        print("Here....")
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,  # image to draw
                hand_landmarks,  # model output
                mp_hands.HAND_CONNECTIONS,  # hand connections
                mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=15),
                mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=10))

        for hand_landmarks in results.multi_hand_landmarks:


            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                z = hand_landmarks.landmark[i].z

                x_.append(x)
                y_.append(y)
                z_.append(z)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                z = hand_landmarks.landmark[i].z
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))
                data_aux.append(z - min(z_))

        x1 = int(min(x_) * W) - 10
        y1 = int(min(y_) * H) - 10

        x2 = int(max(x_) * W) - 10
        y2 = int(max(y_) * H) - 10

        if len(data_aux) >= 126:
            print("!!!!!!!!!!!")
        
        print("Detected!!")
        print(len(data_aux))
        print(data_aux)

    else:
        data_aux = np.array(np.zeros(21 * 3))
        data_aux = data_aux.tolist()
        print("No detected!!")
        print(len(data_aux))
        print(data_aux)

        
#         prediction = model.predict([np.asarray(data_aux)])
        #prediction = np.argmax(model.predict([np.asarray(data_aux)]), axis=-1)
#         print(f'prediction= {prediction}')
#         predicted_character = labels_dict[int(prediction[0])]
        # Create a JSON payload
#         payload = {"action": predicted_character}
#         print(predicted_character)


        # Send a POST request with JSON payload
        
#         response = requests.post('http://127.0.0.1:8000', json=payload)
        
#         if response.status_code == 200:
#             print('Prediction sent successfully.')



#         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
#         cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
#                     cv2.LINE_AA)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

