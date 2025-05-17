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
async def progress(ctx, category: str = "", status: str = "", buzzer_username: str = ""):
    if not category or not status or not buzzer_username:
        await ctx.send(
            "📌 Usage: `!progress 10collab done buzzer_username`, `!progress 30collab done buzzer_username`,\n"
            "or `!progress 10vids done buzzer_username`, `!progress 30vids done buzzer_username`"
        )
        return

    aliases = {
        "10collab": "10vids",
        "30collab": "30vids",
        "10vids": "10vids",
        "30vids": "30vids"
    }

    category_key = category.lower().strip()
    category_mapped = aliases.get(category_key)

    if not category_mapped or status.lower().strip() != "done":
        await ctx.send(
            "📌 Usage: `!progress 10collab done buzzer_username`, `!progress 30collab done buzzer_username`,\n"
            "or `!progress 10vids done buzzer_username`, `!progress 30vids done buzzer_username`"
        )
        return

    webhook_url = os.getenv("MAKE_WEBHOOK_URL")
    payload = {
        "command": "progress",
        "task": category_key,
        "buzzer_username": buzzer_username.strip()
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as response:
            if response.status == 200:
                try:
                    dm_message = (
                        f"✅ Your **{category_mapped}** progress for Buzzer account `{buzzer_username}` has been submitted successfully!\n\n"
                        f"🔍 You can check your task status here:\n"
                        f"https://docs.google.com/spreadsheets/d/1rUHybGMgBdDKRTAXnaANS65GKU1ksKHk75Qp23mEgCE/edit?usp=sharing\n\n"
                        f"📝 First it will show **For Review**. If there are no issues, it will move to **Payment Processing**, then **Paid**.\n"
                        f"💬 Check the **Comments** column for any feedback.\n"
                        f":money_with_wings: **You’ll earn $10** once your videos are reviewed and approved.\n"
                    )

                    guild = ctx.guild

                    if category_key in ["10vids", "10collab"]:
                        role_10_complete = discord.utils.get(guild.roles, name="10vids-complete")
                        if role_10_complete:
                            await ctx.author.add_roles(role_10_complete)

                    await ctx.author.send(dm_message)
                    await ctx.send(f"📩 `{ctx.author.name}`, I’ve sent you a DM with the next steps.")
                except discord.Forbidden:
                    await ctx.send("⚠️ I couldn't send you a DM. Please make sure your DMs are enabled.")
            else:
                await ctx.send("⚠️ Something went wrong while updating your progress. Please try again later.")

@bot.command()
async def claim(ctx, task: str = "", buzzer_username: str = ""):
    user = ctx.author
    task = task.lower().strip()
    buzzer_username = buzzer_username.strip()

    valid_tasks = {
        "10collab": "$10-10vids-collab",
        "30collab": "$30-30vids-collab"
    }

    if task not in valid_tasks:
        await ctx.send("📌 Usage: `!claim 10collab <buzzer_username>` or `!claim 30collab <buzzer_username>`")
        return

    role_name = valid_tasks[task]
    webhook_url = os.getenv("MAKE_WEBHOOK_URL")

    payload = {
        "command": "claim",
        "task": task,
        "buzzer_username": buzzer_username
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                if data.get("valid"):
                    role = discord.utils.get(ctx.guild.roles, name=role_name)
                    if role:
                        await user.add_roles(role)
                        await user.send(f"✅ You've been given access to **{role_name}**. Welcome to the collab!")
                        await ctx.send(f"✅ `{user.name}` has been granted the **{role_name}** role.")
                    else:
                        await ctx.send(f"❌ Role `{role_name}` not found.")
                else:
                    await ctx.send(f"❌ Buzzer username `{buzzer_username}` is not part of the {task} collaborator list.")
            else:
                await ctx.send("⚠️ Something went wrong while verifying your Buzzer username. Please try again later.")

bot.run(TOKEN)
