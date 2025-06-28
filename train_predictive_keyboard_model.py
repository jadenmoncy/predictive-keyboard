import numpy as np
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.sequence import pad_sequences


with open("large_corpus.txt", "r") as f:
    corpus = [line.strip() for line in f if line.strip()]


all_text = " ".join(corpus).lower()
tokenizer = Tokenizer()
tokenizer.fit_on_texts([all_text])
total_words = len(tokenizer.word_index) + 1


input_sequences = []
for line in corpus:
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(2, len(token_list)+1):
        n_gram_sequence = token_list[:i]
        input_sequences.append(n_gram_sequence)


max_seq_len = max([len(seq) for seq in input_sequences])
input_sequences = pad_sequences(input_sequences, maxlen=max_seq_len, padding='pre')


X = input_sequences[:, :-1]
y = input_sequences[:, -1]
y = to_categorical(y, num_classes=total_words)


model = Sequential()
model.add(Embedding(total_words, 64, input_length=max_seq_len-1))
model.add(LSTM(100))
model.add(Dense(total_words, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


print("Training the model...")
model.fit(X, y, epochs=20, verbose=1)  


model.save("predictive_keyboard_model.h5")
with open("tokenizer.pkl", "wb") as f:
    pickle.dump({'tokenizer': tokenizer, 'max_seq_len': max_seq_len, 'total_words': total_words}, f)

print("Model and tokenizer saved.")