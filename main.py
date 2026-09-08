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

# Multiple Servers Mapping
SERVERS = {
    "cs2": os.getenv("CS2_SERVER_ID"),
    "minecraft": os.getenv("MC_SERVER_ID"),
    "rust": os.getenv("RUST_SERVER_ID")
}

@bot.event
async def on_ready():
    print(f"Lo g! Bot online ho gaya hai: {bot.user}")

# 3. AI Conversational & Mazak-Masti Listener
@bot.event
async def on_message(message):
    # Bot apne hi message ka jawab de kar loop mein na phans jaye
    if message.author == bot.user:
        return

    content = message.content.lower()

    # Desi style banter aur casual chat logic
    if "kya hal hai" in content or "kesa hai" in content:
        await message.channel.send("Sab set hai boss! Tum batao, server kab aa raha hai jisay humne control karna hai? 😎")
    elif "mazak" in content or "joke" in content:
        await message.channel.send("Bhai mazak yeh hai ke hum bina VPS ke poora DevOps empire khara kar rahe hain! 😆")
    elif "bot" in content and ("kaam" in content or "kya kr skte ho" in content):
        await message.channel.send("Main tera personal DevOps agent hoon bhai! Abhi standby par hoon, VPS aate hi Pterodactyl aur servers ki aisi ki taisi ek kar denge! 🚀")

    # Yeh line lazmi hai warna commands (!start, !status waghera) kaam nahi karengi
    await bot.process_commands(message)

# 4. Server Management Commands (Multiple Servers Supported)
@bot.command(name="status")
async def server_status(ctx, server_name: str = None):
    """Kisi bhi server ka status check karne ke liye: !status cs2"""
    if not all([PTERODACTYL_URL, PTERODACTYL_API_KEY]):
        await ctx.send("⚠️ **Pterodactyl panel abhi connect nahi hai!** Par tu fikar na kar, main baaki baatein sun raha hoon.")
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
        await ctx.send("🚧 **System Notice:** VPS aur Pterodactyl aane ka intezar hai. Tab tak chill maar!")
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
        await ctx.send("🛑 Panel active nahi hai, warna abhi chala kar dikhata.")
        return
    
    if not server_name or server_name.lower() not in SERVERS:
        available = ", ".join(SERVERS.keys())
        await ctx.send(f"❌ Sahi server ka naam do. Available servers: `{available}` (Misal: `!stop cs2`)")
        return

    server_id = SERVERS[server_name.lower()]
    await ctx.send(f"🛑 Stopping **{server_name.upper()}**...")

# Bot ko run kar do
bot.run(os.getenv("DISCORD_TOKEN"))
