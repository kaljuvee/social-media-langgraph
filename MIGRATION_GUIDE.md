# TypeScript to Python Migration Guide

## Overview

This document describes the migration of the LangGraph Social Media Agent from TypeScript to Python, with a complete rewrite using FastHTML for the web interface.

## Key Changes

### Framework Changes

| Component | TypeScript | Python |
|-----------|-----------|--------|
| Web Framework | Express.js | FastHTML |
| LLM Integration | LangChain JS | LangChain Python |
| Agent Orchestration | LangGraph JS | LangGraph Python |
| Content Generation | Claude via API | Claude via LangChain |
| Web Scraping | Custom/Playwright | FireCrawl |
| Social Media Auth | Custom OAuth | Arcade SDK |
| Type System | TypeScript | Pydantic |
| Testing | Jest | Pytest |

### Architecture Changes

#### TypeScript Structure
```
src/
├── agents/
│   ├── generate-post/
│   ├── upload-post/
│   ├── reflection/
│   └── ...
├── clients/
│   ├── auth-server.ts
│   ├── linkedin.ts
│   └── twitter/
├── utils/
├── tests/
└── evals/
```

#### Python Structure
```
src/
├── agents/
│   ├── types.py (State definitions)
│   └── generate_post_graph.py (Main graph)
├── clients/
│   ├── arcade_client.py (Social media auth)
│   └── arcade_mock.py (Mock for testing)
├── utils/
│   ├── scraper.py (FireCrawl integration)
│   ├── llm.py (Content generation)
├── app.py (FastHTML application)
├── config.py (Settings management)
└── tests/
```

## Migration Approach

### Phase 1: Core Infrastructure
- ✅ Set up Python project structure with pyproject.toml
- ✅ Implement configuration management using Pydantic Settings
- ✅ Create type definitions for agent state
- ✅ Set up environment variable handling

### Phase 2: External Integrations
- ✅ Integrate FireCrawl for web scraping
- ✅ Implement Anthropic Claude integration via LangChain
- ✅ Create Arcade client wrapper (with mock fallback)
- ✅ Set up LLM utilities for content generation

### Phase 3: Agent Logic
- ✅ Implement LangGraph state machine
- ✅ Create node functions for:
  - Content scraping
  - Post generation
  - Human approval workflow
  - Post publishing
- ✅ Set up conditional routing

### Phase 4: Web Interface
- ✅ Replace Express.js with FastHTML
- ✅ Create responsive HTML forms
- ✅ Implement HTMX for dynamic updates
- ✅ Add error handling and user feedback

### Phase 5: Testing & Deployment
- ✅ Set up Pytest with async support
- ✅ Create unit tests for core modules
- ✅ Local testing with real API keys
- ✅ Documentation and deployment guide

## Code Migration Examples

### Configuration Management

**TypeScript (dotenv)**
```typescript
import dotenv from 'dotenv';
dotenv.config();
const apiKey = process.env.ANTHROPIC_API_KEY;
```

**Python (Pydantic Settings)**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    anthropic_api_key: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### LLM Integration

**TypeScript**
```typescript
import { ChatAnthropic } from "@langchain/anthropic";

const llm = new ChatAnthropic({
  modelName: "claude-3-5-sonnet-20241022",
  apiKey: process.env.ANTHROPIC_API_KEY,
});
```

**Python**
```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    api_key=settings.anthropic_api_key
)
```

### Graph Definition

**TypeScript**
```typescript
const graph = new StateGraph(GeneratePostState);
graph.addNode("scrape_content", scrapeContentNode);
graph.addNode("generate_posts", generatePostsNode);
graph.addEdge(START, "scrape_content");
graph.addEdge("scrape_content", "generate_posts");
```

**Python**
```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(GeneratePostState)
graph.add_node("scrape_content", scrape_content_node)
graph.add_node("generate_posts", generate_posts_node)
graph.add_edge(START, "scrape_content")
graph.add_edge("scrape_content", "generate_posts")
```

### Web Framework

**TypeScript (Express.js)**
```typescript
app.post('/generate', async (req, res) => {
  const { url, platforms } = req.body;
  // Process request
  res.json(result);
});
```

**Python (FastHTML)**
```python
@rt("/generate", methods=["POST"])
async def generate_posts(url: str, platforms: list = None):
    # Process request
    return Div(H2("Generated Posts"), *posts_html)
```

## API Compatibility

### Endpoints

| Endpoint | Method | TypeScript | Python | Status |
|----------|--------|-----------|--------|--------|
| / | GET | ✅ | ✅ | Migrated |
| /generate | POST | ✅ | ✅ | Migrated |
| /approve/{id} | POST | ✅ | ✅ | Migrated |
| /reject/{id} | POST | ✅ | ✅ | Migrated |
| /edit/{id} | GET | ✅ | ✅ | Migrated |
| /save/{id} | POST | ✅ | ✅ | Migrated |
| /health | GET | ✅ | ✅ | Migrated |

## Environment Variables

Both versions use the same environment variables:

```bash
# LLM
ANTHROPIC_API_KEY=

# Web Scraping
FIRECRAWL_API_KEY=

# Social Media
ARCADE_API_KEY=
ARCADE_USER_ID=

# Application
HOST=0.0.0.0
PORT=5001
DEBUG=false
```

## Dependencies

### TypeScript
- @langchain/anthropic
- @langchain/langgraph
- @langchain/core
- @mendable/firecrawl-js
- @arcadeai/arcadejs
- express
- typescript

### Python
- python-fasthtml
- langgraph
- langchain
- langchain-anthropic
- langchain-community
- firecrawl-py
- pydantic
- pydantic-settings
- pytest
- pytest-asyncio

## Testing

### TypeScript
```bash
yarn test                # Unit tests
yarn test:int           # Integration tests
yarn test:all           # All tests
```

### Python
```bash
pytest                   # All tests
pytest -v               # Verbose
pytest src/tests/       # Specific directory
pytest -m integration   # Integration tests only
```

## Performance Considerations

### Improvements
- **Faster startup**: Python FastHTML starts faster than Express.js
- **Better async handling**: Native Python async/await
- **Simpler deployment**: Single Python process vs Node.js

### Trade-offs
- **Memory usage**: Python uses more memory than Node.js
- **Type safety**: Pydantic provides runtime validation vs TypeScript compile-time

## Deployment

### Local Development
```bash
python main.py
```

### Production
```bash
# Using Uvicorn directly
uvicorn src.app:app --host 0.0.0.0 --port 5001 --workers 4

# Using FastHTML serve
python -c "from src.app import serve; serve()"
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -e .
CMD ["python", "main.py"]
```

## Known Differences

### Removed Features (Phase 1)
- Image selection and upload (will be added in Phase 2)
- Reddit post generation (will be added in Phase 2)
- GitHub content parsing (will be added in Phase 2)
- YouTube video handling (will be added in Phase 2)
- Slack integration (will be added in Phase 2)

### New Features
- Simplified FastHTML UI with HTMX
- Built-in mock Arcade client for testing
- Pydantic-based configuration
- Pytest-based testing framework

## Migration Checklist

- [x] Project structure setup
- [x] Configuration management
- [x] Type definitions
- [x] External API integrations
- [x] LangGraph agent implementation
- [x] FastHTML web interface
- [x] Error handling
- [x] Testing framework
- [x] Documentation
- [x] Git repository setup
- [ ] Advanced features (Phase 2)
- [ ] Performance optimization
- [ ] Production deployment
- [ ] Monitoring and logging

## Future Enhancements

### Phase 2
- Image selection and upload
- Reddit post generation
- GitHub content parsing
- YouTube video handling
- Slack integration

### Phase 3
- Advanced analytics
- Post scheduling
- A/B testing
- Multi-language support
- Custom prompt templates

## Support

For issues or questions about the migration, please refer to:
- README.md - Project overview and quick start
- FEATURES.md - Detailed feature list
- GitHub Issues - Bug reports and feature requests

## References

- [FastHTML Documentation](https://www.fastht.ml/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Python Documentation](https://python.langchain.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
