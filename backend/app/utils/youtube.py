from urllib.parse import urlparse, parse_qs

def extract_video_id(url: str) -> str:
    """Extract the YouTube video ID from a URL."""

    parsed = urlparse(url)

    if parsed.hostname == "youtu.be":
        return parsed.path.lstrip("/")

    if parsed.hostname in ("www.youtube.com", "youtube.com"):
        return parse_qs(parsed.query).get("v", [""])[0]

    raise ValueError("Invalid YouTube URL")