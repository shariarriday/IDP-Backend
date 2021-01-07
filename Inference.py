# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from tensorflow.data import Dataset
from tensorflow.data.experimental import AUTOTUNE
from tensorflow import image, cast, float32
from tensorflow.io import decode_image, read_file
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras import Model
from tensorflow.keras.layers import Conv2D,Input,Dense,GlobalAveragePooling2D,Dropout,BatchNormalization
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.models import load_model
from tensorflow import numpy_function
from tensorflow.keras.preprocessing.image import load_img,img_to_array
import numpy as np
import os
import glob

os.system('python opencv_text_detection_image.py --image images/Book2.jpg --east frozen_east_text_detection.pb')

os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
#Global Values
BATCH_SIZE = 32
ROW = 240
COL = 80
file_location = 'output'
words = []
file = open("words.txt", "r", encoding='utf-8')
for line in file:
    words.append(line[:-1])
file.close()


# %%
def create_model(training=True):
    base_model = EfficientNetB0(
        weights="imagenet", include_top=False, input_shape=(ROW, COL, 3))

    x = Input(shape=(ROW, COL, 3))
    out_1 = base_model(x, training=training)
    out_1 = GlobalAveragePooling2D(name='encoding')(out_1)
    out_1 = Dropout(0.5)(out_1)
    output = Dense(934, activation="softmax")(out_1)

    final_model = Model(inputs=x, outputs=output)

    return final_model


# %%
def process_path(file_path):
    print(file_path)
    file = read_file(file_path)
    file = image.decode_jpeg(file, channels=3)
    file = cast(file, float32)
    file = preprocess_input(file)
    file = image.resize(file, [ROW, COL])

    return file

inference = Dataset.list_files(str(file_location+'/*') , shuffle = False)
inference = inference.map(process_path).batch(BATCH_SIZE).prefetch(AUTOTUNE)


# %%
checkpoints = glob.glob(os.path.join('Weights' , 'IDP_Final_B*.h5'))

Models = []
for checkpoint in checkpoints:
    new_model = create_model(training = False)
    new_model.load_weights(checkpoint)
    Models = new_model

print('Models loaded...')

sentence = ''

for data in inference:
    data = data.numpy()
    results = np.argmax(Models.predict(data), axis=1)
    
    for result in results:
        sentence += ' ' + words[result]

f = open("sentence.txt", "w" , encoding = 'utf-8')
f.write(sentence +'\n')
f.close()



