"""FastHTML web application for Social Media Agent."""

from fasthtml.common import *
from typing import Optional
import json
import uuid
from src.config import settings
from src.agents.generate_post_graph import generate_post_graph
from src.agents.types import SocialPlatform
from src.utils.mock_llm import mock_content_generator


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
                padding: 10px;
                background: white;
                border: 1px solid #eee;
                border-radius: 3px;
                min-height: 60px;
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
                flex-wrap: wrap;
            }
            .error { color: #d32f2f; padding: 10px; background: #ffebee; border-radius: 5px; }
            .success { color: #388e3c; padding: 10px; background: #e8f5e9; border-radius: 5px; }
            .loading { text-align: center; padding: 20px; }
            .edit-form { background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 10px 0; }
            .edit-textarea { width: 100%; min-height: 100px; padding: 10px; border: 1px solid #ccc; border-radius: 3px; font-family: monospace; }
            .char-count { font-size: 12px; color: #666; margin-top: 5px; }
            .platform-badge { 
                display: inline-block; 
                padding: 5px 10px; 
                border-radius: 20px; 
                font-size: 12px; 
                font-weight: bold;
                margin-right: 10px;
            }
            .twitter-badge { background: #1DA1F2; color: white; }
            .linkedin-badge { background: #0A66C2; color: white; }
            .status-badge {
                display: inline-block;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 12px;
                margin-left: 10px;
            }
            .status-pending { background: #fff3cd; color: #856404; }
            .status-approved { background: #d4edda; color: #155724; }
            .status-published { background: #d1ecf1; color: #0c5460; }
            .status-failed { background: #f8d7da; color: #721c24; }
            .preview-section { margin: 20px 0; }
            .preview-header { font-size: 18px; font-weight: bold; margin-bottom: 15px; }
        """)
    ]
)

# Store for managing posts
posts_store = {}


def render_post_card(post_id: str, post: dict) -> Div:
    """Render a single post card with preview and edit options."""
    platform = post['platform'].lower()
    platform_class = f"{platform}-badge"
    status_class = f"status-{post['status'].lower().replace(' ', '-')}"
    
    char_limit = 280 if platform == "twitter" else 3000
    char_count = len(post['content'])
    char_warning = " ⚠️" if platform == "twitter" and char_count > 280 else ""
    
    return Div(
        Div(
            Span(post['platform'].upper(), cls=f"platform-badge {platform_class}"),
            Span(post['status'], cls=f"status-badge {status_class}"),
            cls="post-meta"
        ),
        Div(post['content'], cls="post-content"),
        Div(
            f"Characters: {char_count}/{char_limit}{char_warning}",
            cls="char-count"
        ),
        Div(
            Button("✏️ Edit", hx_get=f"/edit/{post_id}", cls="btn-secondary"),
            Button("👍 Approve", hx_post=f"/approve/{post_id}", cls="btn-primary"),
            Button("❌ Reject", hx_post=f"/reject/{post_id}", cls="btn-danger"),
            cls="button-group"
        ),
        cls="post-card",
        id=f"post-{post_id}"
    )


def render_edit_form(post_id: str, post: dict) -> Div:
    """Render an edit form for a post."""
    platform = post['platform'].lower()
    char_limit = 280 if platform == "twitter" else 3000
    
    return Div(
        H4(f"Edit {post['platform']} Post"),
        Form(
            Textarea(
                post['content'],
                name="content",
                cls="edit-textarea",
                placeholder="Edit your post here...",
                maxlength=char_limit if platform == "twitter" else None,
                hx_on__input=f"document.getElementById('char-count-{post_id}').textContent = 'Characters: ' + this.value.length + '/{char_limit}'"
            ),
            Div(
                f"Characters: {len(post['content'])}/{char_limit}",
                id=f"char-count-{post_id}",
                cls="char-count"
            ),
            Div(
                Button("💾 Save", type="submit", cls="btn-primary"),
                Button("❌ Cancel", hx_get=f"/cancel/{post_id}", cls="btn-secondary"),
                cls="button-group"
            ),
            hx_post=f"/save/{post_id}",
            hx_target=f"#post-{post_id}",
            hx_swap="outerHTML"
        ),
        cls="edit-form"
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
                        Input(type="checkbox", name="twitter", value="on", checked=True),
                        " Twitter"
                    ),
                    Label(
                        Input(type="checkbox", name="linkedin", value="on", checked=True),
                        " LinkedIn"
                    ),
                    cls="form-group"
                ),
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
            hx_swap="innerHTML"
        ),
        
        Div(id="results"),
    )


@rt("/generate", methods=["POST"])
async def generate_posts(url: str, twitter: str = None, linkedin: str = None, style: str = "professional"):
    """Generate posts from a URL."""
    try:
        # Build platforms list from individual checkbox values
        platforms = []
        if twitter:
            platforms.append("twitter")
        if linkedin:
            platforms.append("linkedin")
        
        # Default to both if none selected
        if not platforms:
            platforms = ["twitter", "linkedin"]
        
        # Convert to SocialPlatform enums
        platform_enums = []
        for p in platforms:
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
        
        # Try to generate posts using mock generator if content was scraped
        posts_list = []
        
        if result.get("content"):
            # Content was successfully scraped, use mock generator
            for platform in platform_enums:
                try:
                    if platform == SocialPlatform.TWITTER:
                        post_content = await mock_content_generator.generate_twitter_post(
                            result["content"],
                            style=style
                        )
                    elif platform == SocialPlatform.LINKEDIN:
                        post_content = await mock_content_generator.generate_linkedin_post(
                            result["content"],
                            style=style
                        )
                    else:
                        continue
                    
                    post_id = str(uuid.uuid4())
                    post_dict = {
                        "platform": platform.value,
                        "content": post_content,
                        "status": "Pending Review"
                    }
                    posts_store[post_id] = post_dict
                    posts_list.append((post_id, post_dict))
                except Exception as e:
                    pass
        
        # If we have posts, render them
        if posts_list:
            posts_html = []
            for post_id, post in posts_list:
                posts_html.append(render_post_card(post_id, post))
            
            return Div(
                Div(
                    H2("Generated Posts (Preview)"),
                    P("Review and edit the posts below before approving."),
                    cls="preview-section"
                ),
                *posts_html,
                Div(
                    Button("✅ Approve All", hx_post="/approve-all", cls="btn-primary"),
                    Button("🗑️ Clear All", hx_delete="/clear", cls="btn-secondary"),
                    cls="button-group"
                )
            )
        
        # If no posts generated, show errors or message
        if result.get("errors"):
            return Div(
                Div(
                    H3("Errors occurred:"),
                    Ul(*[Li(error) for error in result["errors"]]),
                    cls="error"
                )
            )
        
        return Div(
            Div("No posts were generated.", cls="error")
        )
        
    except Exception as e:
        return Div(
            Div(f"Error: {str(e)}", cls="error")
        )


@rt("/edit/{post_id}", methods=["GET"])
async def edit_post(post_id: str):
    """Show edit form for a post."""
    if post_id not in posts_store:
        return Div(Div("Post not found", cls="error"))
    
    post = posts_store[post_id]
    return render_edit_form(post_id, post)


@rt("/save/{post_id}", methods=["POST"])
async def save_post(post_id: str, content: str):
    """Save edited post."""
    if post_id not in posts_store:
        return Div(Div("Post not found", cls="error"))
    
    posts_store[post_id]["content"] = content
    posts_store[post_id]["status"] = "Edited"
    
    return render_post_card(post_id, posts_store[post_id])


@rt("/cancel/{post_id}", methods=["GET"])
async def cancel_edit(post_id: str):
    """Cancel editing and return to post view."""
    if post_id not in posts_store:
        return Div(Div("Post not found", cls="error"))
    
    return render_post_card(post_id, posts_store[post_id])


@rt("/approve/{post_id}", methods=["POST"])
async def approve_post(post_id: str):
    """Approve a single post."""
    if post_id in posts_store:
        posts_store[post_id]["status"] = "Approved"
    
    return Div(
        Div(f"✅ Post approved!", cls="success"),
        hx_swap="outerHTML"
    )


@rt("/reject/{post_id}", methods=["POST"])
async def reject_post(post_id: str):
    """Reject a single post."""
    if post_id in posts_store:
        del posts_store[post_id]
    
    return Div(
        Div(f"❌ Post rejected and removed.", cls="error"),
        hx_swap="outerHTML"
    )


@rt("/approve-all", methods=["POST"])
async def approve_all():
    """Approve all posts."""
    for post_id in posts_store:
        posts_store[post_id]["status"] = "Approved"
    
    return Div(
        Div(f"✅ All {len(posts_store)} posts approved!", cls="success"),
        hx_swap="outerHTML"
    )


@rt("/clear", methods=["DELETE"])
async def clear_posts():
    """Clear all posts."""
    posts_store.clear()
    return Div("")


@rt("/health", methods=["GET"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    print("Starting Social Media Agent on 0.0.0.0:5001")
    print("Debug mode: True")
    print("Link: http://localhost:5001")
    uvicorn.run(app, host="0.0.0.0", port=5001, reload=True)
