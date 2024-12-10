
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import time

model = load_model('model_results/saved_model.h5')

import os
class_labels = [i for i in range(33)]


def preprocess_frame(frame):
    img = cv2.resize(frame, (100, 100))
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict_frame(frame):
    processed_frame = preprocess_frame(frame)
    predictions = model.predict(processed_frame)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    confidence = predictions[0][predicted_class_index] * 100
    return class_labels[predicted_class_index], confidence

try:
    while True:
        frame = cv2.capture_array()
        predicted_class, confidence = predict_frame(frame)
        cv2.putText(frame, f"{predicted_class} ({confidence:.2f}%)", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow("PiCamera - Real-Time Classification", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    picam2.stop()
    cv2.destroyAllWindows()