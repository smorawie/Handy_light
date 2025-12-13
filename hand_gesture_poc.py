
import os
import cv2
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# for loading dataset, please refresh the datasets again, this is only for poc
data = []
labels = []

gestures = ["ON", "OFF", "UP", "DOWN"]  # adjust to your gestures
for gesture in gestures:
    folder = f"dataset/{gesture}"
    for img_name in os.listdir(folder):
        img_path = os.path.join(folder, img_name)
        img = cv2.imread(img_path)
        if img is None:
            continue
        img = cv2.resize(img, (64, 64))
        img = img / 255.0
        data.append(img)
        labels.append(gesture)

data = np.array(data)
labels = np.array(labels)

# encode labels
le = LabelEncoder()
labels_enc = le.fit_transform(labels)
labels_enc = to_categorical(labels_enc)

# standart stuffs

X_train, X_test, y_train, y_test = train_test_split(data, labels_enc, test_size=0.2, random_state=42)

# CNN thingy, nned
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(64,64,3)),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(len(gestures), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# needs to train everytime you change dataset, ripped from CNN
print("training the model")
model.fit(X_train, y_train, epochs=10, batch_size=16, validation_data=(X_test, y_test))
print("complete!")

#THE WEBCAM, lulz
cap = cv2.VideoCapture(0)
print(" Press ESC to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame_resized = cv2.resize(frame, (64,64))
    frame_normalized = frame_resized / 255.0
    frame_input = np.expand_dims(frame_normalized, axis=0)

    pred = model.predict(frame_input)
    gesture = le.inverse_transform([np.argmax(pred)])[0]
    
    if gesture == "ON":
        text = "💡 Light ON"
    elif gesture == "OFF":
        text = "💡 Light OFF"
    elif gesture == "UP":
        text = "🔆 Brightness UP"
    elif gesture == "DOWN":
        text = "🔅 Brightness DOWN"
    else:
        text = gesture

    cv2.putText(frame, text, (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.imshow("Gesture Control PoC", frame)
    
    if cv2.waitKey(1) & 0xFF == 27:  
        break

cap.release()
cv2.destroyAllWindows()