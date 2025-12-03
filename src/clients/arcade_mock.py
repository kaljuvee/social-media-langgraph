"""Mock Arcade client for development and testing."""

from typing import Optional, Dict, Any


class ArcadeMockClient:
    """Mock Arcade client for development."""

    def __init__(self):
        """Initialize the mock Arcade client."""
        self.user_id = None
        self.authenticated = False

    async def authenticate_twitter(self) -> Optional[Dict[str, Any]]:
        """Mock Twitter authentication."""
        self.authenticated = True
        return {"token": "mock_token", "user_id": "mock_user"}

    async def authenticate_linkedin(self) -> Optional[Dict[str, Any]]:
        """Mock LinkedIn authentication."""
        self.authenticated = True
        return {"token": "mock_token", "user_id": "mock_user"}

    async def post_to_twitter(self, content: str, media_urls: Optional[list] = None) -> Optional[str]:
        """Mock Twitter post."""
        return f"mock_tweet_{hash(content) % 1000}"

    async def post_to_linkedin(self, content: str, media_urls: Optional[list] = None) -> Optional[str]:
        """Mock LinkedIn post."""
        return f"mock_linkedin_{hash(content) % 1000}"

    async def schedule_post(
        self,
        platform: str,
        content: str,
        scheduled_time: str,
        media_urls: Optional[list] = None
    ) -> Optional[str]:
        """Mock schedule post."""
        return f"mock_scheduled_{hash(content) % 1000}"
