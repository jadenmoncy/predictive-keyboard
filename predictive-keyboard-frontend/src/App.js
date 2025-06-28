import React, { useState, useEffect, useRef } from 'react';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [cursorPosition, setCursorPosition] = useState(0);
  const [isShiftPressed, setIsShiftPressed] = useState(false);
  const [isCapsLock, setIsCapsLock] = useState(false);
  const textAreaRef = useRef(null);
  const suggestionRef = useRef(null);

 
  const keyboardLayout = [
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
    ['z', 'x', 'c', 'v', 'b', 'n', 'm']
  ];


  const specialKeys = {
    backspace: '⌫',
    space: 'space',
    enter: '↵',
    shift: '⇧',
    caps: '⇪'
  };

  useEffect(() => {
    fetchSuggestions(text);
  }, [text]);

  const fetchSuggestions = async (currentText) => {
    if (!currentText.trim()) {
      setSuggestions([]);
      return;
    }
    
    try {
      const response = await fetch('http://127.0.0.1:5001/autocomplete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ seed: currentText, top_n: 5 })
      });
      const data = await response.json();
      setSuggestions(data.suggestions || []);
    } catch (error) {
      console.error('Error fetching suggestions:', error);
      setSuggestions([]);
    }
  };

  const handleSuggestionClick = (word) => {
    const words = text.split(' ');
    const lastWordIndex = words.length - 1;
    
    if (lastWordIndex >= 0) {
      words[lastWordIndex] = word;
      const newText = words.join(' ') + ' ';
      setText(newText);
      setCursorPosition(newText.length);
    }
    
    if (textAreaRef.current) {
      textAreaRef.current.focus();
    }
  };

  const handleKeyPress = (key) => {
    if (key === specialKeys.backspace) {
      if (text.length > 0) {
        const newText = text.slice(0, -1);
        setText(newText);
        setCursorPosition(newText.length);
      }
    } else if (key === specialKeys.space) {
      const newText = text + ' ';
      setText(newText);
      setCursorPosition(newText.length);
    } else if (key === specialKeys.enter) {
      const newText = text + '\n';
      setText(newText);
      setCursorPosition(newText.length);
    } else if (key === specialKeys.shift) {
      setIsShiftPressed(!isShiftPressed);
    } else if (key === specialKeys.caps) {
      setIsCapsLock(!isCapsLock);
      setIsShiftPressed(false);
    } else {
      const letter = isShiftPressed || isCapsLock ? key.toUpperCase() : key.toLowerCase();
      const newText = text + letter;
      setText(newText);
      setCursorPosition(newText.length);
      

      if (isShiftPressed) {
        setIsShiftPressed(false);
      }
    }


    if (textAreaRef.current) {
      textAreaRef.current.focus();
    }
  };

  const handleTextAreaChange = (e) => {
    setText(e.target.value);
    setCursorPosition(e.target.selectionStart);
  };

  const handleTextAreaClick = (e) => {
    setCursorPosition(e.target.selectionStart);
  };

  const handleTextAreaKeyDown = (e) => {
    setCursorPosition(e.target.selectionStart);
  };

  return (
    <div className="keyboard-app">
      <div className="header">
        <h1>Predictive Keyboard</h1>
      </div>
      
      <div className="text-container">
        <textarea
          ref={textAreaRef}
          value={text}
          onChange={handleTextAreaChange}
          onClick={handleTextAreaClick}
          onKeyDown={handleTextAreaKeyDown}
          placeholder="Start typing..."
          className="text-area"
          rows={6}
        />
      </div>

      {/* Suggestions Bar */}
      {suggestions.length > 0 && (
        <div className="suggestions-bar" ref={suggestionRef}>
          {suggestions.map((word, index) => (
            <button
              key={index}
              className="suggestion-button"
              onClick={() => handleSuggestionClick(word)}
            >
              {word}
            </button>
          ))}
        </div>
      )}

      {/* Virtual Keyboard */}
      <div className="keyboard">
        {/* First Row */}
        <div className="keyboard-row">
          {keyboardLayout[0].map((key) => (
            <button
              key={key}
              className="key"
              onClick={() => handleKeyPress(key)}
            >
              {isShiftPressed || isCapsLock ? key.toUpperCase() : key}
            </button>
          ))}
        </div>

        {/* Second Row */}
        <div className="keyboard-row">
          <div className="keyboard-row-left">
            {keyboardLayout[1].map((key) => (
              <button
                key={key}
                className="key"
                onClick={() => handleKeyPress(key)}
              >
                {isShiftPressed || isCapsLock ? key.toUpperCase() : key}
              </button>
            ))}
          </div>
        </div>

        {/* Third Row */}
        <div className="keyboard-row">
          <button
            className="key special-key"
            onClick={() => handleKeyPress(specialKeys.shift)}
          >
            {specialKeys.shift}
          </button>
          {keyboardLayout[2].map((key) => (
            <button
              key={key}
              className="key"
              onClick={() => handleKeyPress(key)}
            >
              {isShiftPressed || isCapsLock ? key.toUpperCase() : key}
            </button>
          ))}
          <button
            className="key special-key"
            onClick={() => handleKeyPress(specialKeys.backspace)}
          >
            {specialKeys.backspace}
          </button>
        </div>

        {/* Fourth Row - Space and Enter */}
        <div className="keyboard-row">
          <button
            className="key special-key caps-key"
            onClick={() => handleKeyPress(specialKeys.caps)}
          >
            {specialKeys.caps}
          </button>
          <button
            className="key space-key"
            onClick={() => handleKeyPress(specialKeys.space)}
          >
            {specialKeys.space}
          </button>
          <button
            className="key special-key enter-key"
            onClick={() => handleKeyPress(specialKeys.enter)}
          >
            {specialKeys.enter}
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;