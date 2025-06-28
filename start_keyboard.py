import subprocess
import sys
import time
import os
import signal
from pathlib import Path

def check_dependencies():
    print("Checking dependencies.")
    
    try:
        import flask
        import tensorflow
        import numpy
        print("Python dependencies found")
    except ImportError as e:
        print(f"Missing Python dependency: {e}")
        print("Please run: pip install flask flask-cors tensorflow numpy")
        return False
    

    frontend_path = Path("predictive-keyboard-frontend")
    if not frontend_path.exists():
        print("React frontend not found")
        return False
    
    node_modules = frontend_path / "node_modules"
    if not node_modules.exists():
        print("React dependencies not installed")
        print("Please run: cd predictive-keyboard-frontend && npm install")
        return False
    
    print("React dependencies found")
    return True

def check_model_files():
    print("Checking model files.")
    
    required_files = [
        "predictive_keyboard_model.h5",
        "tokenizer.pkl",
        "large_corpus.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"Missing model files: {', '.join(missing_files)}")
        print("Please run: python train_predictive_keyboard_model.py")
        return False
    
    print("Model files found")
    return True

def start_backend():
    print("Starting Flask backend.")
    try:
        backend_process = subprocess.Popen([
            sys.executable, "app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(3)
        
        if backend_process.poll() is None:
            print("Backend server started on http://localhost:5001")
            return backend_process
        else:
            print("Backend server failed to start")
            return None
            
    except Exception as e:
        print(f"Error starting backend: {e}")
        return None

def start_frontend():
    print("Starting React frontend.")
    try:
        os.chdir("predictive-keyboard-frontend")
        
        frontend_process = subprocess.Popen([
            "npm", "start"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(5)
        

        if frontend_process.poll() is None:
            print("Frontend server started on http://localhost:3000")
            return frontend_process
        else:
            print("Frontend server failed to start")
            return None
            
    except Exception as e:
        print(f"Error starting frontend: {e}")
        return None

def main():
    print("Predictive Keyboard Startup")
    print("=" * 40)
    
    if not check_dependencies():
        sys.exit(1)
    
    if not check_model_files():
        sys.exit(1)
    
    print("\n Starting servers.")
    

    backend_process = start_backend()
    if not backend_process:
        sys.exit(1)
    

    frontend_process = start_frontend()
    if not frontend_process:
        print("Frontend failed to start, stopping backend.")
        backend_process.terminate()
        sys.exit(1)
    
    print("\n Predictive Keyboard is ready!")
    print(" Frontend: http://localhost:3000")
    print(" Backend:  http://localhost:5001")
    
    try:
        while True:
            time.sleep(1)
            
            if backend_process.poll() is not None:
                print("Backend server stopped unexpectedly")
                break
                
            if frontend_process.poll() is not None:
                print("Frontend server stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n Stopping servers...")
        
        if backend_process:
            backend_process.terminate()
            print("Backend stopped")
        
        # Stop frontend
        if frontend_process:
            frontend_process.terminate()
            print("Frontend stopped")
        
        print("Goodbye!")

if __name__ == "__main__":
    main() 