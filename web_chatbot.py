from flask import Flask, request, jsonify, render_template, session
import random
import pyttsx3
from speech_recognition import listen, speak

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for sessions


## Predefined responses with lists for random replies
RESPONSES = {
    "greetings": ["Hello there!", "Hey! How's it going?", "Hi! Great to see you!"],
    "how are you": ["I'm doing great! How about you?", "I'm just code, but I'm happy to chat!", "Fantastic! And you?"],
    "what's your name": ["I'm your AI companion.", "You can call me your buddy.", "I don't have a name yet! Want to give me one?"],
    "bye": ["Goodbye! Have an amazing day!", "See you later, friend!", "Bye-bye! Stay awesome!"],
    "default": ["I'm not sure I understand.", "Tell me more!", "Interesting... Can you explain that?"]
}

KEYWORDS = {
    "greetings" : ["hello", "hi", "hey"],
    "how are you": ["how are you", "how do you do"],
    "what's your name": ["what's your name", "who are you", "what are you"]
}

MOOD_RESPONSES = {
    "happy": ["I'm glad you're feeling happy! 😊", "That's awesome! Keep smiling! 😄"],
    "sad": ["I'm sorry you're feeling down. 😢 Anything I can do to help?", "It's okay to feel sad sometimes. I'm here for you! 💙"],
    "angry": ["I'm sorrys you're upset. Let's take a deep breath together. 🧘‍♂️", "Take it easy, everything will be alright!"],
    "neutral": ["I hope everything's going well with you.", "What's on your mind?"]
}

def get_response(message):
    for category, synonyms in KEYWORDS.items():
        if any(keyword in message for keyword in synonyms):  # Match keywords
            return random.choice(RESPONSES[category])
    return random.choice(RESPONSES["default"])

@app.route('/')
def home():
    return render_template('chat.html')

# Define a route for chatting
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")  # Get the user's message from the request

    # Handle mood-based responses
    if "feeling" in user_message.lower():
        if "happy" in user_message.lower():
            return jsonify({"reply": random.choice(MOOD_RESPONSES["happy"])})
        elif "sad" in user_message.lower():
            return jsonify({"reply": random.choice(MOOD_RESPONSES["sad"])})
        elif "angry" in user_message.lower():
            return jsonify({"reply": random.choice(MOOD_RESPONSES["angry"])})
        else:
            return jsonify({"reply": random.choice(MOOD_RESPONSES["neutral"])})
    
    # Save user's name if they share it
    if "my name is" in user_message.lower():
        name = user_message.split("my name is")[-1].strip()
        session['name'] = name
        return jsonify({"reply": f"Got it, {name}! How can I assist you?"})

    # Check for user's name in session
    if 'name' in session:
        name = session['name']
        if "what is my name" in user_message.lower():
            return jsonify({"reply": f"Your name is {name}, right?"})


    response = get_response(user_message)
    return jsonify({"reply": response})  # Return the AI's response as JSON
    

@app.route('/listen', methods=['GET'])
def listen_to_user():
    # Simulate AI response
    response = {
        "reply": "Hello, how can I help you today?"
    }
    return jsonify(response)
    # Listen to the user's speech
    user_message = listen()
    if user_message:
        response = get_response(user_message)
        speak(response)  # AI speaks the response
        return jsonify({"reply": response})
    return jsonify({"reply": "Sorry, I couldn't hear you."})

if __name__ == "__main__":
    app.run(debug=True)