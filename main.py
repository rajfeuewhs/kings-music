import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
import yt_dlp

# ===== ENV VARIABLES (Render se aayenge) =====
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ===== Telegram Client =====
app = Client(
    "kings_music",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

voice = PyTgCalls(app)

# ===== Song Download Function =====
def download_song(song_name):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "song.%(ext)s",
        "quiet": True,
        "default_search": "ytsearch1",
        "noplaylist": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([song_name])
    return "song.webm"

# ===== Commands =====
@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply(
        "🎶 **Kings Live Music Bot Ready**\n\n"
        "Commands:\n"
        "/play <song name>\n"
        "/stop"
    )

@app.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        await message.reply("❌ Song ka naam likho\nExample: `/play tum hi ho`")
        return

    song_name = " ".join(message.command[1:])
    await message.reply("🔍 Song search ho raha hai...")

    file_path = download_song(song_name)

    await voice.join_group_call(
        message.chat.id,
        AudioPiped(file_path)
    )

    await message.reply(f"▶️ **Now Playing:** {song_name}")

@app.on_message(filters.command("stop"))
async def stop(_, message):
    await voice.leave_group_call(message.chat.id)
    await message.reply("⏹ Music stop kar diya")

# ===== Start Bot =====
voice.start()
app.run()
