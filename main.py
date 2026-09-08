import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord.ext import commands

# 1. Dummy Web Server taake Railway ka health check pass rahe aur container band na ho
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
SERVER_ID = os.getenv("SERVER_ID")

@bot.event
async def on_ready():
    print(f"Lo g! Bot online ho gaya hai: {bot.user}")

@bot.command(name="status")
async def server_status(ctx):
    """Check karega ke server ka kya haal hai"""
    if not all([PTERODACTYL_URL, PTERODACTYL_API_KEY, SERVER_ID]):
        await ctx.send("⚠️ **Pterodactyl panel abhi connect nahi hai!** Jab VPS aa jaye ga aur variables set ho jayenge, tab yeh live status dikhane lagega.")
        return
    
    # Jab VPS aa jayega, yahan Pterodactyl API call aayegi
    await ctx.send("🔍 Pterodactyl API se connection establish ho raha hai...")

@bot.command(name="start")
async def server_start(ctx):
    """CS2 server start karne ki command"""
    if not all([PTERODACTYL_URL, PTERODACTYL_API_KEY, SERVER_ID]):
        await ctx.send("🚧 **System Notice:** VPS aur Pterodactyl configure hone ka intezar hai. Tab tak yeh command offline mode par hai!")
        return
    
    await ctx.send("🚀 Server start kiya ja raha hai...")

@bot.command(name="stop")
async def server_stop(ctx):
    """CS2 server stop karne ki command"""
    if not all([PTERODACTYL_URL, PTERODACTYL_API_KEY, SERVER_ID]):
        await ctx.send("🛑 Panel active nahi hai, isliye server stop nahi ho sakta.")
        return
    
    await ctx.send("🛑 Server safely stop ho raha hai...")

# Bot ko run kar do
bot.run(os.getenv("DISCORD_TOKEN"))
