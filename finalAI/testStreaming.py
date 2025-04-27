from flask import Flask, Response, render_template_string
import google.generativeai as genai

app = Flask(__name__)

# Set your Gemini API key
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Create a Gemini model instance
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def index():
    return render_template_string('''
        <html>
            <body>
                <h1>Gemini Streaming Example</h1>
                <button onclick="startStreaming()">Start Streaming</button>
                <div id="output" style="white-space: pre-wrap; font-family: monospace; margin-top: 20px;"></div>

                <script>
                function startStreaming() {
                    const outputDiv = document.getElementById('output');
                    outputDiv.innerHTML = "";
                    fetch('/stream')
                        .then(response => {
                            const reader = response.body.getReader();
                            const decoder = new TextDecoder();
                            function read() {
                                reader.read().then(({ done, value }) => {
                                    if (done) {
                                        return;
                                    }
                                    outputDiv.innerHTML += decoder.decode(value);
                                    read();
                                });
                            }
                            read();
                        });
                }
                </script>
            </body>
        </html>
    ''')

@app.route('/stream')
def stream():
    def generate():
        response = model.start_chat().send_message(
            "Write a short story about a dragon who learns to paint.",
            stream=True  # streaming enabled
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text
    return Response(generate(), content_type='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
