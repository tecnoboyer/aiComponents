import os
from pytube import YouTube
from pydub import AudioSegment
import warnings

# ====== CONFIGURATION ======
# Using relative paths
FFMPEG_DIR = os.path.join("ffmpeg", "ffmpeg-2025-04-23-git-25b0a8e295-essentials_build", "bin")
FFMPEG_PATH = os.path.abspath(os.path.join(FFMPEG_DIR, "ffmpeg.exe"))
YOUTUBE_URL = "https://www.youtube.com/watch?v=yPXvTzQUXYA"

# ====== SETUP ======
def setup():
    """Configure environment and verify requirements"""
    # Suppress pydub warning
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    
    # Verify FFmpeg exists
    if not os.path.exists(FFMPEG_PATH):
        print(f"❌ FFmpeg not found at: {FFMPEG_PATH}")
        print("Expected directory structure:")
        print("project_folder/")
        print("├── your_script.py")
        print("└── ffmpeg/")
        print("    └── ffmpeg-2025-.../")
        print("        └── bin/")
        print("            └── ffmpeg.exe")
        return False
    
    # Configure pydub
    AudioSegment.ffmpeg = FFMPEG_PATH
    os.environ["PATH"] += os.pathsep + os.path.dirname(FFMPEG_PATH)
    print(f"✅ FFmpeg configured at: {FFMPEG_PATH}")
    return True

# ====== DOWNLOAD ======
def download_youtube_audio(url, max_minutes=None):
    """Download YouTube audio and convert to MP3"""
    try:
        # Initialize YouTube
        yt = YouTube(
            url,
            use_oauth=True,
            allow_oauth_cache=True,
            on_progress_callback=lambda s, c, r: 
                print(f"⏳ Downloading... {round((1 - r/s.filesize)*100, 1)}%", end='\r')
        )
        
        # Bypass age restriction if needed
        if yt.age_restricted:
            yt.bypass_age_gate()
        
        # Get best audio stream
        stream = yt.streams.filter(
            only_audio=True,
            file_extension='mp4'
        ).order_by('abr').desc().first()
        
        if not stream:
            raise Exception("No suitable audio stream found")
        
        print(f"\n🎵 Downloading: {yt.title}")
        temp_file = stream.download(filename_prefix="temp_")
        
        # Process audio
        print("⚙ Converting to MP3...")
        audio = AudioSegment.from_file(temp_file)
        
        # Trim if specified
        if max_minutes:
            max_ms = max_minutes * 60 * 1000
            audio = audio[:max_ms] if len(audio) > max_ms else audio
        
        # Create safe filename
        output_file = "".join(c if c.isalnum() or c in " -_" else "_" for c in yt.title[:50]) + ".mp3"
        audio.export(output_file, format="mp3", bitrate="192k")
        os.remove(temp_file)
        
        print(f"✅ Saved as: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if 'temp_file' in locals() and os.path.exists(temp_file):
            os.remove(temp_file)
        return None

# ====== MAIN EXECUTION ======
if __name__ == "__main__":
    if not setup():
        exit(1)
    
    result = download_youtube_audio(YOUTUBE_URL, max_minutes=30)
    
    if not result:
        print("\n💡 Troubleshooting steps:")
        print("1. Update dependencies: pip install --upgrade pytube pydub")
        print("2. Verify FFmpeg installation")
        print("3. Try a different video URL")
        print("4. Check network connection/VPN")