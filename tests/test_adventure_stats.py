import json
from assertpy import assert_that
from fastmcp.client import Client

from conftest import make_elicit_handler


def describe_adventure_stats():
    STATS_URI = "adventure://stats"

    async def it_registers_the_resource(mcp):
        async with Client(transport=mcp) as client:
            resources = await client.list_resources()
            assert_that([str(r.uri) for r in resources]).contains(STATS_URI)

    async def it_returns_default_stats(mcp):
        async with Client(transport=mcp) as client:
            content = await client.read_resource(STATS_URI)
            assert_that(json.loads(content[0].text)).is_equal_to({"health": 100, "adventures": 0})

    async def it_updates_stats_on_win(mcp):
        async with Client(transport=mcp, elicitation_handler=make_elicit_handler(["go left", "open chest"])) as client:
            await client.call_tool("play_adventure", {})
            content = await client.read_resource(STATS_URI)
            assert_that(json.loads(content[0].text)).is_equal_to({"health": 100, "adventures": 1})

    async def it_updates_stats_on_loss(mcp):
        async with Client(transport=mcp, elicitation_handler=make_elicit_handler(["go right", "jump across"])) as client:
            await client.call_tool("play_adventure", {})
            content = await client.read_resource(STATS_URI)
            assert_that(json.loads(content[0].text)).is_equal_to({"health": 0, "adventures": 1})

    async def it_increments_adventures_across_plays(mcp):
        async with Client(transport=mcp, elicitation_handler=make_elicit_handler(["go left", "open chest", "go left", "open chest"])) as client:
            await client.call_tool("play_adventure", {})
            await client.call_tool("play_adventure", {})
            content = await client.read_resource(STATS_URI)
            assert_that(json.loads(content[0].text)).contains_entry({"adventures": 2})
