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

    if (category.lower().strip() == "10vids" or category.lower().strip() == "30vids") and status.lower().strip() == "done":
        payload = {
            "username": discord_tag,
            "command": f"progress_{category.lower().strip()}_done"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload) as response:
                if response.status == 200:
                    await ctx.send(
                        f"✅ `{discord_tag}`, your **{category}** progress has been marked as **Done**!\n\n"
                        f"🔍 You can check the status of your task here:\n"
                        f"https://docs.google.com/spreadsheets/d/1rUHybGMgBdDKRTAXnaANS65GKU1ksKHk75Qp23mEgCE/edit?usp=sharing\n\n"
                        f"📝 It will first show **For Review**. If there are no issues, it will proceed to **Payment Processing**, then **Paid**.\n"
                        f"💬 Also check the **Comments** column for any feedback about your content."
                    )
                else:
                    await ctx.send(f"⚠️ Something went wrong while updating your progress. Please try again later.")
    else:
        await ctx.send(f"📌 Usage: `!progress 10vids done` or `!progress 30vids done` to mark your video task as completed.")

bot.run(TOKEN)
