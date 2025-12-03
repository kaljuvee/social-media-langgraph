"""FastHTML web application for the social media agent."""

from fasthtml.common import *
from typing import Optional
import json
from src.config import settings
from src.agents.generate_post_graph import generate_post_graph
from src.agents.types import SocialPlatform


# Create FastHTML app
app, rt = fast_app(
    title="Social Media Agent",
    pico=True,
    hdrs=[
        Meta(name="viewport", content="width=device-width, initial-scale=1"),
        Style("""
            .form-group { margin-bottom: 20px; }
            .post-card { 
                border: 1px solid #ccc; 
                padding: 15px; 
                margin: 10px 0; 
                border-radius: 5px;
                background: #f9f9f9;
            }
            .post-content { 
                font-size: 14px; 
                line-height: 1.5; 
                margin: 10px 0;
            }
            .post-meta { 
                font-size: 12px; 
                color: #666; 
                margin-top: 10px;
            }
            .button-group { 
                display: flex; 
                gap: 10px; 
                margin-top: 10px;
            }
            .error { color: #d32f2f; padding: 10px; background: #ffebee; border-radius: 5px; }
            .success { color: #388e3c; padding: 10px; background: #e8f5e9; border-radius: 5px; }
            .loading { text-align: center; padding: 20px; }
        """)
    ]
)

# Store for managing runs and sessions
runs_store = {}


def render_post_card(post_id: str, post: dict) -> Div:
    """Render a single post card."""
    return Div(
        H3(f"{post['platform'].upper()} Post"),
        Div(post['content'], cls="post-content"),
        Div(
            Span(f"Status: {post['status']}"),
            cls="post-meta"
        ),
        Div(
            Button("Approve", hx_post=f"/approve/{post_id}", cls="btn-primary"),
            Button("Edit", hx_get=f"/edit/{post_id}", cls="btn-secondary"),
            Button("Reject", hx_post=f"/reject/{post_id}", cls="btn-danger"),
            cls="button-group"
        ),
        cls="post-card"
    )


@rt
def index():
    """Home page with form to generate posts."""
    return Titled(
        "Social Media Agent",
        H1("Generate Social Media Posts"),
        P("Enter a URL to generate Twitter and LinkedIn posts automatically."),
        
        Form(
            Div(
                Label("URL to analyze:", _for="url"),
                Input(
                    type="url",
                    name="url",
                    id="url",
                    placeholder="https://example.com/article",
                    required=True
                ),
                cls="form-group"
            ),
            
            Div(
                Label("Platforms:"),
                Div(
                    Label(
                        Input(type="checkbox", name="platforms", value="twitter", checked=True),
                        " Twitter"
                    ),
                    Label(
                        Input(type="checkbox", name="platforms", value="linkedin", checked=True),
                        " LinkedIn"
                    ),
                    cls="form-group"
                ),
                cls="form-group"
            ),
            
            Div(
                Label("Style:", _for="style"),
                Select(
                    Option("Professional", value="professional", selected=True),
                    Option("Casual", value="casual"),
                    Option("Technical", value="technical"),
                    name="style",
                    id="style"
                ),
                cls="form-group"
            ),
            
            Button("Generate Posts", type="submit", cls="btn-primary"),
            hx_post="/generate",
            hx_target="#results",
            hx_swap="innerHTML",
        ),
        
        Div(id="results"),
    )


@rt("/generate", methods=["POST"])
async def generate_posts(url: str, platforms: list = None, style: str = "professional"):
    """Generate posts from a URL."""
    try:
        if not platforms:
            platforms = ["twitter", "linkedin"]
        
        # Ensure platforms is a list
        if isinstance(platforms, str):
            platforms = [platforms]
        
        # Filter out empty strings and convert to SocialPlatform enums
        platform_enums = []
        for p in platforms:
            if p and p.strip():
                try:
                    platform_enums.append(SocialPlatform(p.lower()))
                except ValueError:
                    pass
        
        # Create input for the graph
        input_data = {
            "url": url,
            "platforms": platform_enums,
            "style": style
        }
        
        # Run the graph
        result = await generate_post_graph.ainvoke({
            "input": input_data,
            "content": None,
            "posts": [],
            "errors": [],
            "human_feedback": None,
            "is_approved": False
        })
        
        # Render results
        if result.get("errors"):
            return Div(
                Div(
                    H3("Errors occurred:"),
                    Ul(*[Li(error) for error in result["errors"]]),
                    cls="error"
                )
            )
        
        if not result.get("posts"):
            return Div(
                Div("No posts were generated.", cls="error")
            )
        
        # Render posts
        posts_html = []
        for i, post in enumerate(result["posts"]):
            post_dict = {
                "platform": post.platform,
                "content": post.content,
                "status": post.status.value
            }
            posts_html.append(render_post_card(f"post_{i}", post_dict))
        
        return Div(
            H2("Generated Posts"),
            *posts_html,
            Div(
                Button("Approve All", hx_post="/approve-all", cls="btn-primary"),
                Button("Clear", hx_delete="/clear", cls="btn-secondary"),
                cls="button-group"
            )
        )
        
    except Exception as e:
        return Div(
            Div(f"Error: {str(e)}", cls="error")
        )


@rt("/approve/{post_id}", methods=["POST"])
async def approve_post(post_id: str):
    """Approve a single post."""
    return Div(
        Div(f"Post {post_id} approved!", cls="success"),
        hx_swap="outerHTML"
    )


@rt("/reject/{post_id}", methods=["POST"])
async def reject_post(post_id: str):
    """Reject a single post."""
    return Div(
        Div(f"Post {post_id} rejected.", cls="error"),
        hx_swap="outerHTML"
    )


@rt("/edit/{post_id}", methods=["GET"])
async def edit_post(post_id: str):
    """Show edit form for a post."""
    return Div(
        Textarea(
            id=f"edit_{post_id}",
            name="content",
            placeholder="Edit post content...",
            rows=5
        ),
        Button("Save", hx_post=f"/save/{post_id}", cls="btn-primary"),
        Button("Cancel", hx_get="/", cls="btn-secondary"),
        cls="form-group"
    )


@rt("/save/{post_id}", methods=["POST"])
async def save_post(post_id: str, content: str):
    """Save edited post."""
    return Div(
        Div(f"Post {post_id} updated!", cls="success")
    )


@rt("/approve-all", methods=["POST"])
async def approve_all():
    """Approve all posts."""
    return Div(
        Div("All posts approved and scheduled!", cls="success")
    )


@rt("/clear", methods=["DELETE"])
async def clear_posts():
    """Clear all posts."""
    return Div(id="results")


@rt("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    from src.config import settings
    serve(host=settings.host, port=settings.port)
