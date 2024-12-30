# Discord Radio & Music Bot

🎵 A feature-rich Discord bot that streams **HitFM Radio** and plays music from user-provided URLs in voice channels. Built using the **Nextcord** library, this bot is perfect for community servers looking to enhance their voice channels with seamless audio streaming and music playback.

## Features
- **HitFM Radio Playback**: Stream your favorite radio station directly into a voice channel.
- **Music Playback**: Play songs from any URL that supports audio streaming.
- **Queue Management**: Add tracks to a queue and manage playback order.
- **Skip Tracks**: Skip the currently playing track.
- **Stop Playback**: Disconnect from the voice channel and stop all playback.

## Installation

1. **Clone this repository**:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Install the required Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install** <ins>FFmpeg</ins> *(required for audio streaming)*:
   - Download from [FFmpeg.org](https://ffmpeg.org/).
   - Follow the installation instructions for your operating system.

4. **Create a `config.py` file** in the project directory and add your bot token:
   ```python
   token = "YOUR_BOT_TOKEN"
   ```

## Usage

1. **Run the bot**:
   ```bash
   python bot.py
   ```

2. **Invite the bot** to your Discord server using the OAuth2 URL from the Discord Developer Portal.

3. **Use the following slash commands**:
   - `/play_radio` - **Play HitFM radio** in the voice channel.
   - `/stop_radio` - **Stop the radio playback**.
   - `/play_music <url>` - **Play a song from the specified URL**.
   - `/skip_music` - **Skip the currently playing track**.
   - `/stop_music` - **Stop all music playback and disconnect** from the voice channel.
   - `/queue_music` - **Display the current music queue**.

## Requirements

- **Python 3.8** or higher
- **Nextcord** library *(see `requirements.txt`)*
- **FFmpeg** installed on your system

## Example Commands

- **Play HitFM radio**:
  ```
  /play_radio
  ```

- **Play a song from a URL**:
  ```
  /play_music https://example.com/song.mp3
  ```

- **Show the queue**:
  ```
  /queue_music
  ```

## Contributing

**Contributions are welcome!** Feel free to submit issues or pull requests to improve the bot.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

