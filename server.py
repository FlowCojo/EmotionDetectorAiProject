from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")

# Defining the route /emotionDetector for emotion detection
@app.route('/emotionDetector', methods=['POST'])
def detect_emotion():
    # Parsing the request JSON payload
    request_data = request.get_json()
    
    # Ensuring 'text' key exists in the request payload
    if 'text' not in request_data:
        return "Error: The request payload must contain 'text' field.", 400
    
    text_to_analyze = request_data['text']
    
    # Calling the emotion_detector function with the given text
    result = emotion_detector(text_to_analyze)

    # If the result is a dictionary, format the response in the desired way
    if isinstance(result, dict):
        response_text = (
            f"For the given statement, the system response is "
            f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
            f"'fear': {result['fear']}, 'joy': {result['joy']} and "
            f"'sadness': {result['sadness']}. The dominant emotion is {result['dominant_emotion']}."
        )
        return response_text
    else:
        # Return any error message as JSON response
        return jsonify({"error": result})

@app.route("/")
def render_index_page():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5002, debug=True)
