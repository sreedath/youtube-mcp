"use client";
import { useState, useEffect } from "react";

export default function Home() {
  const [url, setUrl] = useState("");
  const [provider, setProvider] = useState("openai");
  const [apiKey, setApiKey] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setProvider(localStorage.getItem("provider") || "openai");
    setApiKey(localStorage.getItem("api_key") || "");
  }, []);

  function saveSettings(newProvider: string, newKey: string) {
    setProvider(newProvider);
    setApiKey(newKey);
    localStorage.setItem("provider", newProvider);
    localStorage.setItem("api_key", newKey);
  }

  async function callTool(tool: string) {
    if (!url.trim()) return;
    if (!apiKey.trim() && tool !== "get_video_transcript") {
      setResult("Please enter your API key above.");
      return;
    }
    setLoading(true);
    setResult("");
    const res = await fetch("/api/tool", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tool, video_url: url, provider, api_key: apiKey }),
    });
    const data = await res.json();
    setResult(data.error || data.result);
    setLoading(false);
  }

  return (
    <main style={{ maxWidth: 700, margin: "60px auto", padding: "0 20px", fontFamily: "system-ui, sans-serif" }}>
      <h1>YouTube Lecture Assistant</h1>
      <p style={{ color: "#666", marginBottom: 24 }}>Paste a YouTube URL and pick an action.</p>

      <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
        <select
          value={provider}
          onChange={(e) => saveSettings(e.target.value, apiKey)}
          style={{ padding: 10, borderRadius: 8, border: "1px solid #ccc", fontSize: 14 }}
        >
          <option value="openai">OpenAI</option>
          <option value="gemini">Gemini</option>
        </select>
        <input
          type="password"
          value={apiKey}
          onChange={(e) => saveSettings(provider, e.target.value)}
          placeholder={provider === "openai" ? "sk-..." : "AIza..."}
          style={{ flex: 1, padding: 10, borderRadius: 8, border: "1px solid #ccc", fontSize: 14 }}
        />
      </div>

      <input
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="https://www.youtube.com/watch?v=..."
        style={{ width: "100%", padding: 12, fontSize: 16, borderRadius: 8, border: "1px solid #ccc", marginBottom: 16 }}
      />
      <div style={{ display: "flex", gap: 8, marginBottom: 24 }}>
        <button onClick={() => callTool("summarize_video")} disabled={loading} style={btnStyle}>Summarize</button>
        <button onClick={() => callTool("extract_key_points")} disabled={loading} style={btnStyle}>Key Points</button>
        <button onClick={() => callTool("generate_notes")} disabled={loading} style={btnStyle}>Lecture Notes</button>
        <button onClick={() => callTool("get_video_transcript")} disabled={loading} style={{ ...btnStyle, background: "#666" }}>Transcript</button>
      </div>
      <pre style={{ whiteSpace: "pre-wrap", background: "#f5f5f5", padding: 20, borderRadius: 8, minHeight: 80, lineHeight: 1.6 }}>
        {loading ? "Processing... this may take a moment." : result || "Results will appear here..."}
      </pre>
    </main>
  );
}

const btnStyle: React.CSSProperties = {
  padding: "10px 20px", borderRadius: 8, border: "none",
  background: "#2563eb", color: "#fff", fontSize: 14, fontWeight: 600, cursor: "pointer",
};
