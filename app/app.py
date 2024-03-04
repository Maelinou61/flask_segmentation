from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
import cv2

app = Flask(__name__)

# Charger le modèle TensorFlow Lite
interpreter = tf.lite.Interpreter(model_path="app/weights.tflite")
interpreter.allocate_tensors()

@app.route('/')
def index():
   return 'Hello World'

@app.route('/predict', methods=['POST'])
def predict():
    uploaded_file = request.files['image']
    image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
    image = cv2.resize(image, (320, 320))

    preprocessed_image = preprocess_image(image).astype(np.float32)

    # Préparer les tenseurs d'entrée et de sortie
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Injecter les données d'entrée dans le modèle TensorFlow Lite
    interpreter.set_tensor(input_details[0]['index'], np.expand_dims(preprocessed_image, axis=0))

    # Effectuer l'inférence
    interpreter.invoke()

    # Récupérer les résultats de l'inférence
    prediction = interpreter.get_tensor(output_details[0]['index'])
    prediction = postprocess_prediction(prediction)
    
    prediction = (prediction*255).astype(np.uint8)

    response = {'result': prediction.tolist()}
    return jsonify(response)

def preprocess_image(image):
    # Ajouter tout prétraitement nécessaire ici
    return image

def postprocess_prediction(prediction):
    # Ajouter tout post-traitement nécessaire ici
    prediction = 1 * (prediction > 0.5)
    return prediction.squeeze()

if __name__ == '__main__':
   app.run(debug=True)
