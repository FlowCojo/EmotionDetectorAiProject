import requests
import json

def emotion_detector(text_to_analyze):
    # Define the URL and headers for the API request
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
        "Content-Type": "application/json"
    }
    
    # Handle blank input
    if not text_to_analyze.strip():
        # Return a dictionary with all None values for blank input
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    
    # Define the JSON structure of the request payload
    input_json = {
        "raw_document": {
            "text": text_to_analyze
        }
    }
    
    # Send the POST request to the API
    response = requests.post(url, json=input_json, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Convert the API response into a Python dictionary
        response_dict = response.json()
                
        # Check if 'emotionPredictions' key is in the response
        if 'emotionPredictions' in response_dict:
            # Extract the first item in 'emotionPredictions' list
            emotion_prediction = response_dict['emotionPredictions'][0]
            
            # Extract the 'emotion' dictionary from 'emotionPredictions'
            if 'emotion' in emotion_prediction:
                emotions = emotion_prediction['emotion']
                
                # Extract individual emotion scores
                anger_score = emotions.get('anger', 0)
                disgust_score = emotions.get('disgust', 0)
                fear_score = emotions.get('fear', 0)
                joy_score = emotions.get('joy', 0)
                sadness_score = emotions.get('sadness', 0)

                # Find the dominant emotion by comparing the scores
                emotion_scores = {
                    'anger': anger_score,
                    'disgust': disgust_score,
                    'fear': fear_score,
                    'joy': joy_score,
                    'sadness': sadness_score
                }

                dominant_emotion = max(emotion_scores, key=emotion_scores.get)

                # Return the structured output format with scores and dominant emotion
                return {
                    'anger': anger_score,
                    'disgust': disgust_score,
                    'fear': fear_score,
                    'joy': joy_score,
                    'sadness': sadness_score,
                    'dominant_emotion': dominant_emotion
                }
            else:
                return "Emotion key not found in emotionPredictions."
        else:
            return "EmotionPredictions not found in response."

    # Handle status code 400 - Bad Request (e.g., server did not accept input)
    elif response.status_code == 400:
        # Return a dictionary with all None values for a bad request
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    else:
        # If the request failed, return an error message
        return f'Request failed with status code {response.status_code}: {response.text}'
