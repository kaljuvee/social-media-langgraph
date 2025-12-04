"""LangGraph agent for generating social media posts."""

from langgraph.graph import StateGraph, START, END
from typing import Annotated, TypedDict
from src.agents.types import AgentState, GeneratedPost, SocialPlatform, PostStatus
from src.utils.scraper import scraper
from src.utils.llm import content_generator
from src.clients.arcade_client import arcade_client


class GeneratePostState(TypedDict):
    """State for the generate post graph."""
    input: dict
    content: str
    posts: list
    errors: list
    human_feedback: str
    is_approved: bool


async def scrape_content_node(state: GeneratePostState) -> GeneratePostState:
    """
    Scrape content from the provided URL.

    Args:
        state: Current graph state

    Returns:
        Updated state with scraped content
    """
    try:
        url = state["input"]["url"]
        content = await scraper.extract_text(url)
        
        if not content:
            state["errors"].append(f"Failed to scrape content from {url}")
            return state
        
        state["content"] = content
        return state
    except Exception as e:
        state["errors"].append(f"Error scraping content: {str(e)}")
        return state


async def generate_posts_node(state: GeneratePostState) -> GeneratePostState:
    """
    Generate posts for each requested platform.

    Args:
        state: Current graph state

    Returns:
        Updated state with generated posts
    """
    if not state.get("content"):
        state["errors"].append("No content available for post generation")
        return state

    try:
        platforms = state["input"].get("platforms", [SocialPlatform.TWITTER, SocialPlatform.LINKEDIN])
        style = state["input"].get("style", "professional")
        posts = []

        for platform in platforms:
            try:
                if platform == SocialPlatform.TWITTER:
                    post_content = await content_generator.generate_twitter_post(
                        state["content"],
                        style=style
                    )
                elif platform == SocialPlatform.LINKEDIN:
                    post_content = await content_generator.generate_linkedin_post(
                        state["content"],
                        style=style
                    )
                else:
                    continue

                post = GeneratedPost(
                    platform=platform,
                    content=post_content,
                    status=PostStatus.PENDING_APPROVAL
                )
                posts.append(post)
            except Exception as platform_error:
                state["errors"].append(f"Error generating {platform.value} post: {str(platform_error)}")
                continue

        state["posts"] = posts
        return state
    except Exception as e:
        state["errors"].append(f"Error generating posts: {str(e)}")
        return state


async def human_approval_node(state: GeneratePostState) -> GeneratePostState:
    """
    Wait for human approval of generated posts.

    Args:
        state: Current graph state

    Returns:
        Updated state with approval status
    """
    # This node would be interrupted for human feedback
    # For now, we'll just mark it as pending
    state["is_approved"] = False
    return state


def should_publish(state: GeneratePostState) -> str:
    """
    Determine if posts should be published or scheduled.

    Args:
        state: Current graph state

    Returns:
        Next node to execute
    """
    if state.get("is_approved"):
        return "publish_posts"
    return END


async def publish_posts_node(state: GeneratePostState) -> GeneratePostState:
    """
    Publish approved posts to social media.

    Args:
        state: Current graph state

    Returns:
        Updated state with published posts
    """
    try:
        for post in state["posts"]:
            if post.platform == SocialPlatform.TWITTER:
                post_id = await arcade_client.post_to_twitter(post.content)
            elif post.platform == SocialPlatform.LINKEDIN:
                post_id = await arcade_client.post_to_linkedin(post.content)
            else:
                continue

            if post_id:
                post.status = PostStatus.PUBLISHED
                post.metadata["post_id"] = post_id
            else:
                post.status = PostStatus.FAILED
                state["errors"].append(f"Failed to publish {post.platform} post")

        return state
    except Exception as e:
        state["errors"].append(f"Error publishing posts: {str(e)}")
        return state


def create_generate_post_graph():
    """
    Create the LangGraph for generating social media posts.

    Returns:
        Compiled graph ready for execution
    """
    graph = StateGraph(GeneratePostState)

    # Add nodes
    graph.add_node("scrape_content", scrape_content_node)
    graph.add_node("generate_posts", generate_posts_node)
    graph.add_node("human_approval", human_approval_node)
    graph.add_node("publish_posts", publish_posts_node)

    # Add edges
    graph.add_edge(START, "scrape_content")
    graph.add_edge("scrape_content", "generate_posts")
    graph.add_edge("generate_posts", "human_approval")
    graph.add_conditional_edges("human_approval", should_publish)
    graph.add_edge("publish_posts", END)

    return graph.compile()


# Create the graph
generate_post_graph = create_generate_post_graph()
