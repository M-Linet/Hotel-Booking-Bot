import json
import nltk
from nltk.tokenize import word_tokenize
from sklearn.preprocessing import LabelEncoder
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Download necessary NLTK resources if not already available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Load intents from JSON file
with open('intents.json') as f:
    intents_data = json.load(f)

# Prepare the data
texts = []
intents = []
for intent in intents_data['intents']:
    for example in intent['examples']:
        texts.append(example)
        intents.append(intent['intent'])

# Tokenization and label encoding
tokenized_texts = [word_tokenize(text.lower()) for text in texts]
le = LabelEncoder()
labels = le.fit_transform(intents)

# Create the tokenizer and fit on texts
tokenizer = tf.keras.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(tokenized_texts)
sequences = tokenizer.texts_to_sequences(tokenized_texts)

# Pad sequences
padded_sequences = pad_sequences(sequences, padding='post')

#check if model exists if otherwise make and train a new one
model_filename = 'hotel_booking_model.keras'
try:
    model = load_model(model_filename)
    print('load existing model')
except:
    model = Sequential()
    model.add(Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=64))
    model.add(LSTM(128, return_sequences=True))
    model.add(GlobalAveragePooling1D())
    model.add(Dense(len(set(intents)), activation='softmax')) 

# Compile the model
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(padded_sequences, np.array(labels), epochs=10, batch_size=8)

#save the model
model.save(model_filename)
print('trained and saved model')

# Function to predict intent
def predict_intent(user_input):
    sequence = tokenizer.texts_to_sequences([user_input])
    padded = pad_sequences(sequence, padding='post', maxlen=padded_sequences.shape[1])
    prediction = model.predict(padded)
    return le.inverse_transform([np.argmax(prediction)])[0]

def initialize_log_file(filename='interaction_log.json'):
    initialize_log_file()
# Main chatbot loop
print("Hotel Booking Chatbot: Type a greeting or type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Bot: Goodbye!")
        break
    response_intent = predict_intent(user_input)
    if response_intent == "greeting":
        print("Bot: Hi there! How can I help you today?")
    elif response_intent == "book_room":
        print("Bot: Sure! What type of room would you like to book?")
    elif response_intent == "check_availability":
        print("Bot: Let me check the availability for you.")
    elif response_intent == "cancel_booking":
        print("Bot: I can help you with that. Can you provide your booking details?")
    elif response_intent == "view_booking":
        print("Bot: Please provide your booking reference to view details.")
    elif response_intent == "farewell":
        print("Bot: Goodbye! Have a great day!")
    else:
        print("Bot: I'm sorry, I didn't understand that.")

#log interaction
def log_interaction(user_input, bot_response, filename='interaction_log.json'):
    log_interaction(user_input, bot_response)

