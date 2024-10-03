from flask import Flask, render_template, request, jsonify
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")

# Defining the route /emotionDetector for emotion detection, allowing both GET and POST methods
@app.route('/emotionDetector', methods=['GET', 'POST'])
def detect_emotion():
    # Handle GET request (from JavaScript function)
    if request.method == 'GET':
        # Extract 'textToAnalyze' from query parameters
        text_to_analyze = request.args.get('textToAnalyze')
        
        if not text_to_analyze:
            return "Error: No text provided for analysis. Please provide a valid input.", 400
        
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
        
        # Call the emotion_detector function with the given text
        result = emotion_detector(text_to_analyze)

    # If the result is a dictionary, format the response
    if isinstance(result, dict):
        if result['dominant_emotion'] is None:
            return "Invalid text! Please try again."
        
        response_text = (
            f"For the given statement, the system response is "
            f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
            f"'fear': {result['fear']}, 'joy': {result['joy']}, and "
            f"'sadness': {result['sadness']}. The dominant emotion is {result['dominant_emotion']}."
        )
        return response_text
    else:
        # Return any error message from emotion_detector as a response
        return jsonify({"error": result})

@app.route("/")
def render_index_page():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
