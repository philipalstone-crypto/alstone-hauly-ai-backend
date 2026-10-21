# Alstone Hauly AI Backend

A small Flask API that connects a frontend chat page to the OpenAI Responses API.

## Files
- `app.py`: backend endpoints
- `requirements.txt`: Python dependencies
- `render.yaml`: Render deployment configuration
- `.gitignore`: avoids committing local secrets

## Endpoints
- `GET /` — service information
- `GET /health` — health check
- `POST /chat` — sends a message to the AI

Example request:
```json
{"message": "Explain Python variables simply"}
```

Example response:
```json
{"reply": "A variable is a named place to store a value..."}
```

## Important security notes
- Never put your OpenAI API key in frontend HTML/JavaScript or commit it to GitHub.
- Add `OPENAI_API_KEY` as a secret environment variable in Render.
- Set `FRONTEND_ORIGIN` to your deployed frontend origin, for example `https://your-site.netlify.app` (no trailing slash).
- The API uses a basic per-IP rate limit. Before a public launch, consider stronger abuse prevention and usage monitoring.
- API usage may incur charges; check your OpenAI API billing and usage limits.

## Run locally
Install packages:
```bash
pip install -r requirements.txt
```
Set environment variables in your terminal (do not paste the key into public code):
```bash
export OPENAI_API_KEY="your_api_key"
export OPENAI_MODEL="gpt-5.5"
python app.py
```
Then check `http://127.0.0.1:5000/health`.

## Deploy on Render
1. Upload these files to a GitHub repository.
2. In Render, create a new Web Service connected to that repository.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Add environment variables `OPENAI_API_KEY`, `OPENAI_MODEL` (`gpt-5.5`), and `FRONTEND_ORIGIN` (your website URL).
6. Deploy, then open `/health` on your Render service URL.
