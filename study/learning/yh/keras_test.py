### Required Packages Installation
# python 3.9 버전 지원에 관련한 내용이 없으므로 3.8 설치
# pip install -U tensorflow
# conda install keras matplotlib
# tensorflow 사용 시 CUDA 사용 하려면 다음 링크에서 CUDA Toolkit 11.0 설치
# https://developer.nvidia.com/cuda-11.0-download-archive?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exenetwork 

import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

# 이미지 확인용
def show_image(img) :
    plt.figure()
    plt.imshow(img, cmap=plt.cm.binary)
    plt.colorbar()
    plt.grid(False)
    plt.show()

print(tf.__version__)
#tf.debugging.set_log_device_placement(True)

fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

#show_image(train_images[1])

# 0 ~ 255 값을 0 ~ 1 로 스케일링
train_images = train_images / 255.0
test_images = test_images / 255.0

# 학습모델 레이어 추가
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

# 학습모델 컴파일
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 학습 진행
model.fit(train_images, train_labels, epochs=10, verbose=1)

# 테스트
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=1)