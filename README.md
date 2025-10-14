# DJ Set Builder & SoundCloud Downloader

## Overview
This project automates the process of downloading tracks from SoundCloud, analyzing their musical features, and building a DJ set with AI-powered recommendations.

## Features
- Download individual tracks or playlists from SoundCloud using yt-dlp
- Analyze downloaded MP3s for BPM, musical key, and energy
- Summarize and recommend DJ set order using an LLM (OpenAI)
- Modular workflow: downloader, analyzer, summarizer, and agent orchestrator
- Environment variable support via `.env` file

## Setup
1. **Clone the repository**
2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   pip install yt-dlp ffmpeg-python librosa python-dotenv langchain-openai
   ```
3. **Set your OpenAI API key**:
   - Copy `.env.example` to `.env` and add your key:
     ```
     cp .env.example .env
     # Edit .env and add your OpenAI API key
     OPENAI_API_KEY=sk-YourOpenAIKeyHere
     ```

## Usage
### Download and Build DJ Set
Run the agent script with a SoundCloud URL and output directory:
```sh
python -m app.dj_set_agent "<soundcloud_url>" "<output_dir>"
```

### Example
```sh
python -m app.dj_set_agent "https://soundcloud.com/youruser/sets/yourset" "./downloads"
```

## Project Structure
```
app/
  track_downloader.py   # Downloads tracks/playlists
  track_analyzer.py     # Analyzes BPM, key, energy
  track_summarizer.py   # Summarizes DJ set with LLM
  dj_set_agent.py       # Orchestrates workflow
  __init__.py
.env                    # API keys and environment variables
requirements.txt        # Python dependencies
```

## Customization
- You can adjust analysis parameters in `track_analyzer.py`.
- The summary prompt can be edited in `track_summarizer.py` for different DJ set logic.

## Troubleshooting
- Ensure all dependencies are installed and your `.env` file contains a valid OpenAI API key.
- If you see errors about missing packages, run `pip install` for the required modules.
- For ffmpeg issues, ensure ffmpeg is installed and available in your system PATH.

## License
MIT
