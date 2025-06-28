import pickle
import numpy as np
from flask import Flask, request, render_template, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from flask_cors import CORS
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


try:
    model = load_model("predictive_keyboard_model.h5")
    with open("tokenizer.pkl", "rb") as f:
        data = pickle.load(f)
    tokenizer = data['tokenizer']
    max_seq_len = data['max_seq_len']
    total_words = data['total_words']
    logger.info("Model and tokenizer loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    model = None
    tokenizer = None
    max_seq_len = None
    total_words = None

def predict_next_word(seed_text, n_words=1):
    if not model or not tokenizer or max_seq_len is None:
        return seed_text
    
    try:
        result = seed_text
        for _ in range(n_words):
            token_list = tokenizer.texts_to_sequences([result])[0]
            if len(token_list) == 0:
                break
                
            token_list = pad_sequences([token_list], maxlen=max_seq_len-1, padding='pre')
            predicted = np.argmax(model.predict(token_list, verbose=0), axis=-1)
            
            output_word = ""
            for word, index in tokenizer.word_index.items():
                if index == predicted:
                    output_word = word
                    break
                    
            if output_word == "":
                break
                
            result += " " + output_word
        return result
    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        return seed_text

def get_top_next_words(seed_text, top_n=5):
    if not model or not tokenizer or max_seq_len is None:
        return []
    
    try:
        if not seed_text.strip():
            return []
            
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        if len(token_list) == 0:
            return []
            
        token_list = pad_sequences([token_list], maxlen=max_seq_len-1, padding='pre')
        preds = model.predict(token_list, verbose=0)[0]

        top_indices = preds.argsort()[-top_n:][::-1]
        index_word = {v: k for k, v in tokenizer.word_index.items()}
        
        suggestions = []
        for idx in top_indices:
            word = index_word.get(idx)
            if word and word not in suggestions:
                suggestions.append(word)
                
        return suggestions[:top_n]
    except Exception as e:
        logger.error(f"Error getting suggestions: {e}")
        return []

def get_word_completion(partial_word, top_n=3):
    if not tokenizer:
        return []
    
    try:
        suggestions = []
        partial_lower = partial_word.lower()
        
        for word, index in tokenizer.word_index.items():
            if word.lower().startswith(partial_lower) and word.lower() != partial_lower:
                suggestions.append(word)
                if len(suggestions) >= top_n:
                    break
                    
        return suggestions
    except Exception as e:
        logger.error(f"Error in word completion: {e}")
        return []

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        seed = data.get('seed', '').strip()
        n_words = int(data.get('n_words', 1))
        
        
        if n_words < 1 or n_words > 10:
            n_words = 1
            
        prediction = predict_next_word(seed, n_words)
        return jsonify({'prediction': prediction})
        
    except Exception as e:
        logger.error(f"Error in predict endpoint: {e}")
        return jsonify({'error': 'Prediction failed'}), 500

@app.route('/autocomplete', methods=['POST'])
def autocomplete():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        seed = data.get('seed', '').strip()
        top_n = int(data.get('top_n', 5))
        
  
        if top_n < 1 or top_n > 10:
            top_n = 5
            

        words = seed.split()
        if words and not seed.endswith(' '):
            partial_word = words[-1]
            suggestions = get_word_completion(partial_word, top_n)
        else:
            suggestions = get_top_next_words(seed, top_n)
            
        return jsonify({'suggestions': suggestions})
        
    except Exception as e:
        logger.error(f"Error in autocomplete endpoint: {e}")
        return jsonify({'error': 'Autocomplete failed'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'tokenizer_loaded': tokenizer is not None
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)