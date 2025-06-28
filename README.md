# Predictive Keyboard with Modern UI

A sophisticated predictive keyboard application that combines machine learning with a beautiful, responsive interface. Built with React, Flask, and TensorFlow, this project demonstrates modern AI-powered text prediction with a keyboard-like user experience.

## Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Architecture](#-architecture)

## Features

### **Modern User Interface**
- **Virtual Keyboard**: Full QWERTY layout with special keys (Shift, Caps Lock, Backspace, Space, Enter)
- **Real-time Suggestions**: Word predictions appear above the keyboard in a mobile-friendly format
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Dark Mode Support**: Automatic dark mode detection and styling
- **Smooth Animations**: Modern transitions and hover effects

### **Intelligent Predictions**
- **Word Completion**: Suggests completions for partial words as you type
- **Context-Aware Predictions**: Uses LSTM neural network for next-word prediction
- **Multiple Suggestions**: Shows up to 5 word suggestions with smart ranking
- **Real-time Updates**: Suggestions update as you type

### **Keyboard Features**
- **Dual Input**: Use virtual keyboard or physical keyboard
- **Case Handling**: Proper Shift and Caps Lock functionality
- **Special Keys**: Backspace, Space, Enter with visual feedback
- **Touch-Friendly**: Large, easy-to-tap keys for mobile devices


## Quick Start

### Prerequisites
- Python 3.7 or higher
- Node.js 14 or higher
- npm or yarn

### One-Command Setup
```bash
# Clone the repository
git clone https://github.com/jadenmoncy/predictive-keyboard.git
cd predictive-keyboard

# Run the startup script (checks dependencies and starts both servers)
python start_keyboard.py
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/jadenmoncy/predictive-keyboard.git
cd predictive-keyboard
```

### Step 2: Install Python Dependencies
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Install React Dependencies
```bash
cd predictive-keyboard-frontend
npm install
cd ..
```

### Step 4: Train the Model (Optional)
```bash
# The model is pre-trained, but you can retrain with your own data
python train_predictive_keyboard_model.py
```

### Step 5: Start the Application
```bash
# Option 1: Use the startup script
python start_keyboard.py

# Option 2: Manual start
# Terminal 1 - Backend
python app.py

# Terminal 2 - Frontend
cd predictive-keyboard-frontend
npm start
```

## Usage

### Basic Typing
1. **Open the application** in your browser
2. **Start typing** using the virtual keyboard or your physical keyboard
3. **View suggestions** that appear above the keyboard
4. **Click on suggestions** to auto-complete words
5. **Continue typing** - the interface adapts to your input

### Keyboard Shortcuts
| Key | Function |
|-----|----------|
| `Shift` | Toggle uppercase for next character |
| `Caps Lock` | Toggle uppercase mode |
| `Backspace` | Delete last character |
| `Space` | Add space |
| `Enter` | Add new line |

### Mobile Usage
- **Touch the virtual keys** to type
- **Swipe horizontally** through suggestions if needed
- **Tap suggestions** to auto-complete
- **Use your device keyboard** as an alternative

### Advanced Features
- **Partial word completion**: Type "hel" and see "hello", "help", etc.
- **Context-aware predictions**: Suggestions based on your current text
- **Real-time updates**: Suggestions change as you type

## API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### GET `/health`
Check API health and model status.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "tokenizer_loaded": true
}
```

#### POST `/autocomplete`
Get word suggestions for autocomplete.

**Request:**
```json
{
  "seed": "hello wor",
  "top_n": 5
}
```

**Response:**
```json
{
  "suggestions": ["world", "work", "word", "worry", "worth"]
}
```

#### POST `/predict`
Predict next word in a sequence.

**Request:**
```json
{
  "seed": "hello world",
  "n_words": 3
}
```

**Response:**
```json
{
  "prediction": "hello world how are you"
}
```

### Error Handling
All endpoints return appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (invalid input)
- `500`: Server error

## Architecture

### Frontend (React)
```
predictive-keyboard-frontend/
├── src/
│   ├── App.js              # Main React component
│   ├── App.css             # Modern styling with CSS3
│   └── index.js            # React entry point
├── public/
│   └── index.html          # HTML template
└── package.json            # Dependencies
```

### Backend (Flask)
```
├── app.py                          # Main Flask application
├── train_predictive_keyboard_model.py  # Model training script
├── predictive_keyboard_model.h5    # Trained LSTM model
├── tokenizer.pkl                   # Word tokenizer
├── large_corpus.txt               # Training data
└── templates/
    └── index.html                 # Simple HTML interface
```

### Machine Learning Model
- **Architecture**: LSTM (Long Short-Term Memory) neural network
- **Input**: Word sequences from text corpus
- **Output**: Probability distribution over vocabulary
- **Training Data**: Literary text (Sherlock Holmes corpus)
- **Model Size**: ~18MB (compressed)

### Technology Stack
- **Frontend**: React 18, CSS3, JavaScript ES6+
- **Backend**: Flask, TensorFlow/Keras, NumPy
- **ML**: LSTM neural network, word tokenization
- **Styling**: Modern CSS with gradients, animations, responsive design




---