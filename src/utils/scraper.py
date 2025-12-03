"""Web scraping utilities for extracting content from URLs."""

import httpx
from typing import Optional, Dict, Any
from firecrawl import FirecrawlApp
from src.config import settings


class ContentScraper:
    """Handles web scraping and content extraction using FireCrawl."""

    def __init__(self):
        """Initialize the scraper with FireCrawl API."""
        self.firecrawl = FirecrawlApp(api_key=settings.firecrawl_api_key)

    async def scrape_url(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape content from a URL using FireCrawl.

        Args:
            url: The URL to scrape

        Returns:
            Dictionary containing scraped content or None if scraping fails
        """
        try:
            result = self.firecrawl.scrape(url)
            return result
        except Exception as e:
            print(f"Error scraping URL {url}: {str(e)}")
            return None

    async def extract_text(self, url: str) -> Optional[str]:
        """
        Extract plain text from a URL.

        Args:
            url: The URL to extract text from

        Returns:
            Extracted text or None if extraction fails
        """
        result = await self.scrape_url(url)
        if result and "content" in result:
            return result["content"]
        return None

    async def extract_metadata(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Extract metadata from a URL.

        Args:
            url: The URL to extract metadata from

        Returns:
            Dictionary containing metadata or None if extraction fails
        """
        result = await self.scrape_url(url)
        if result:
            return {
                "title": result.get("metadata", {}).get("title"),
                "description": result.get("metadata", {}).get("description"),
                "image": result.get("metadata", {}).get("image"),
                "url": url,
            }
        return None


# Global scraper instance
scraper = ContentScraper()
