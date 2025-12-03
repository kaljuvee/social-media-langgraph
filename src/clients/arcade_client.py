"""Arcade client for social media authentication and posting."""

from typing import Optional, Dict, Any
import os
from src.config import settings

# Try to import real Arcade, fall back to mock
try:
    from arcade import Arcade
    ARCADE_AVAILABLE = True
except ImportError:
    ARCADE_AVAILABLE = False
    from src.clients.arcade_mock import ArcadeMockClient as Arcade


class ArcadeClient:
    """Handles social media authentication and posting via Arcade."""

    def __init__(self):
        """Initialize the Arcade client."""
        if ARCADE_AVAILABLE:
            self.client = Arcade(api_key=settings.arcade_api_key)
        else:
            self.client = Arcade()
        self.user_id = settings.arcade_user_id

    async def authenticate_twitter(self) -> Optional[Dict[str, Any]]:
        """
        Authenticate with Twitter via Arcade.

        Returns:
            Authentication token or None if authentication fails
        """
        try:
            # Arcade handles authentication flow
            result = await self.client.authenticate("twitter", user_id=self.user_id)
            return result
        except Exception as e:
            print(f"Error authenticating with Twitter: {str(e)}")
            return None

    async def authenticate_linkedin(self) -> Optional[Dict[str, Any]]:
        """
        Authenticate with LinkedIn via Arcade.

        Returns:
            Authentication token or None if authentication fails
        """
        try:
            result = await self.client.authenticate("linkedin", user_id=self.user_id)
            return result
        except Exception as e:
            print(f"Error authenticating with LinkedIn: {str(e)}")
            return None

    async def post_to_twitter(self, content: str, media_urls: Optional[list] = None) -> Optional[str]:
        """
        Post content to Twitter.

        Args:
            content: The post content
            media_urls: Optional list of media URLs to attach

        Returns:
            Post ID or None if posting fails
        """
        try:
            result = await self.client.post(
                "twitter",
                user_id=self.user_id,
                content=content,
                media_urls=media_urls or []
            )
            return result.get("id")
        except Exception as e:
            print(f"Error posting to Twitter: {str(e)}")
            return None

    async def post_to_linkedin(self, content: str, media_urls: Optional[list] = None) -> Optional[str]:
        """
        Post content to LinkedIn.

        Args:
            content: The post content
            media_urls: Optional list of media URLs to attach

        Returns:
            Post ID or None if posting fails
        """
        try:
            result = await self.client.post(
                "linkedin",
                user_id=self.user_id,
                content=content,
                media_urls=media_urls or [],
                organization_id=settings.linkedin_organization_id if settings.post_to_linkedin_organization else None
            )
            return result.get("id")
        except Exception as e:
            print(f"Error posting to LinkedIn: {str(e)}")
            return None

    async def schedule_post(
        self,
        platform: str,
        content: str,
        scheduled_time: str,
        media_urls: Optional[list] = None
    ) -> Optional[str]:
        """
        Schedule a post for later.

        Args:
            platform: The social media platform (twitter, linkedin)
            content: The post content
            scheduled_time: ISO format datetime string
            media_urls: Optional list of media URLs to attach

        Returns:
            Scheduled post ID or None if scheduling fails
        """
        try:
            result = await self.client.schedule_post(
                platform,
                user_id=self.user_id,
                content=content,
                scheduled_time=scheduled_time,
                media_urls=media_urls or []
            )
            return result.get("id")
        except Exception as e:
            print(f"Error scheduling post: {str(e)}")
            return None


# Global Arcade client instance
arcade_client = ArcadeClient()
