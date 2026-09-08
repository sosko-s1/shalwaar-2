import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord.ext import commands
import google.generativeai as genai

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

# 2. Google Gemini AI Setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # Gemini model initialize kar rahe hain
    ai_model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="You are a smart, funny, desi, and tech-savvy DevOps & gaming AI assistant on Discord. You chat with the user in a mix of Roman Urdu and English, keep the vibe chill and friendly, and help them with servers, coding, and general tech talk."
    )
else:
    ai_model = None

# 3. Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Pterodactyl Configuration Variables (Future Ready)
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

    # Agar message command hai (! se shuru hota hai) toh usay commands ke liye pass kar do
    if message.content.startswith("!"):
        await bot.process_commands(message)
        return

    # Agar aam baat hai, toh seedha Gemini AI ko bhej do!
    if ai_model:
        try:
            # Typing indicator show karega taake lage ke AI soch raha hai
            async with message.channel.typing():
                response = ai_model.generate_content(message.content)
                await message.channel.send(response.text)
        except Exception as e:
            await message.channel.send("Bhai, AI brain thori der ke liye hang ho gaya hai, dubara try kar! 😅")
    else:
        await message.channel.send("⚠️ Railway variables mein `GEMINI_API_KEY` set karna bhool gaye ho boss!")

    await bot.process_commands(message)

# 5. Server Management Commands
@bot.command(name="status")
async def server_status(ctx, server_name: str = None):
    if not all([PTERODACTYL_URL, PTERODACTYL_API_KEY]):
        await ctx.send("⚠️ **Pterodactyl panel abhi connect nahi hai!** Par baaki baatein AI ke sath kar sakta hai.")
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

# Bot run kar do
bot.run(os.getenv("DISCORD_TOKEN"))
