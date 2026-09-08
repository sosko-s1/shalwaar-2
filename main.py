import os
import discord
from discord.ext import commands

# Intents set kar rahe hain
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Lo g! Bot online ho gaya hai: {bot.user}')

@bot.command(name='ping')
async def ping(ctx):
    """Test command"""
    await ctx.send("Pong! Bot बिल्कुल theek kaam kar raha hai.")

# Render ke environment variable se token uthayega
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: DISCORD_TOKEN nahi mila!")
    
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import discord

# Dummy server taake Railway ka health check pass rahe
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_server():
    server = HTTPServer(('0.0.0.0', 8080), SimpleHandler)
    server.serve_forever()

# Server ko background thread mein chala do
server_thread = threading.Thread(target=run_server)
server_thread.daemon = True
server_thread.start()

# Yahan se tumhara apna discord bot ka code shuru hota hai
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Lo g! Bot online ho gaya hai: {client.user}")

client.run(os.getenv("DISCORD_TOKEN"))
