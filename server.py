"""
This module implements a Flask web server for emotion detection.
It defines two main routes: `/emotionDetector` for emotion analysis 
and `/` for rendering the index page.
"""

from flask import Flask, render_template, request, jsonify
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")

@app.route('/emotionDetector', methods=['GET', 'POST'])
def detect_emotion():
    """
    Handles the route for emotion detection.
    Allows both GET and POST methods for text input analysis to detect emotions.

    GET:
        Takes 'textToAnalyze' as a query parameter and returns the emotion analysis.

    POST:
        Accepts a JSON payload with 'text' key and returns the emotion analysis.
    """

    result = None  # Initialize result to avoid possibly using it before assignment

    # Handle GET request (e.g., from JavaScript function)
    if request.method == 'GET':
        # Extract 'textToAnalyze' from query parameters
        text_to_analyze = request.args.get('textToAnalyze')
        # Handle empty or missing text
        if not text_to_analyze or not text_to_analyze.strip():
            return "Invalid text! Please try again.", 400

        # Call the emotion_detector function with the given text
        result = emotion_detector(text_to_analyze)

    # Handle POST request (potential future support)
    elif request.method == 'POST':
        # Parsing the request JSON payload
        request_data = request.get_json()
        # Ensure 'text' key exists in the request payload
        if 'text' not in request_data:
            return "Error: The request payload must contain 'text' field.", 400

        text_to_analyze = request_data['text']
        # Handle empty or missing text
        if not text_to_analyze or not text_to_analyze.strip():
            return "Invalid text! Please try again.", 400

        # Call the emotion_detector function with the given text
        result = emotion_detector(text_to_analyze)

    # If the result is a dictionary, format the response
    if isinstance(result, dict):
        # Check if the dominant emotion is None
        if result['dominant_emotion'] is None:
            return "Invalid text! Please try again.", 400
        # Construct the response text
        response_text = (
            f"For the given statement, the system response is "
            f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
            f"'fear': {result['fear']}, 'joy': {result['joy']}, and "
            f"'sadness': {result['sadness']}. The dominant emotion is {result['dominant_emotion']}."
        )
        return response_text

    # Return any error message from emotion_detector as a response
    return jsonify({"error": result})

@app.route("/")
def render_index_page():
    """
    Renders the index page of the application.
    """
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003)
