# Social Media LangGraph Agent

A Python-based social media agent using LangGraph and FastHTML to generate and schedule social media posts from URLs.

## Overview

This is a migration of the TypeScript social media agent to Python, using:
- **FastHTML** - For the web interface (replacing the TypeScript frontend)
- **LangGraph** - For orchestrating the agent workflow
- **LangChain** - For LLM interactions and content processing
- **Anthropic Claude** - For content generation
- **FireCrawl** - For web scraping and content extraction
- **Arcade** - For social media authentication and posting

## Features

- 🔗 Extract content from URLs using FireCrawl
- 🤖 Generate platform-specific social media posts using Claude
- 📱 Support for Twitter and LinkedIn
- 👤 Human-in-the-loop approval workflow
- 🎨 Beautiful FastHTML web interface
- 🔐 Secure authentication via Arcade
- 📊 Post scheduling and management

## Quick Start

### Prerequisites

- Python 3.11+
- pip or uv package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/kaljuvee/social-media-langgraph.git
cd social-media-langgraph
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Configuration

Required environment variables:

```bash
# LLM
ANTHROPIC_API_KEY=your_anthropic_key

# Web Scraping
FIRECRAWL_API_KEY=your_firecrawl_key

# Social Media
ARCADE_API_KEY=your_arcade_key
ARCADE_USER_ID=your_arcade_user_id
```

### Running Locally

```bash
python main.py
```

The application will start on `http://localhost:5001`

## Usage

1. Open the web interface at `http://localhost:5001`
2. Enter a URL to analyze
3. Select target platforms (Twitter, LinkedIn)
4. Choose a writing style
5. Click "Generate Posts"
6. Review generated posts
7. Approve and publish or edit as needed

## Project Structure

```
src/
├── agents/
│   ├── types.py              # Type definitions and state
│   └── generate_post_graph.py # Main LangGraph workflow
├── clients/
│   └── arcade_client.py       # Social media API client
├── utils/
│   ├── scraper.py            # Web scraping utilities
│   └── llm.py                # LLM content generation
├── app.py                     # FastHTML web application
└── config.py                  # Configuration management

main.py                         # Application entry point
```

## API Endpoints

### Web Interface
- `GET /` - Main page with generation form
- `POST /generate` - Generate posts from URL
- `POST /approve/{post_id}` - Approve a post
- `POST /reject/{post_id}` - Reject a post
- `GET /edit/{post_id}` - Edit post form
- `POST /save/{post_id}` - Save edited post
- `GET /health` - Health check

## Testing

Run tests with:
```bash
pytest
```

Run integration tests:
```bash
pytest -m integration
```

## Development

### Code Style
- Black for formatting
- Ruff for linting
- MyPy for type checking

Format code:
```bash
black src/
```

Lint code:
```bash
ruff check src/
```

## Migration Notes

This is a complete rewrite of the TypeScript social media agent in Python:

### Key Changes
- Replaced Express.js with FastHTML for the web framework
- Replaced TypeScript with Python
- Simplified the agent graph for core functionality
- Used Arcade for unified social media authentication
- Maintained the human-in-the-loop approval workflow

### Supported Features (Phase 1)
- ✅ URL content extraction
- ✅ Twitter post generation
- ✅ LinkedIn post generation
- ✅ Human approval workflow
- ✅ Post publishing via Arcade

### Future Enhancements
- Image selection and upload
- Content curation from multiple sources
- Post scheduling and analytics
- Reddit support
- GitHub content parsing
- YouTube video handling

## Troubleshooting

### Port already in use
Change the port in `.env`:
```bash
PORT=5002
```

### API Key errors
Ensure all required API keys are set in `.env` and valid.

### Content scraping fails
- Check if the URL is accessible
- Verify FireCrawl API key is valid
- Check internet connection

## License

MIT

## Support

For issues and questions, please open an issue on GitHub.
