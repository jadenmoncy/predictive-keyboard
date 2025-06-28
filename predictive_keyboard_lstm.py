import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer # type: ignore
from tensorflow.keras.utils import to_categorical # type: ignore
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Embedding, LSTM, Dense # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore

def get_user_corpus():
    print("Enter your text corpus, one sentence per line. Type 'END' to finish:")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        if line.strip():
            lines.append(line.strip())
    return lines

if __name__ == "__main__":
    corpus = get_user_corpus()
    if not corpus:
        print("No corpus provided. Exiting.")
        exit(1)

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


    print("Training the model.")
    model.fit(X, y, epochs=200, verbose=1)


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