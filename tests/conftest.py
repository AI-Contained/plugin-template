import pytest
from fastmcp import FastMCP
from fastmcp.client.elicitation import ElicitResult

from ai_contained.plugins.template import register


@pytest.fixture
def mcp() -> FastMCP:
    server = FastMCP("test")
    register(server)
    return server


def make_elicit_handler(choices: list[str]):
    it = iter(choices)
    async def handler(message, response_type, params, context):
        return ElicitResult(action="accept", content={"value": next(it)})
    return handler
