# plugin-helloworld

A hello world plugin for [AI-Contained](https://github.com/AI-Contained) demonstrating the plugin architecture with a choose-your-own-adventure game.

## Tools

- **`play_adventure`** - An interactive choose-your-own-adventure game using MCP elicitation

## Installation

### Local Development

```bash
pip install -e ".[dev]" --break-system-packages
```

### Production

```bash
pip install "ai-contained-plugin-helloworld @ git+https://github.com/AI-Contained/plugin-helloworld.git@main"
```

## Running Tests

```bash
pytest -v
```
