from assertpy import assert_that
from fastmcp.client import Client

from conftest import make_elicit_handler


def describe_adventure_recap():
    PROMPT_NAME = "adventure_recap"

    async def it_registers_the_prompt(mcp):
        async with Client(transport=mcp) as client:
            prompts = await client.list_prompts()
            assert_that([p.name for p in prompts]).contains(PROMPT_NAME)

    async def it_reflects_stats_after_win(mcp):
        async with Client(transport=mcp, elicitation_handler=make_elicit_handler(["go left", "open chest"])) as client:
            await client.call_tool("play_adventure", {})
            result = await client.get_prompt(PROMPT_NAME, {})
            text = result.messages[0].content.text
            assert_that(text).contains("adventure://stats")

    async def it_reflects_stats_after_loss(mcp):
        async with Client(transport=mcp, elicitation_handler=make_elicit_handler(["go right", "jump across"])) as client:
            await client.call_tool("play_adventure", {})
            result = await client.get_prompt(PROMPT_NAME, {})
            text = result.messages[0].content.text
            assert_that(text).contains("adventure://stats")
