"""Template plugin for AI-Contained."""
from fastmcp import Context


def register(mcp):
    """Register tools, resources and prompts with the MCP server."""

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

    # --- Tool ---

    @mcp.tool
    async def play_adventure(ctx: Context) -> str:
        """Play a short choose-your-own-adventure game."""
        scene = "forest"

        while scene not in ("win", "lose"):
            choices = list(transitions[scene].keys())
            result = await ctx.elicit(message=scenes[scene], response_type=choices)

            if result.action != "accept":
                return "Adventure abandoned."

            scene = transitions[scene][result.data]

        stats = await ctx.get_state("stats") or {"health": 100, "adventures": 0}
        stats["health"] = 100 if scene == "win" else 0
        stats["adventures"] += 1
        await ctx.set_state("stats", stats)

        return scenes[scene]

    # --- Resource ---

    @mcp.resource("adventure://stats", mime_type="application/json")
    async def adventure_stats(ctx: Context) -> dict:
        """Current player stats."""
        return await ctx.get_state("stats") or {"health": 100, "adventures": 0}

    # --- Prompt ---

    @mcp.prompt
    def adventure_recap() -> str:
        """Generate a recap based on the player's stats."""
        return (
            "Read adventure://stats then write a short dramatic recap of the player's journey. "
            "If health is 0, make it a tale of defeat. If 100, a tale of triumph."
        )
