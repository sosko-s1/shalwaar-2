import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord.ext import commands
from google import genai

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

# 2. Google GenAI Setup & Model Discovery
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    ai_client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Check karne ke liye ke is AQ key par kon se models available hain
    try:
        print("🔍 Checking available models for this AQ key...")
        for m in ai_client.models.list():
            print(f"Supported Model: {m.name}")
    except Exception as e:
        print(f"Model list error: {e}")
else:
    ai_client = None

# 3. Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

PTERODACTYL_URL = os.getenv("PTERODACTYL_URL")
PTERODACTYL_API_KEY = os.getenv("PTERODACTYL_API_KEY")

SERVERS = {
    "cs2": os.getenv("CS2_SERVER_ID"),
    "minecraft": os.getenv("MC_SERVER_ID"),
    "rust": os.getenv("RUST_SERVER_ID")
}

@bot.event
async def on_ready():
    print(f"Lo g! AI DevOps Agent online ho gaya hai: {bot.user}")

# 4. AI Brain + Message Handler
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("!"):
        await bot.process_commands(message)
        return

    if ai_client:
        try:
            async with message.channel.typing():
                # Yahan hum 'gemini-2.5-flash' ya jo logs mein show ho usay try kar rahe hain
                response = ai_client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=message.content,
                )
                await message.channel.send(response.text)
        except Exception as e:
            print(f"Gemini Error: {e}")
            await message.channel.send(f"Bhai, AI error agya hai: `{e}` 😅")
    else:
        await message.channel.send("⚠️ Railway variables mein `GEMINI_API_KEY` set nahi hai!")

    await bot.process_commands(message)

# 5. Server Management Commands
@bot.command(name="status")
async def server_status(ctx, server_name: str = None):
    if not all([PTERODACTYL_URL, PTERODACTYL_API_KEY]):
        await ctx.send("⚠️ **Pterodactyl panel abhi connect nahi hai!**")
        return
    
    if not server_name or server_name.lower() not in SERVERS:
        available = ", ".join(SERVERS.keys())
        await ctx.send(f"❌ Sahi server ka naam do. Available: `{available}`")
        return

    server_id = SERVERS[server_name.lower()]
    await ctx.send(f"🔍 Checking status for **{server_name.upper()}** (ID: {server_id})...")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong! AI agent bilkul high speed par chal raha hai. ⚡")

bot.run(os.getenv("DISCORD_TOKEN"))
