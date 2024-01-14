from flask import Flask, render_template, request

import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key="AIzaSyAvDQjTto-gFHfGNw2uA_Nf8Xaf9MLr1Pg")

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.form['user_question']

    if user_question.lower() == 'q':
        return render_template('index.html', response="Çıkıldı")

    convo = model.start_chat(
        history=[
            {"role": "user", "parts": ["sen kimsin ve neler yapabilirsin"]},
            {"role": "model", "parts": ["..."]},
            {"role": "user", "parts": ["sorularıma risale nur dan alıntı yaparak yanıt vereceksin"]},
            {"role": "model", "parts": ["tamam"]},
            {"role": "user", "parts": ["sorularıma sorularla islamiyet sitesinden faydalanarak yanıtlar vereceksin"]},
            {"role": "model", "parts": ["tamam"]},
        ]
    )

    convo.send_message(user_question)
    response = convo.last.text
    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
