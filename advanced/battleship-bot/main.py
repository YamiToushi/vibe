"""
Battleship Bot — Discord interface
Commands:
  bb help       — show rules
  bb start      — start a new game
  bb shoot r,c  — fire at cell (1-10, 1-10)
  bb surrender  — give up and reveal the fleet
"""
import os
import discord
from dotenv import load_dotenv

from game import (
    BattleshipGame, SHIPS,
    RESULT_ALREADY_SHOT, RESULT_MISS, RESULT_HIT,
    RESULT_SUNK, RESULT_WIN, RESULT_INVALID,
)
import board as renderer

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ── Colours ───────────────────────────────────────────────────────────────────
C_BLUE   = 0x89B4FA
C_GREEN  = 0xA6E3A1
C_YELLOW = 0xF9E2AF
C_RED    = 0xF38BA8
C_PEACH  = 0xFAB387
C_GRAY   = 0x6C7086

# ── Per-user game state ───────────────────────────────────────────────────────
games: dict[int, BattleshipGame] = {}   # user_id → game

# ── Discord client ────────────────────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
client  = discord.Client(intents=intents)


# ═══════════════════════════════════════════════════════════ Embed helpers ════

def _embed(title: str, desc: str, color: int,
           board: BattleshipGame | None = None,
           reveal: bool = False,
           extra_fields: list[tuple[str, str, bool]] | None = None
           ) -> discord.Embed:
    e = discord.Embed(title=title, description=desc, color=color)
    if board is not None:
        grid_str = renderer.render(board, reveal=reveal)
        e.add_field(name="🗺️  Battle Grid", value=grid_str, inline=False)
        fleet_str = renderer.fleet_status_text(board)
        e.add_field(name="🚢  Fleet Status", value=fleet_str, inline=True)
        stats = (
            f"Shots fired: **{board.total_shots}**\n"
            f"Accuracy: **{board.accuracy():.0f}%**\n"
            f"Ships sunk: **{board.ships_sunk}/{len(board.ships)}**"
        )
        e.add_field(name="📊  Stats", value=stats, inline=True)
    if extra_fields:
        for name, value, inline in extra_fields:
            e.add_field(name=name, value=value, inline=inline)
    return e


# ═══════════════════════════════════════════════════════════ Command handlers ═

async def cmd_help(msg: discord.Message):
    ships_list = "\n".join(
        f"• **{name}** — {size} cells" for name, size in SHIPS
    )
    desc = (
        "⚓ **Battleship** — sink the hidden fleet before running out of guesses!\n\n"
        "The bot secretly places **5 ships** on a 10×10 grid. "
        "Your job is to find and sink them all.\n"
    )
    commands = (
        "`bb help`           — show this help\n"
        "`bb start`          — start a new game (resets existing game)\n"
        "`bb shoot r,c`      — fire at row r, column c  *(1–10)*\n"
        "`bb surrender`      — give up & reveal the fleet\n\n"
        "**Examples:**\n"
        "`bb shoot 3,7`  •  `bb shoot 10,1`"
    )
    legend = (
        f"{renderer.OCEAN} — unknown water\n"
        f"{renderer.HIT}   — hit!\n"
        f"{renderer.MISS}  — miss\n"
        f"{renderer.SHIP}  — revealed ship\n"
        f"{renderer.SUNK}  — sunk ship cell"
    )
    embed = _embed("📖  Battleship — Rules & Commands", desc, C_BLUE,
                   extra_fields=[
                       ("⚓  Fleet", ships_list, True),
                       ("🎮  Commands", commands, False),
                       ("🗺️  Legend", legend, True),
                   ])
    await msg.channel.send(embed=embed)


async def cmd_start(msg: discord.Message, user_id: int):
    games[user_id] = BattleshipGame()
    game = games[user_id]
    desc = (
        f"A new fleet of **{len(game.ships)} ships** has been hidden on the grid.\n"
        "Use `bb shoot r,c` to fire — good luck, Admiral! 🎯"
    )
    await msg.channel.send(
        embed=_embed("⚓  New Game Started!", desc, C_GREEN, board=game)
    )


async def cmd_shoot(msg: discord.Message, user_id: int, coord_str: str):
    if user_id not in games or games[user_id].over:
        await msg.channel.send(
            "No active game. Start one with `bb start`.", delete_after=8
        )
        return

    game = games[user_id]

    # ── Parse coordinates ─────────────────────────────────────────────────────
    try:
        parts = coord_str.split(",")
        if len(parts) != 2:
            raise ValueError
        r_user, c_user = int(parts[0].strip()), int(parts[1].strip())
        if not (1 <= r_user <= 10 and 1 <= c_user <= 10):
            raise ValueError
    except ValueError:
        await msg.channel.send(
            "⚠️  Invalid coordinates. Use `bb shoot r,c` where r and c are **1–10**.\n"
            "Example: `bb shoot 4,7`",
            delete_after=10,
        )
        return

    r, c = r_user - 1, c_user - 1   # convert to 0-indexed
    result, ship = game.shoot(r, c)

    # ── Build response ────────────────────────────────────────────────────────
    if result == RESULT_ALREADY_SHOT:
        await msg.channel.send(
            f"⚠️  You already targeted **({r_user}, {c_user})**. Try a different cell.",
            delete_after=8,
        )
        return

    if result == RESULT_MISS:
        embed = _embed(
            f"💦  Miss! ({r_user}, {c_user})",
            "The shot splashed harmlessly into the ocean.",
            C_BLUE, board=game,
        )

    elif result == RESULT_HIT:
        embed = _embed(
            f"💥  Hit! ({r_user}, {c_user})",
            f"Direct hit on the **{ship.name}**! Keep firing! 🎯",
            C_YELLOW, board=game,
        )

    elif result == RESULT_SUNK:
        embed = _embed(
            f"🔥  {ship.name} Sunk! ({r_user}, {c_user})",
            (
                f"You sank the **{ship.name}**! 💀\n"
                f"**{game.ships_remaining}** ship(s) remaining."
            ),
            C_PEACH, board=game,
        )

    elif result == RESULT_WIN:
        embed = _embed(
            "🏆  Victory! All Ships Destroyed!",
            (
                f"Congratulations, **{msg.author.display_name}**! 🎉\n"
                f"You sank the entire fleet in **{game.total_shots}** shots "
                f"with **{game.accuracy():.0f}%** accuracy!\n\n"
                "Here's the full battle map:"
            ),
            C_GREEN, board=game, reveal=True,
        )
        del games[user_id]
        await msg.channel.send(embed=embed)
        return

    else:  # RESULT_INVALID (shouldn't reach here after coord check)
        await msg.channel.send("⚠️  Invalid coordinates.", delete_after=8)
        return

    await msg.channel.send(embed=embed)


async def cmd_surrender(msg: discord.Message, user_id: int):
    if user_id not in games or games[user_id].over:
        await msg.channel.send(
            "No active game to surrender. Start one with `bb start`.",
            delete_after=8,
        )
        return

    game = games.pop(user_id)
    embed = _embed(
        "🏳️  You Surrendered",
        (
            f"Better luck next time, **{msg.author.display_name}**. 😔\n"
            f"You fired **{game.total_shots}** shots and sank "
            f"**{game.ships_sunk}/{len(game.ships)}** ships.\n\n"
            "Here's where the fleet was hiding:"
        ),
        C_RED, board=game, reveal=True,
    )
    await msg.channel.send(embed=embed)


# ═══════════════════════════════════════════════════════════ Event handlers ═══

@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Game(name="Battleship | bb help")
    )
    print(f"✅  Battleship Bot ready — logged in as {client.user} (ID: {client.user.id})")


@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    content = message.content.strip()
    if not content.lower().startswith("bb "):
        return

    tokens = content.split()
    if len(tokens) < 2:
        return

    cmd      = tokens[1].lower()
    user_id  = message.author.id

    match cmd:
        case "help":
            await cmd_help(message)

        case "start":
            await cmd_start(message, user_id)

        case "shoot":
            coord = tokens[2] if len(tokens) >= 3 else ""
            await cmd_shoot(message, user_id, coord)

        case "surrender":
            await cmd_surrender(message, user_id)

        case _:
            await message.channel.send(
                f"❓  Unknown command `{cmd}`. Type `bb help` for the command list.",
                delete_after=8,
            )


# ═══════════════════════════════════════════════════════════ Entry point ══════

if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit(
            "❌  DISCORD_TOKEN not found.\n"
            "    Copy .env.example → .env and fill in your bot token."
        )
    client.run(TOKEN)
