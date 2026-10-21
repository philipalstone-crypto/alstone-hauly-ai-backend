import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from openai import OpenAI, OpenAIError

app = Flask(__name__)

# Set FRONTEND_ORIGIN to your deployed website URL on Render.
# During initial testing, "*" allows requests from your frontend before its URL is known.
frontend_origin = os.getenv("FRONTEND_ORIGIN", "*")
CORS(app, resources={r"/*": {"origins": frontend_origin}})

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://",
)

MODEL = os.getenv("OPENAI_MODEL", "gpt-5.5")
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

SYSTEM_INSTRUCTIONS = """
You are Hauly, the AI assistant for Alstone Hauly AI.
Be helpful, accurate, friendly, and clear.
Help with learning, programming, writing, languages, and general questions.
When teaching beginners, explain ideas in simple steps and give safe examples.
If you are unsure, say so instead of inventing facts.
"""

@app.get("/")
def home():
    return jsonify({
        "name": "Alstone Hauly AI Backend",
        "status": "running",
        "endpoints": ["/health", "/chat"]
    })

@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "Alstone Hauly AI backend"})

@app.post("/chat")
@limiter.limit("20 per minute")
def chat():
    if client is None:
        return jsonify({
            "error": "The backend is missing its OPENAI_API_KEY environment variable."
        }), 503

    data = request.get_json(silent=True) or {}
    message = data.get("message")

    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "Please send a non-empty 'message' string."}), 400

    if len(message) > 8000:
        return jsonify({"error": "Message is too long. Keep it under 8,000 characters."}), 413

    try:
        response = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
            input=message.strip(),
            max_output_tokens=800,
        )
        return jsonify({"reply": response.output_text})
    except OpenAIError as exc:
        # Keep secret credentials and internal details out of the public response.
        app.logger.error("OpenAI API request failed: %s", type(exc).__name__)
        return jsonify({
            "error": "Hauly could not get an AI response. Check the API key, model access, and API billing, then try again."
        }), 502

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
