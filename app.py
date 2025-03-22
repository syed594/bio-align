import webbrowser
from threading import Timer
import signal
import sys

# Import necessary libraries
from flask import Flask, render_template, request
from Bio.Align import PairwiseAligner
import matplotlib.pyplot as plt
import os

# Initialize the Flask app
app = Flask(__name__)

# Ensure the static folder exists
if not os.path.exists('static'):
    os.makedirs('static')

# Function to visualize alignment
def visualize_alignment(seq1, seq2, alignment):
    plt.figure(figsize=(10, 4))
    plt.title("Sequence Alignment")
    plt.xlabel("Sequence Position")
    plt.ylabel("Sequences")
    plt.text(0.5, 0.6, seq1, fontsize=12, ha='center')
    plt.text(0.5, 0.4, alignment, fontsize=12, ha='center')
    plt.text(0.5, 0.2, seq2, fontsize=12, ha='center')
    image_path = os.path.join('static', 'alignment.png')
    plt.savefig(image_path)
    plt.close()
    return image_path

# Define the home page route
@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    image_url = None
    if request.method == "POST":
        # Get user input from the form
        seq1 = request.form.get("seq1", "")
        seq2 = request.form.get("seq2", "")
        algorithm = request.form.get("algorithm", "global")
        
        # Perform alignment
        try:
            aligner = PairwiseAligner()
            aligner.mode = algorithm
            alignments = aligner.align(seq1, seq2)
            result = str(alignments[0])
            
            # Generate visualization
            image_url = visualize_alignment(seq1, seq2, result)
        except Exception as e:
            result = f"An error occurred: {e}"
    
    # Render the home page with the result and image
    return render_template("index.html", result=result, image_url=image_url)

# Function to open the browser automatically
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

# Function to handle Ctrl + C
def signal_handler(sig, frame):
    print("\nShutting down the server...")
    sys.exit(0)

# Register the signal handler for Ctrl + C
signal.signal(signal.SIGINT, signal_handler)

# Run the app
if __name__ == "__main__":
    # Open the browser after 1 second
    Timer(1, open_browser).start()
    app.run(host="0.0.0.0", port=5000, debug=True)