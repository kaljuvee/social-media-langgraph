"""Tests for the LLM content generator."""

import pytest
from src.utils.llm import ContentGenerator


@pytest.fixture
def generator():
    """Create a content generator instance for testing."""
    return ContentGenerator()


def test_generator_initialization(generator):
    """Test that generator initializes correctly."""
    assert generator is not None
    assert generator.llm is not None


def test_generator_has_methods(generator):
    """Test that generator has all required methods."""
    assert hasattr(generator, 'generate_twitter_post')
    assert hasattr(generator, 'generate_linkedin_post')
    assert hasattr(generator, 'summarize_content')
    assert hasattr(generator, 'extract_key_points')
    assert callable(generator.generate_twitter_post)
    assert callable(generator.generate_linkedin_post)
    assert callable(generator.summarize_content)
    assert callable(generator.extract_key_points)
