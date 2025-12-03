"""Main entry point for the social media agent application."""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app import app, serve
from src.config import settings


if __name__ == "__main__":
    print(f"Starting Social Media Agent on {settings.host}:{settings.port}")
    print(f"Debug mode: {settings.debug}")
    serve(host=settings.host, port=settings.port)
