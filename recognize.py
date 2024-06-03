from keras.applications import VGG16
from keras.applications.vgg16 import preprocess_input, decode_predictions
from keras.utils import load_img, img_to_array
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

# Load the VGG16 model
model = VGG16(weights="imagenet")

def show_image(image_path):
    """ Display image from the path """
    image = mpimg.imread(image_path)
    plt.imshow(image)
    plt.show()

def load_and_process_image(image_path):
    """ Load and preprocess the image for VGG16 model """
    image = load_img(image_path, target_size=(224, 224))
    image_array = img_to_array(image)
    image_array_reshaped = image_array.reshape(1, 224, 224, 3)
    return preprocess_input(image_array_reshaped)

def recognize_image(image_path):
    """ Recognize the image using VGG16 model and return the top prediction """
    # Show the image (optional, can be removed if not needed)
    # show_image(image_path)

    # Load and preprocess the image
    image_preprocessed = load_and_process_image(image_path)

    # Predict using VGG16 model
    predictions = model.predict(image_preprocessed)

    # Decode predictions
    top_predictions = decode_predictions(predictions, top=1)
    top1prediction_name = top_predictions[0][0][1].replace('_', ' ')
    return top1prediction_name