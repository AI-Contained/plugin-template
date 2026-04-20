# plugin-helloworld

A hello world plugin for [AI-Contained](https://github.com/AI-Contained) demonstrating the plugin architecture with a choose-your-own-adventure game.

## Using as a Template

Click **"Use this template"** on GitHub to create a new plugin repo, then:

1. Rename `src/ai_contained/plugins/helloworld/` → `src/ai_contained/plugins/<yourplugin>/`
2. Find-replace `helloworld` → `<yourplugin>` in `pyproject.toml`
3. Replace the `play_adventure` tool in `__init__.py` with your own tools
4. Update the `# TODO` comments in `pyproject.toml`
5. Update `tests/test_play_adventure.py` with tests for your tools - use the existing tests as a reference for how to use `Client`, fixtures, and elicitation handlers

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
