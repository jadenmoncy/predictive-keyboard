import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


model = load_model("predictive_keyboard_model.h5")
with open("tokenizer.pkl", "rb") as f:
    data = pickle.load(f)
tokenizer = data['tokenizer']
max_seq_len = data['max_seq_len']
total_words = data['total_words']


def predict_next_word(seed_text, n_words=1):
    for _ in range(n_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_seq_len-1, padding='pre')
        predicted = np.argmax(model.predict(token_list, verbose=0), axis=-1)
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        if output_word == "":
            break
        seed_text += " " + output_word
    return seed_text


if __name__ == "__main__":
    print("\n--- Predictive Keyboard Demo ---")
    while True:
        seed = input("Enter a seed phrase to predict next words (or type 'exit' to quit): ")
        if seed.strip().lower() == "exit":
            break
        try:
            n_words = int(input("How many words to predict? "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        print("Prediction:", predict_next_word(seed, n_words=n_words))