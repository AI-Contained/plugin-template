"""Hello World adventure game plugin for AI-Contained."""
from fastmcp import Context


def register(mcp):
    """Register adventure game tools with the MCP server."""

    scenes = {
        "forest": "🌲 You're in a dark forest. Paths lead left and right.",
        "cave":   "🕯 You enter a cave. It's dark. A glowing chest sits in the corner.",
        "river":  "🌊 You reach a river. A small boat is tied to the bank.",
        "win":    "🏆 You found the treasure! You win!",
        "lose":   "💀 You slipped and fell into the river. Game over!",
    }

    transitions = {
        "forest": {"go left": "cave",  "go right": "river"},
        "cave":   {"open chest": "win", "go back": "forest"},
        "river":  {"take boat": "win",  "jump across": "lose", "go back": "forest"},
    }

    @mcp.tool
    async def play_adventure(ctx: Context) -> str:
        """Play a short choose-your-own-adventure game."""
        scene = "forest"
        # This appears to be ignored in agent-claude
        ctx.info("The user wants to play a game...")

        while scene not in ("win", "lose"):
            choices = list(transitions[scene].keys())
            result = await ctx.elicit(message=scenes[scene], response_type=choices)

            if result.action != "accept":
                return "Adventure abandoned."

            scene = transitions[scene][result.data]

        return scenes[scene]
