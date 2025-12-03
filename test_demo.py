#!/usr/bin/env python3
"""
Demo script to test the social media agent with mock data.
This demonstrates what the full workflow looks like when content is successfully scraped.
"""

import asyncio
from src.agents.types import SocialPlatform, PostStatus
from src.utils.llm import ContentGenerator
from src.config import settings


async def demo_post_generation():
    """Demonstrate the post generation workflow with mock content."""
    
    # Mock content that would be scraped from a URL
    mock_content = """
    LangChain: Building Intelligent Applications with AI
    
    LangChain is a framework for developing applications powered by language models. 
    It enables applications that are:
    - Data-aware: connect a language model to other sources of data
    - Agentic: allow a language model to interact with its environment
    
    The main value props of LangChain are:
    1. Components: abstractions for working with language models, plus a collection of implementations for every abstraction
    2. Chains: assembled components into a coherent worflows
    
    LangChain provides standard, extendable interfaces and external integrations so that you can quickly and easily 
    build LLM apps whether you're using OpenAI, Anthropic, or open source models running on your own infrastructure.
    
    Key Features:
    - Support for multiple LLM providers
    - Chains for complex workflows
    - Agents for autonomous decision making
    - Memory management
    - Document loaders and processors
    - Vector stores for semantic search
    """
    
    print("=" * 80)
    print("SOCIAL MEDIA AGENT - POST GENERATION DEMO")
    print("=" * 80)
    print()
    
    # Initialize the content generator
    generator = ContentGenerator()
    print("✓ Content Generator initialized")
    print()
    
    # Demonstrate different writing styles
    styles = ["professional", "casual", "technical"]
    platforms = ["twitter", "linkedin"]
    
    for style in styles:
        print(f"\n{'=' * 80}")
        print(f"STYLE: {style.upper()}")
        print(f"{'=' * 80}\n")
        
        # Generate Twitter post
        print("📱 TWITTER POST:")
        print("-" * 80)
        try:
            twitter_post = await generator.generate_twitter_post(
                mock_content,
                style=style
            )
            print(f"✓ Generated: {twitter_post}")
            print(f"  Length: {len(twitter_post)} characters (limit: 280)")
        except Exception as e:
            print(f"✗ Error: {e}")
        
        print()
        
        # Generate LinkedIn post
        print("💼 LINKEDIN POST:")
        print("-" * 80)
        try:
            linkedin_post = await generator.generate_linkedin_post(
                mock_content,
                style=style
            )
            print(f"✓ Generated: {linkedin_post[:200]}...")
            print(f"  Full length: {len(linkedin_post)} characters")
        except Exception as e:
            print(f"✗ Error: {e}")
        
        print()
    
    # Demonstrate content analysis
    print(f"\n{'=' * 80}")
    print("CONTENT ANALYSIS")
    print(f"{'=' * 80}\n")
    
    print("📊 CONTENT SUMMARY:")
    print("-" * 80)
    try:
        summary = await generator.summarize_content(mock_content)
        print(f"✓ Summary: {summary}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print()
    
    print("🔑 KEY POINTS:")
    print("-" * 80)
    try:
        key_points = await generator.extract_key_points(mock_content)
        for i, point in enumerate(key_points, 1):
            print(f"  {i}. {point}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print()
    print("=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    print("\nStarting Social Media Agent Demo...\n")
    asyncio.run(demo_post_generation())
