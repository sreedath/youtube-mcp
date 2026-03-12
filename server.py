import os
from mcp.server.fastmcp import FastMCP
from youtube_tools import get_transcript
from llm_utils import ask_llm

mcp = FastMCP(
    "YouTube Lecture MCP",
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 8000)),
)


# --- TOOLS (model-controlled actions) ---

@mcp.tool()
def get_video_transcript(video_url: str) -> str:
    """Fetch the transcript of a YouTube video."""
    return get_transcript(video_url)


@mcp.tool()
def summarize_video(video_url: str, provider: str = "openai", api_key: str = "") -> str:
    """Summarize a YouTube video in 5 concise sentences."""
    transcript = get_transcript(video_url)
    return ask_llm(
        f"Summarize the following lecture transcript in 5 concise sentences.\n\n"
        f"Transcript:\n{transcript}",
        provider, api_key,
    )


@mcp.tool()
def extract_key_points(video_url: str, provider: str = "openai", api_key: str = "") -> str:
    """Extract 5 key bullet points from a YouTube video."""
    transcript = get_transcript(video_url)
    return ask_llm(
        f"Extract the main key points from the following lecture transcript. "
        f"Return 5 bullet points.\n\nTranscript:\n{transcript}",
        provider, api_key,
    )


@mcp.tool()
def generate_notes(video_url: str, provider: str = "openai", api_key: str = "") -> str:
    """Convert a YouTube video into structured lecture notes."""
    transcript = get_transcript(video_url)
    return ask_llm(
        f"Convert the following lecture transcript into structured lecture notes. "
        f"Organize it with headings and short explanations.\n\nTranscript:\n{transcript}",
        provider, api_key,
    )


# --- RESOURCES (read-only data) ---

@mcp.resource("transcript://{video_url}")
def read_transcript(video_url: str) -> str:
    """Read a YouTube video's transcript as a resource."""
    return get_transcript(video_url)


# --- PROMPTS (reusable prompt templates) ---

@mcp.prompt()
def summarize(video_url: str) -> str:
    """Summarize a YouTube video in 5 concise sentences."""
    transcript = get_transcript(video_url)
    return (
        f"Summarize the following lecture transcript in 5 concise sentences.\n\n"
        f"Transcript:\n{transcript}"
    )


@mcp.prompt()
def key_points(video_url: str) -> str:
    """Extract 5 key bullet points from a YouTube video."""
    transcript = get_transcript(video_url)
    return (
        f"Extract the main key points from the following lecture transcript. "
        f"Return 5 bullet points.\n\nTranscript:\n{transcript}"
    )


@mcp.prompt()
def lecture_notes(video_url: str) -> str:
    """Convert a YouTube video into structured lecture notes."""
    transcript = get_transcript(video_url)
    return (
        f"Convert the following lecture transcript into structured lecture notes. "
        f"Organize it with headings and short explanations.\n\nTranscript:\n{transcript}"
    )


if __name__ == "__main__":
    mcp.run(transport="sse")
