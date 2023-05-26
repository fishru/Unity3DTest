#%%
import os
from tensorflow import keras
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.callbacks import TensorBoard
from tqdm import tqdm
from sklearn.metrics import accuracy_score
import tensorflow_datasets as tfds
print('tf version:', tf.version)
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
#%%
actions = np.array(['left', 'right', 'forward', 'backward', 'jump'])
sequence_length = 37
label_map = {label: num for num, label in enumerate(actions)}
batch_size = 64

def DataLoader(setname, batch_size=batch_size):
    print(f'***Start loading {setname} data.***')
    sequences, labels = [], []
    # Collect the sequences and determine the maximum number of frames
    for action in actions:
        dirs = os.listdir(f'./pose_data/{setname}/{action}')
        print(f'Loading \"{action}\" data...')
        for sequence in tqdm(dirs):
            sequence_data = []
            for frame_num in range(sequence_length):
                res = np.load(f'./pose_data/{setname}/{action}/{sequence}/{frame_num}.npy')
                sequence_data.append(res)
            sequences.append(sequence_data)
            # print(f'{sequence}, {action}: {label_map[action]}')
            labels.append(label_map[action])

    # Pad the sequences to have a consistent length
    padded_sequences = []
    for sequence_data in sequences:
        padded_sequence = np.zeros((sequence_length, 63))
        padded_sequence[:len(sequence_data)] = sequence_data
        padded_sequences.append(padded_sequence)

    x = np.array(padded_sequences)
    y = np.array(labels)

    # One-hot encode the labels
    y = to_categorical(y)

    print("X shape:", x.shape)
    print("y shape:", y.shape)
    print("\n\n")
    # dataset = tf.data.Dataset.from_tensor_slices((X, y))
    # dataset = dataset.shuffle(len(dataset))
    # dataset = dataset.batch(batch_size)
    # dataset = tfds.as_numpy(dataset)
    return x, y
#%%
x_train, y_train = DataLoader('Train')
x_test, y_test = DataLoader('Test')
print(type(x_test))
print(type(y_test))
#%%
log_dir = os.path.join('Logs')
tb_callback = TensorBoard(log_dir=log_dir)
earlystop_callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=100)
num_epoch = 1

model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(sequence_length, 63)))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))

model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
model.fit(x_train, y_train, epochs=num_epoch, shuffle=True, batch_size=batch_size,callbacks=[tb_callback, earlystop_callback])
model.save('model_save/model.h5')
#%%
model2 = tf.keras.models.load_model('model.h5')
# for ds in test_dataset:
#     print(len(ds[1]))
    # print(type(x),type(y))
#     # print(f'{len(x)},{len(y)}')
#     # print(y)
prediction = model2.predict(test_dataset)
# print(prediction.shape)
# # print(prediction)
# print(test_dataset.shape)