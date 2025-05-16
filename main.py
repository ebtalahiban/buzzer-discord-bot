import discord
from discord.ext import commands
import os
import aiohttp

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

@bot.command()
async def progress(ctx, category: str = "", status: str = ""):
    discord_tag = f"{ctx.author.name}"
    webhook_url = os.getenv("MAKE_WEBHOOK_URL")

    category_clean = category.lower().strip()
    status_clean = status.lower().strip()

    if (category_clean in ["10vids", "30vids"]) and status_clean == "done":
        payload = {
            "username": discord_tag,
            "command": f"progress_{category_clean}_done"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload) as response:
                if response.status == 200:
                    if category_clean == "10vids":
                        role_name = "10vids-complete"  
                        role = discord.utils.get(ctx.guild.roles, name=role_name)
                        if role:
                            await ctx.author.add_roles(role)

                            try:
                                await ctx.author.send(
                                    "🎉 Congrats! You've completed the **10 Videos** task and have been given access to the private collab channel.\n\n"
                                    "📌 You can now proceed with the **30 Days - 30 Videos** collaboration.\n"
                                    "📝 Fill out this form to get started: https://tally.so/r/wdVEZo\n"
                                    "🗓 Your goal: Post 1 video daily for the next 30 days, following our guidelines.\n"
                                    "💰 You will earn **$10** for consistent engagement and quality content.\n\n"
                                    "📊 Track your progress here:\n"
                                    "https://docs.google.com/spreadsheets/d/1rUHybGMgBdDKRTAXnaANS65GKU1ksKHk75Qp23mEgCE/edit#gid=971032824\n\n"
                                    "✅ Once done, type `!progress 30vids done` in the private thread!"
                                )
                            except discord.Forbidden:
                                await ctx.send("⚠️ I couldn't send you a private message. Please check your DM settings.")

                    await ctx.send(
                        f"✅ `{discord_tag}`, your **{category}** progress has been marked as **Done**!\n\n"
                        f"🔍 You can check the status of your task here:\n"
                        f"https://docs.google.com/spreadsheets/d/1rUHybGMgBdDKRTAXnaANS65GKU1ksKHk75Qp23mEgCE/edit?usp=sharing\n\n"
                        f"📝 It will first show **For Review**. If there are no issues, it will proceed to **Payment Processing**, then **Paid**.\n"
                        f"💬 Also check the **Comments** column for any feedback about your content."
                    )
                else:
                    await ctx.send("⚠️ Something went wrong while updating your progress. Please try again later.")
    else:
        await ctx.send("📌 Usage: `!progress 10vids done` or `!progress 30vids done` to mark your video task as completed.")

bot.run(TOKEN)
