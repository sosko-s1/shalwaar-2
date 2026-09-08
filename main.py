import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord.ext import commands

# 1. Dummy Web Server taake Railway ka health check pass rahe
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive and ready!")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

server_thread = threading.Thread(target=run_server)
server_thread.daemon = True
server_thread.start()

# 2. Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Pterodactyl Configuration Variables (Future Ready)
PTERODACTYL_URL = os.getenv("PTERODACTYL_URL")
PTERODACTYL_API_KEY = os.getenv("PTERODACTYL_API_KEY")

# Multiple Servers Mapping (Yahan tum apne alag-alag servers ke naam aur unki IDs define kar sakoge)
SERVERS = {
    "cs2": os.getenv("CS2_SERVER_ID"),
    "minecraft": os.getenv("MC_SERVER_ID"),
    "rust": os.getenv("RUST_SERVER_ID")
}

@bot.event
async def on_ready():
    print(f"Lo g! Bot online ho gaya hai: {bot.user}")

@bot.command(name="status")
async def server_status(ctx, server_name: str = None):
    """Kisi bhi server ka status check karne ke liye: !status cs2"""
    if not all([PTERODACTYL_URL, PTERODACTYL_API_KEY]):
        await ctx.send("⚠️ **Pterodactyl panel abhi connect nahi hai!**")
        return
    
    if not server_name or server_name.lower() not in SERVERS:
        available = ", ".join(SERVERS.keys())
        await ctx.send(f"❌ Sahi server ka naam do. Available servers: `{available}` (Misal: `!status cs2`)")
        return

    server_id = SERVERS[server_name.lower()]
    await ctx.send(f"🔍 Checking status for **{server_name.upper()}** (ID: {server_id})...")

@bot.command(name="start")
async def server_start(ctx, server_name: str = None):
    """Server start karne ke liye: !start cs2"""
    if not all([PTERODACTYL_URL, PTERODACTYL_API_KEY]):
        await ctx.send("🚧 **System Notice:** VPS aur Pterodactyl configure hone ka intezar hai.")
        return
    
    if not server_name or server_name.lower() not in SERVERS:
        available = ", ".join(SERVERS.keys())
        await ctx.send(f"❌ Sahi server ka naam do. Available servers: `{available}` (Misal: `!start cs2`)")
        return

    server_id = SERVERS[server_name.lower()]
    await ctx.send(f"🚀 Starting **{server_name.upper()}**...")

@bot.command(name="stop")
async def server_stop(ctx, server_name: str = None):
    """Server stop karne ke liye: !stop cs2"""
    if not all([PTERODACTYL_URL, PTERODACTYL_API_KEY]):
        await ctx.send("🛑 Panel active nahi hai.")
        return
    
    if not server_name or server_name.lower() not in SERVERS:
        available = ", ".join(SERVERS.keys())
        await ctx.send(f"❌ Sahi server ka naam do. Available servers: `{available}` (Misal: `!stop cs2`)")
        return

    server_id = SERVERS[server_name.lower()]
    await ctx.send(f"🛑 Stopping **{server_name.upper()}**...")

# Bot ko run kar do
bot.run(os.getenv("DISCORD_TOKEN"))
