"""Tests for the content scraper."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.utils.scraper import ContentScraper


@pytest.fixture
def scraper():
    """Create a scraper instance for testing."""
    return ContentScraper()


@pytest.mark.asyncio
async def test_scrape_url_success(scraper):
    """Test successful URL scraping."""
    mock_result = {
        "content": "Test content",
        "metadata": {
            "title": "Test Title",
            "description": "Test Description"
        }
    }
    
    scraper.firecrawl.scrape = MagicMock(return_value=mock_result)
    result = await scraper.scrape_url("https://example.com")
    assert result == mock_result


@pytest.mark.asyncio
async def test_extract_text(scraper):
    """Test text extraction from URL."""
    mock_result = {
        "content": "Extracted text content"
    }
    
    scraper.firecrawl.scrape = MagicMock(return_value=mock_result)
    text = await scraper.extract_text("https://example.com")
    assert text == "Extracted text content"


@pytest.mark.asyncio
async def test_extract_metadata(scraper):
    """Test metadata extraction from URL."""
    mock_result = {
        "metadata": {
            "title": "Test Title",
            "description": "Test Description",
            "image": "https://example.com/image.jpg"
        }
    }
    
    scraper.firecrawl.scrape = MagicMock(return_value=mock_result)
    metadata = await scraper.extract_metadata("https://example.com")
    assert metadata["title"] == "Test Title"
    assert metadata["description"] == "Test Description"


@pytest.mark.asyncio
async def test_scrape_url_failure(scraper):
    """Test handling of scraping failure."""
    scraper.firecrawl.scrape = MagicMock(side_effect=Exception("API Error"))
    result = await scraper.scrape_url("https://example.com")
    assert result is None
