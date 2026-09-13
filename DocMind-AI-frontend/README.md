# DocMind AI Frontend

A modern frontend for the DocMind AI RAG project.

## Files

- `index.html` — main UI
- `style.css` — responsive styling
- `script.js` — chat and FastAPI connection

## Run

Open `index.html` in a browser.

For best results, serve it with a local server:

```powershell
python -m http.server 5500
```

Then open:

http://127.0.0.1:5500

## Backend expected

The frontend currently expects:

```text
POST http://127.0.0.1:8000/ask
```

Request:

```json
{
  "question": "What is machine learning?"
}
```

Example response:

```json
{
  "answer": "Machine learning is ...",
  "sources": ["sample.pdf - page 2"]
}
```

Your current Python RAG code is terminal-based and uses `input()`. The next step is to convert that RAG logic into a FastAPI `/ask` endpoint so this frontend can talk to it.

The upload panel is already designed in the UI; PDF upload can be connected to a `/upload` endpoint after the `/ask` endpoint.
