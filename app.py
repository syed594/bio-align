import webbrowser
from threading import Timer
import signal
import sys
from flask import Flask, render_template, request, redirect, url_for
from Bio.Align import PairwiseAligner
import matplotlib.pyplot as plt
import os
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg' to avoid GUI threading issues

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

# Function to calculate alignment percentage
def calculate_alignment_percentage(seq1, seq2, alignment):
    """
    Calculate the percentage of alignment between two sequences.
    """
    matches = sum(1 for a, b in zip(seq1, seq2) if a == b)  # Count matching characters
    alignment_length = max(len(seq1), len(seq2))  # Use the longer sequence length
    percentage = (matches / alignment_length) * 100  # Calculate percentage
    return round(percentage, 2)  # Round to 2 decimal places

# Define the home page route
@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    image_url = None
    alignment_percentage = None  # Initialize alignment percentage
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
            
            # Calculate alignment percentage
            alignment_percentage = calculate_alignment_percentage(seq1, seq2, alignments[0])
            
            # Generate visualization
            image_url = visualize_alignment(seq1, seq2, result)
        except Exception as e:
            result = f"An error occurred: {e}"
    
    # Render the home page with the result, image, and alignment percentage
    return render_template("index.html", result=result, image_url=image_url, alignment_percentage=alignment_percentage)

# Route to handle feedback submissions
@app.route('/feedback', methods=['POST'])
def feedback():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    # Save feedback to a file
    with open('feedback.txt', 'a') as f:
        f.write(f"Name: {name}\nEmail: {email}\nMessage: {message}\n\n")
    
    # Redirect to the home page
    return redirect(url_for('home'))

# Route to handle suggestions
@app.route('/suggestions', methods=['POST'])
def suggestions():
    suggestion = request.form.get('suggestion')
    
    # Save suggestion to a file
    with open('suggestions.txt', 'a') as f:
        f.write(f"Suggestion: {suggestion}\n\n")
    
    # Redirect to the home page
    return redirect(url_for('home'))

# Function to open the browser automatically
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5001/")  # Updated to port 5001

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
    app.run(host="0.0.0.0", port=5001, debug=False)  # Updated to port 5001 and debug=False