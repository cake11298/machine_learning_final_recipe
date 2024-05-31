import base64
import requests

api_key = "YOUR_API"

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

image_path = "189.jpeg"

from keras.applications import VGG16

# Load the VGG16 model
model = VGG16(weights="imagenet")
model.summary() # show the imagenet model architecture and the number of parameters

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import keras.utils as image_utils

# Show image function
def show_image(image_path):
    if "http" in image_path:
        image_path = image_utils.get_file(origin=image_path)
    image = mpimg.imread(image_path)
    plt.imshow(image)

from keras.applications.vgg16 import preprocess_input

# Load and pre-process image function for VGG16 model
def load_and_process_image(image_path):
    if "http" in image_path:
        image_path = image_utils.get_file(origin=image_path)
    image_s = image_utils.load_img(image_path, target_size=(224, 224)) # load image and resize it to 224x224
    image_s_array = image_utils.img_to_array(image_s) # change the format of the image to array
    # single picture, so expand_dims
    image_s_array_reshape = image_s_array.reshape(1, 224, 224, 3) # reshape the image to 4D array
    # ImageNet preprocessing
    image_forVGG16 = preprocess_input(image_s_array_reshape) # preprocess the image for VGG16 model
    return image_forVGG16
  
from keras.applications.vgg16 import decode_predictions

# Make predictions using the VGG16 pre-trained model
def readable_prediction(image_path):
    # Show image
    show_image(image_path)
    # Load and pre-process image
    image = load_and_process_image(image_path)
    # Make predictions using the VGG16 pre-trained model, but it is not human-readable
    predictions = model.predict(image) 
    # Print predictions in readable form (get top 3 predictions)
    # Get the name of top 1 prediction and change the "_" into " "
    top_predictions = decode_predictions(predictions, top=1)
    top1prediction_name = top_predictions[0][0][1].replace('_', ' ')
    return top1prediction_name

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "gpt-4-turbo",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          # "text": "請分辨出此圖片中所有食材，並且使用英文列出，格式需要遵照以下回傳，並且不要回傳別的，例如\"1. shrimp 2. tomato 3. XXX\"，若沒有食材請回覆No"
          "text": "問問題 但好像也不用問問題?"
        },
        {
          "type": "text",
          "text": readable_prediction(image_path)
        }
      ]
    }
  ],
  "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

# print(response.json()['choices'][0]['message']['content'])