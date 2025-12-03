"""Type definitions for the social media agent."""

from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
from enum import Enum


class PostStatus(str, Enum):
    """Status of a generated post."""
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"


class SocialPlatform(str, Enum):
    """Supported social media platforms."""
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    REDDIT = "reddit"


@dataclass
class GeneratedPost:
    """Represents a generated social media post."""
    platform: SocialPlatform
    content: str
    status: PostStatus = PostStatus.DRAFT
    scheduled_time: Optional[str] = None
    media_urls: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContentInput:
    """Input for content generation."""
    url: str
    platforms: List[SocialPlatform] = field(default_factory=lambda: [SocialPlatform.TWITTER, SocialPlatform.LINKEDIN])
    style: Optional[str] = None
    additional_context: Optional[str] = None


@dataclass
class AgentState:
    """State for the social media agent graph."""
    input: ContentInput
    content: Optional[str] = None
    posts: List[GeneratedPost] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    human_feedback: Optional[str] = None
    is_approved: bool = False
