from youtube_transcript_api import YouTubeTranscriptApi
import re


def extract_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")


def get_transcript(video_url):

    video_id = extract_video_id(video_url)

    transcript = YouTubeTranscriptApi().fetch(video_id)

    text = " ".join([snippet.text for snippet in transcript])

    return text