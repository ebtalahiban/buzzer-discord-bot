import discord
from discord.ext import commands
import os
import aiohttp

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

@bot.command()
async def progress(ctx, category: str = "", status: str = ""):
    discord_tag = f"{ctx.author.name}"
    webhook_url = os.getenv("MAKE_WEBHOOK_URL")

    if category.lower().strip() == "10vids" and status.lower().strip() == "done":
        payload = {
            "username": discord_tag,
            "command": "progress_10vids_done"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload) as response:
                if response.status == 200:
                    await ctx.send(f"✅ `{discord_tag}`, your **10 videos** progress has been marked as **Done**!")
                else:
                    await ctx.send(f"⚠️ Something went wrong while updating your progress. Please try again later.")
    else:
        await ctx.send(f"📌 Usage: `!progress 10vids done` to mark your 10 video task as completed.")

@bot.command()
async def appreview(ctx, *, task: str = ""):
    discord_tag = f"{ctx.author.name}"

    if task.lower().strip() == "done":
        webhook_url = os.getenv("MAKE_WEBHOOK_URL")
        payload = {
            "username": discord_tag,
            "command": "appreview"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload) as response:
                if response.status == 200:
                    await ctx.send(f"🌟 Thank you `{ctx.author.display_name}` for the 5-star review! We’ve marked your review as **Done** in our system.")
                else:
                    await ctx.send(f"⚠️ Something went wrong while submitting your review. Please try again later.")
    else:
        await ctx.send(f"📌 `{ctx.author.display_name}`, please use the command like this: `!appreview done` to mark your review.")


bot.run(TOKEN)
