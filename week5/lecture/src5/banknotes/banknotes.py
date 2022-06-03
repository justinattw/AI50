import csv
import tensorflow as tf

from sklearn.model_selection import train_test_split

# Read data in from file
with open("banknotes.csv") as f:
    reader = csv.reader(f)
    next(reader)

    data = []
    for row in reader:
        data.append({
            "evidence": [float(cell) for cell in row[:4]],
            "label": 1 if row[4] == "0" else 0
        })

# Separate data into training and testing groups
evidence = [row["evidence"] for row in data]
labels = [row["label"] for row in data]
X_training, X_testing, y_training, y_testing = train_test_split(
    evidence, labels, test_size=0.4
)

# Create a neural network
model = tf.keras.models.Sequential()

# Add a hidden layer with 8 units, with ReLU activation
# Dense layer:  every node in hidden layer is connected to every node in previous layer
# 8 units:      arbitrary choice - more units comes at a cost - risk of added computation and of overfitting
# input_shape:  4, because input has 4 values.
model.add(tf.keras.layers.Dense(8, input_shape=(4,), activation="relu"))

# Add output layer with 1 unit, with sigmoid activation
# Sigmoid:  standardises output value within 0-1.
model.add(tf.keras.layers.Dense(1, activation="sigmoid"))

# Train neural network
model.compile(
    optimizer="adam",  # how to optimise weight
    loss="binary_crossentropy",  # loss function
    metrics=["accuracy"]  # how to evaluate the model (accuracy = number of points classified correctly)
)

# Train model for 20 epochs (run through each training point 20 times)
model.fit(X_training, y_training, epochs=20)

# Evaluate how well model performs
model.evaluate(X_testing, y_testing, verbose=2)
