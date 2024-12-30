import nextcord
from nextcord.ext import commands
import asyncio
import config

# Initialize the bot with a command prefix and intents
bot = commands.Bot(command_prefix="/", intents=nextcord.Intents.all())

# Class to manage radio playback
class RadioPlayer:
    def __init__(self, voice_client):
        self.voice_client = voice_client  # The active voice connection
        self.is_playing = False  # Status to track if radio is playing

    async def play_radio(self):
        """Starts streaming the HitFM radio."""
        self.is_playing = True

        # URL of the radio stream
        radio_stream_url = "https://online.hitfm.ua/HitFM_HD"

        # Options for FFmpeg to process the audio
        ffmpeg_options = {'options': '-vn'}  # -vn disables video processing
        self.voice_client.play(
            nextcord.FFmpegPCMAudio(radio_stream_url, **ffmpeg_options),
            after=lambda e: asyncio.run_coroutine_threadsafe(self.after_playback(), bot.loop)
        )

    async def after_playback(self):
        """Handles tasks after radio playback ends."""
        self.is_playing = False


# Class to manage music playback
class MusicPlayer:
    def __init__(self, voice_client):
        self.voice_client = voice_client  # The active voice connection
        self.queue = asyncio.Queue()  # Queue to manage song URLs
        self.current = None  # Currently playing song
        self.is_playing = False  # Status to track if music is playing

    async def play_next(self):
        """Plays the next song in the queue."""
        if self.queue.empty():
            self.is_playing = False  # No more songs to play
            return

        self.is_playing = True
        self.current = await self.queue.get()  # Retrieve the next song from the queue

        # Options for FFmpeg to process the audio
        ffmpeg_options = {'options': '-vn'}
        self.voice_client.play(
            nextcord.FFmpegPCMAudio(self.current, **ffmpeg_options),
            after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), bot.loop)
        )


# Dictionaries to store active players for each server (guild)
radio_players = {}
music_players = {}

@bot.event
async def on_ready():
    """Logs a message when the bot is ready to use."""
    print(f"Bot launched as {bot.user}. Ready to serve!")


# Radio Commands
@bot.slash_command(name="play_radio", description="🎶 Play HitFM radio in a voice channel.")
async def play_radio(interaction: nextcord.Interaction):
    """Command to play HitFM radio in a voice channel."""
    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message("📢 Please join a voice channel first!")
        return

    await interaction.response.defer()  # Indicate that the command is being processed

    guild_id = interaction.guild.id
    if guild_id not in radio_players:
        # Connect to the user's voice channel if not already connected
        voice_client = await interaction.user.voice.channel.connect()
        radio_players[guild_id] = RadioPlayer(voice_client)

    player = radio_players[guild_id]

    if not player.is_playing:
        await player.play_radio()  # Start playing the radio
        await interaction.followup.send("🎶 HitFM is now playing!")
    else:
        await interaction.followup.send("🎵 The radio is already playing.")


@bot.slash_command(name="stop_radio", description="🛑 Stop HitFM radio.")
async def stop_radio(interaction: nextcord.Interaction):
    """Command to stop HitFM radio playback."""
    guild_id = interaction.guild.id
    if guild_id in radio_players:
        player = radio_players[guild_id]
        if player.voice_client:
            await player.voice_client.disconnect()  # Disconnect from the voice channel
            del radio_players[guild_id]  # Remove the player from the dictionary
            await interaction.response.send_message("🛑 Radio has been stopped.")
    else:
        await interaction.response.send_message("❌ No radio is currently playing.")


# Music Commands
@bot.slash_command(name="play_music", description="🎵 Play a music track from a URL.")
async def play_music(interaction: nextcord.Interaction, url: str):
    """Command to play music from a given URL."""
    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message("📢 Please join a voice channel first!")
        return

    await interaction.response.defer()

    guild_id = interaction.guild.id
    if guild_id not in music_players:
        # Connect to the user's voice channel if not already connected
        voice_client = await interaction.user.voice.channel.connect()
        music_players[guild_id] = MusicPlayer(voice_client)

    player = music_players[guild_id]

    await player.queue.put(url)  # Add the song URL to the queue
    if not player.is_playing:
        await player.play_next()  # Start playback if not already playing
        await interaction.followup.send(f"🎶 Now playing: {url}")
    else:
        await interaction.followup.send(f"✅ Added to queue: {url}")


@bot.slash_command(name="skip_music", description="⏭ Skip the current music track.")
async def skip_music(interaction: nextcord.Interaction):
    """Command to skip the currently playing music track."""
    guild_id = interaction.guild.id
    if guild_id in music_players:
        player = music_players[guild_id]
        if player.voice_client.is_playing():
            player.voice_client.stop()  # Stop the current track
            await interaction.response.send_message("⏭ Track skipped.")
        else:
            await interaction.response.send_message("❌ No music is currently playing.")
    else:
        await interaction.response.send_message("❌ The queue is empty.")


@bot.slash_command(name="stop_music", description="🛑 Stop music playback.")
async def stop_music(interaction: nextcord.Interaction):
    """Command to stop music playback and clear the queue."""
    guild_id = interaction.guild.id
    if guild_id in music_players:
        player = music_players[guild_id]
        if player.voice_client:
            await player.voice_client.disconnect()  # Disconnect from the voice channel
            del music_players[guild_id]  # Remove the player from the dictionary
            await interaction.response.send_message("🛑 Music playback stopped.")
    else:
        await interaction.response.send_message("❌ No music is currently playing.")


@bot.slash_command(name="queue_music", description="🎶 Show the music queue.")
async def queue_music(interaction: nextcord.Interaction):
    """Command to display the current music queue."""
    guild_id = interaction.guild.id
    if guild_id in music_players:
        player = music_players[guild_id]
        queue_list = list(player.queue._queue)  # Get the list of queued songs
        if queue_list:
            queue_str = "\n".join([f"{i + 1}. {song}" for i, song in enumerate(queue_list)])
            await interaction.response.send_message(f"🎵 Music Queue:\n{queue_str}")
        else:
            await interaction.response.send_message("❌ The queue is empty.")
    else:
        await interaction.response.send_message("❌ No active music player.")

# Run the bot with the token from the configuration
bot.run(config.token)
