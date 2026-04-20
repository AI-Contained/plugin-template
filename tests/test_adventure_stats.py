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
            assert_that(json.loads(content[0].text)).is_equal_to({"health": 90, "adventures": 1})

    async def it_increments_adventures_across_plays(mcp):
        num_plays = 2
        async with Client(transport=mcp, elicitation_handler=make_elicit_handler(["go left", "open chest"] * num_plays)) as client:
            for _ in range(num_plays):
                await client.call_tool("play_adventure", {})
            content = await client.read_resource(STATS_URI)
            assert_that(json.loads(content[0].text)).contains_entry({"adventures": num_plays})

    async def it_caps_health_at_100_on_win(mcp):
        num_plays = 2
        async with Client(transport=mcp, elicitation_handler=make_elicit_handler(["go left", "open chest"] * num_plays)) as client:
            for _ in range(num_plays):
                await client.call_tool("play_adventure", {})
            content = await client.read_resource(STATS_URI)
            assert_that(json.loads(content[0].text)).contains_entry({"health": 100})

    async def it_floors_health_at_0_on_loss(mcp):
        # Each play requires 2 choices. All plays must be in a single Client session
        # since ctx.get_state is session-scoped - a new Client() would reset the state.
        num_attempts = 11  # 10 losses to reach 0, 11th verifies it stays at 0
        async with Client(transport=mcp, elicitation_handler=make_elicit_handler(["go right", "jump across"] * num_attempts)) as client:
            for _ in range(num_attempts):
                await client.call_tool("play_adventure", {})
            content = await client.read_resource(STATS_URI)
            assert_that(json.loads(content[0].text)).contains_entry({"health": 0})

    async def it_includes_stats_uri_in_result(mcp):
        async with Client(transport=mcp, elicitation_handler=make_elicit_handler(["go left", "open chest"])) as client:
            result = await client.call_tool("play_adventure", {})
            assert_that(result.data).contains("adventure://stats")
