import logging

from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.youtube import TranscriptFormat
from langchain_core.documents import Document

from config import SUPPORTED_LANGUAGES

logger = logging.getLogger(__name__)

class TranscriptLoadingError(Exception):
    """Raised when YouTube transcript loading fails."""
    pass

class TranscriptLoader:
    """Service for loading YouTube transcripts."""
    
    def load_transcript(self, youtube_url: str) -> list[Document]:
        """
        Load the transcript of a YouTube video.

        Args:
            youtube_url: Full YouTube video URL.

        Returns:
            A list of LangChain Document objects.

        Raises:
            TranscriptLoadingError: If the transcript cannot be loaded.
        """
        
        loader = YoutubeLoader.from_youtube_url(
            youtube_url=youtube_url,
            add_video_info=False,
            language=SUPPORTED_LANGUAGES,
            transcript_format = TranscriptFormat.TEXT
        )
        try:
            return loader.load()
        except Exception as e:
            logger.exception("Failed to load transcript")
            raise TranscriptLoadingError(
                f"Could not load transcript for {youtube_url}"
            ) from e