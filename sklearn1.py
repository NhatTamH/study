# import tensorflow as tf
# from tensorflow import keras
# from keras import layers
# import os

# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# if tf.test.gpu_device_name():
#     print('GPU found')
# else:
#     print("No GPU found")

# tf.config.set_visible_devices([], 'GPU')

# model = keras.Sequential(
#     [
#         layers.Dense(2, activation='relu', name='layer1'),
#         layers.Dense(3, activation='relu', name='layer2'),
#         layers.Dense(4, name='layer3'),
#     ]
#     )

# x = tf.ones((3, 3))
# y = model(x)
# print("1")
