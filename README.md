# Browser Automation Agent Framework

A custom-built autonomous agent framework for browser automation, developed from scratch without relying on LangChain or LangGraph. This project demonstrates core concepts of building agentic systems while maintaining full control over the implementation.

## Demo
![Phone Finder Demo](src/examples/phone-finder.gif)
*Demo showing the agent searching for phones under ₹30,000*

![LinkedIn Search Demo](src/examples/linkedin-search-example.gif)
*Demo showing the agent performing LinkedIn profile search and company analysis*

## Current Implementation
- Custom agent framework with tool-based architecture
- Browser automation capabilities using Playwright
- Basic CLI interface for agent interaction
- FastAPI integration (work in progress)
- SQLite for data persistence (development purposes)

## Getting Started

1. Install Miniconda (if not already installed)
   - Download from [Miniconda website](https://docs.conda.io/en/latest/miniconda.html)

2. Setup the environment
```bash
make install
```

3. Run the CLI tool
```bash
make run
```

4. For FastAPI app (work in progress)
```bash
uvicorn src.playwright_fastapi_app.app:app --host 0.0.0.0 --port 4000 --reload
```

## Production Considerations

For production deployment, several improvements are planned:

- **Framework Integration**: 
  - Integrate with LangChain/LangGraph for enhanced agent capabilities
  - Leverage battle-tested components instead of custom implementations
  - Implement custom function calling for better performance (OpenAI's function calling can be slow)

- **Infrastructure**:
  - Replace SQLite with PostgreSQL for robust data persistence
  - Add Langfuse for observability and tracing
  - Implement LiteLLM for flexible LLM provider switching

## Current Limitations & Future Work

This is a proof-of-concept implementation with several pending improvements:

- Multi Step Agentic Loop
- Enhanced error handling and recovery
- Better conversation memory management
- Improved tool validation and safety checks
- Comprehensive testing suite
- Better documentation and examples
- Custom function calling implementation to improve response times

## Features
- Proxy server support through BrightData (Note: Google may still detect and block automated access)

## Work in Progress
- FastAPI application for improved API access and management

## Known Limitations
- Even with proxy server configuration through BrightData, Google may still detect and block automated access

## Development Process
To understand the thought process and evolution of this project, please check the commit history. It provides detailed insights into how the implementation progressed and various design decisions made along the way.

# If this submission is not good enough, please let me know. I will fix the issues.
<p align="center">
  <img src="src/examples/hi5dojjie.png" width="300" alt="hi5dojjie">
</p>