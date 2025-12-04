"""Mock LLM for demonstration and testing."""

import re
from typing import List


class MockContentGenerator:
    """Generates realistic mock social media content for testing."""

    def __init__(self):
        """Initialize the mock generator."""
        pass

    async def generate_twitter_post(self, content: str, style: str = "professional") -> str:
        """
        Generate a mock Twitter post from content.

        Args:
            content: The source content
            style: The style of the post (professional, casual, technical)

        Returns:
            Generated Twitter post
        """
        # Extract title or first meaningful text
        lines = [l.strip() for l in content.split('\n') if l.strip() and len(l.strip()) > 10]
        title = lines[0] if lines else "New Tender"
        
        # Extract key info
        value_match = re.search(r'€([\d,]+(?:\.\d+)?)', content)
        value = f"€{value_match.group(1)}" if value_match else "€N/A"
        
        deadline_match = re.search(r'December (\d+), (\d+)', content)
        deadline = f"Dec {deadline_match.group(1)}" if deadline_match else "Soon"
        
        posts = {
            "professional": f"📢 New Tender: {title}\n\nBudget: {value}\nDeadline: {deadline}\n\nExplore opportunities and submit your bid. #Procurement #Tender",
            "casual": f"🎯 Check out this new tender: {title}\n\nBudget: {value}\nDue: {deadline}\n\nInterested? Apply now! 💼 #Opportunities",
            "technical": f"📋 Tender Announcement: {title}\n\nAllocation: {value}\nSubmission Deadline: {deadline}\n\nReview specifications and requirements. #TenderProcess"
        }
        
        return posts.get(style, posts["professional"])[:280]

    async def generate_linkedin_post(self, content: str, style: str = "professional") -> str:
        """
        Generate a mock LinkedIn post from content.

        Args:
            content: The source content
            style: The style of the post (professional, casual, technical)

        Returns:
            Generated LinkedIn post
        """
        # Extract title
        lines = [l.strip() for l in content.split('\n') if l.strip() and len(l.strip()) > 10]
        title = lines[0] if lines else "New Tender Opportunity"
        
        # Extract key info
        value_match = re.search(r'€([\d,]+(?:\.\d+)?)', content)
        value = f"€{value_match.group(1)}" if value_match else "Budget TBD"
        
        category_match = re.search(r'KATEGOORIA\s+([^\n]+)', content)
        category = category_match.group(1).strip() if category_match else "Supplies"
        
        posts = {
            "professional": f"""🎯 Exciting Tender Opportunity: {title}

We're pleased to announce a new procurement opportunity in the {category} sector.

📊 Key Details:
• Budget Allocation: {value}
• Category: {category}
• Scope: Comprehensive procurement initiative

This represents a significant opportunity for qualified suppliers and partners to contribute to important projects. We encourage interested parties to review the full tender documentation and submit competitive proposals.

For more information and to submit your bid, visit the tender portal.

#Procurement #Tender #BusinessOpportunity #SupplyChain""",
            
            "casual": f"""🚀 New Tender Alert: {title}

Exciting news! A new {category} tender has just been posted.

💰 Budget: {value}
📋 Category: {category}

If you're interested in this opportunity, now's the time to review the requirements and submit your proposal. Let's make something great together!

#Opportunities #Procurement #Growth""",
            
            "technical": f"""📋 Tender Specification: {title}

Technical procurement notice for {category} services.

Specifications:
• Project Category: {category}
• Budget Allocation: {value}
• Procurement Type: Competitive Bidding

Interested vendors should review the complete technical requirements and submission guidelines. Compliance with all specifications is mandatory.

#TenderProcess #Procurement #TechnicalSpecifications"""
        }
        
        return posts.get(style, posts["professional"])

    async def summarize_content(self, content: str, max_length: int = 500) -> str:
        """
        Summarize content for social media.

        Args:
            content: The content to summarize
            max_length: Maximum length of summary

        Returns:
            Summarized content
        """
        lines = [l.strip() for l in content.split('\n') if l.strip()]
        summary = " ".join(lines[:5])
        return summary[:max_length]

    async def extract_key_points(self, content: str) -> List[str]:
        """
        Extract key points from content.

        Args:
            content: The content to extract from

        Returns:
            List of key points
        """
        points = []
        
        # Extract value
        value_match = re.search(r'€([\d,]+(?:\.\d+)?)', content)
        if value_match:
            points.append(f"Budget: €{value_match.group(1)}")
        
        # Extract deadline
        deadline_match = re.search(r'December (\d+), (\d+)', content)
        if deadline_match:
            points.append(f"Deadline: December {deadline_match.group(1)}, {deadline_match.group(2)}")
        
        # Extract category
        category_match = re.search(r'KATEGOORIA\s+([^\n]+)', content)
        if category_match:
            points.append(f"Category: {category_match.group(1).strip()}")
        
        # Extract organization
        org_match = re.search(r'ORGANISATSIOON\s+([^\n]+)', content)
        if org_match:
            points.append(f"Organization: {org_match.group(1).strip()}")
        
        # Extract location
        location_match = re.search(r'ASUKOHT\s+([^\n]+)', content)
        if location_match:
            points.append(f"Location: {location_match.group(1).strip()}")
        
        return points if points else ["Tender opportunity available", "Review full details on tender portal"]


# Global mock generator instance
mock_content_generator = MockContentGenerator()
