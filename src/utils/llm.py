"""LLM utilities for content generation and analysis."""

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.config import settings


class ContentGenerator:
    """Generates social media content using Claude."""

    def __init__(self):
        """Initialize the content generator with Claude."""
        self.llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            api_key=settings.anthropic_api_key
        )

    async def generate_twitter_post(self, content: str, style: str = "professional") -> str:
        """
        Generate a Twitter post from content.

        Args:
            content: The source content
            style: The style of the post (professional, casual, technical)

        Returns:
            Generated Twitter post
        """
        prompt = ChatPromptTemplate.from_template(
            """Based on the following content, generate a compelling Twitter post that is:
- Concise (under 280 characters)
- Engaging and informative
- Style: {style}
- Include relevant hashtags if appropriate

Content:
{content}

Generate only the tweet text, nothing else."""
        )

        chain = prompt | self.llm | StrOutputParser()
        result = await chain.ainvoke({
            "content": content,
            "style": style
        })
        return result.strip()

    async def generate_linkedin_post(self, content: str, style: str = "professional") -> str:
        """
        Generate a LinkedIn post from content.

        Args:
            content: The source content
            style: The style of the post (professional, casual, technical)

        Returns:
            Generated LinkedIn post
        """
        prompt = ChatPromptTemplate.from_template(
            """Based on the following content, generate a professional LinkedIn post that:
- Is engaging and thought-provoking
- Includes relevant insights or takeaways
- Style: {style}
- Can be longer than Twitter (up to 3000 characters)
- Include relevant hashtags

Content:
{content}

Generate only the LinkedIn post text, nothing else."""
        )

        chain = prompt | self.llm | StrOutputParser()
        result = await chain.ainvoke({
            "content": content,
            "style": style
        })
        return result.strip()

    async def summarize_content(self, content: str, max_length: int = 500) -> str:
        """
        Summarize content for social media.

        Args:
            content: The content to summarize
            max_length: Maximum length of summary

        Returns:
            Summarized content
        """
        prompt = ChatPromptTemplate.from_template(
            """Summarize the following content in {max_length} characters or less:

{content}

Provide only the summary, nothing else."""
        )

        chain = prompt | self.llm | StrOutputParser()
        result = await chain.ainvoke({
            "content": content,
            "max_length": max_length
        })
        return result.strip()

    async def extract_key_points(self, content: str) -> list:
        """
        Extract key points from content.

        Args:
            content: The content to extract from

        Returns:
            List of key points
        """
        prompt = ChatPromptTemplate.from_template(
            """Extract the 3-5 most important key points from the following content:

{content}

Return only the key points as a numbered list."""
        )

        chain = prompt | self.llm | StrOutputParser()
        result = await chain.ainvoke({"content": content})
        
        # Parse the numbered list
        points = [line.strip() for line in result.strip().split('\n') if line.strip()]
        return points


# Global content generator instance
content_generator = ContentGenerator()
