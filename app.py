from flask import Flask, request, jsonify, render_template_string
from youtube_tools import get_transcript
from llm_utils import ask_llm

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>YouTube Lecture Assistant</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, sans-serif; background: #0f0f0f; color: #fff; min-height: 100vh; display: flex; justify-content: center; padding: 40px 20px; }
        .container { max-width: 700px; width: 100%; }
        h1 { font-size: 28px; margin-bottom: 8px; }
        .subtitle { color: #aaa; margin-bottom: 30px; }
        input[type=text] { width: 100%; padding: 14px; border-radius: 8px; border: 1px solid #333; background: #1a1a1a; color: #fff; font-size: 16px; margin-bottom: 20px; }
        input[type=text]::placeholder { color: #666; }
        .buttons { display: flex; gap: 10px; margin-bottom: 30px; flex-wrap: wrap; }
        button { padding: 12px 24px; border-radius: 8px; border: none; font-size: 15px; font-weight: 600; cursor: pointer; background: #2563eb; color: #fff; transition: background 0.2s; }
        button:hover { background: #1d4ed8; }
        button:disabled { background: #333; cursor: not-allowed; }
        .result { background: #1a1a1a; border: 1px solid #333; border-radius: 8px; padding: 20px; white-space: pre-wrap; line-height: 1.7; min-height: 60px; }
        .loading { color: #aaa; font-style: italic; }
    </style>
</head>
<body>
    <div class="container">
        <h1>YouTube Lecture Assistant</h1>
        <p class="subtitle">Paste a YouTube URL to get a summary, key points, or structured notes.</p>
        <input type="text" id="url" placeholder="https://www.youtube.com/watch?v=...">
        <div class="buttons">
            <button onclick="run('summarize')">Summarize</button>
            <button onclick="run('keypoints')">Key Points</button>
            <button onclick="run('notes')">Lecture Notes</button>
        </div>
        <div class="result" id="result">Results will appear here...</div>
    </div>
    <script>
        async function run(action) {
            const url = document.getElementById('url').value.trim();
            if (!url) { alert('Please enter a YouTube URL'); return; }
            const result = document.getElementById('result');
            result.innerHTML = '<span class="loading">Processing... this may take a moment.</span>';
            document.querySelectorAll('button').forEach(b => b.disabled = true);
            try {
                const res = await fetch('/api/' + action, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: url})
                });
                const data = await res.json();
                result.textContent = data.error || data.result;
            } catch (e) {
                result.textContent = 'Error: ' + e.message;
            }
            document.querySelectorAll('button').forEach(b => b.disabled = false);
        }
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/api/summarize", methods=["POST"])
def summarize():
    video_url = request.json["url"]
    transcript = get_transcript(video_url)
    result = ask_llm(
        f"Summarize the following lecture transcript in 5 concise sentences.\n\n"
        f"Transcript:\n{transcript}"
    )
    return jsonify({"result": result})


@app.route("/api/keypoints", methods=["POST"])
def keypoints():
    video_url = request.json["url"]
    transcript = get_transcript(video_url)
    result = ask_llm(
        f"Extract the main key points from the following lecture transcript. "
        f"Return 5 bullet points.\n\nTranscript:\n{transcript}"
    )
    return jsonify({"result": result})


@app.route("/api/notes", methods=["POST"])
def notes():
    video_url = request.json["url"]
    transcript = get_transcript(video_url)
    result = ask_llm(
        f"Convert the following lecture transcript into structured lecture notes. "
        f"Organize it with headings and short explanations.\n\nTranscript:\n{transcript}"
    )
    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True, port=8000)
