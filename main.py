from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
import yt_dlp
import os

API_ID = 39519158
API_HASH = "REPLACE_API_HASH"
BOT_TOKEN = "REPLACE_BOT_TOKEN"

app = Client(
    "kingsmusic",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

voice = PyTgCalls(app)

def download_song(song_name):
    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "song.%(ext)s",
        "quiet": True,
        "default_search": "ytsearch1",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([song_name])
    return "song.webm"

@app.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply(
        "🎶 Kings Live Music Bot Ready!\n"
        "Use:\n/play song name\n/stop"
    )

@app.on_message(filters.command("play"))
async def play(_, msg):
    if len(msg.command) < 2:
        await msg.reply("Song ka naam likho. Example: /play tum hi ho")
        return

    song_name = " ".join(msg.command[1:])
    await msg.reply("🔍 Song search ho raha hai...")

    file_path = download_song(song_name)

    chat_id = msg.chat.id
    await voice.join_group_call(
        chat_id,
        AudioPiped(file_path)
    )

    await msg.reply(f"▶️ Ab chal raha hai: {song_name}")

@app.on_message(filters.command("stop"))
async def stop(_, msg):
    chat_id = msg.chat.id
    await voice.leave_group_call(chat_id)
    if os.path.exists("song.webm"):
        os.remove("song.webm")
    await msg.reply("⏹ Music stop kar diya")

voice.start()
app.run()
