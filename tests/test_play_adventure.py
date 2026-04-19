import pytest
from assertpy import assert_that
from fastmcp import FastMCP
from fastmcp.client import Client
from fastmcp.client.elicitation import ElicitResult

from ai_contained.plugins.helloworld import register


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


def describe_play_adventure():
    async def it_registers_the_tool(mcp):
        async with Client(transport=mcp) as client:
            tools = await client.list_tools()
            assert_that([t.name for t in tools]).contains("play_adventure")

    async def it_wins_via_cave(mcp):
        async with Client(transport=mcp, elicitation_handler=make_elicit_handler(["go left", "open chest"])) as client:
            result = await client.call_tool("play_adventure", {})
            assert_that(result.data).contains("You win")

    async def it_wins_via_river_boat(mcp):
        async with Client(transport=mcp, elicitation_handler=make_elicit_handler(["go right", "take boat"])) as client:
            result = await client.call_tool("play_adventure", {})
            assert_that(result.data).contains("You win")

    async def it_loses_by_jumping(mcp):
        async with Client(transport=mcp, elicitation_handler=make_elicit_handler(["go right", "jump across"])) as client:
            result = await client.call_tool("play_adventure", {})
            assert_that(result.data).contains("Game over")

    async def it_can_go_back_from_cave(mcp):
        async with Client(transport=mcp, elicitation_handler=make_elicit_handler(["go left", "go back", "go right", "take boat"])) as client:
            result = await client.call_tool("play_adventure", {})
            assert_that(result.data).contains("You win")

    async def it_abandons_on_decline(mcp):
        async def decline_handler(message, response_type, params, context):
            return ElicitResult(action="decline", content=None)

        async with Client(transport=mcp, elicitation_handler=decline_handler) as client:
            result = await client.call_tool("play_adventure", {})
            assert_that(result.data).contains("abandoned")
