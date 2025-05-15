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
async def progress(ctx, *, task: str):
    discord_tag = f"{ctx.author.name}"

    if task.lower().strip() == "done":
        webhook_url = os.getenv("MAKE_WEBHOOK_URL")
        payload = {
            "username": discord_tag,
            "command": "progress_done"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload) as response:
                if response.status == 200:
                    await ctx.send(f"✅ `{discord_tag}`, your progress has been marked as **Done**!")
                else:
                    await ctx.send(f"⚠️ Something went wrong while updating progress. Please try again later.")
    else:
        await ctx.send(f"📌 Got it, `{ctx.author.display_name}`! You submitted: **{task}**. Our team will review it shortly.")

@bot.command()
async def appreview(ctx):
    await ctx.send(f"🌟 Thank you `{ctx.author.display_name}` for the 5-star review! We truly appreciate your support. 💖")

bot.run(TOKEN)
