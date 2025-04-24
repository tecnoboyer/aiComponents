import os

# Get current working directory
current_dir = os.getcwd()
print(f"Current directory: {current_dir}")

# List files in current directory (to help debug)
print("Files in current directory:")
for file in os.listdir(current_dir):
    print(f" - {file}")

# Relative path to ffmpeg.exe (assuming it's in a subdirectory called 'ffmpeg')
ffmpeg_relative_path = os.path.join("ffmpeg", "ffmpeg-2025-04-23-git-25b0a8e295-essentials_build", "bin", "ffmpeg.exe")
ffmpeg_path = os.path.abspath(ffmpeg_relative_path)

# Verify if FFmpeg exists
if os.path.exists(ffmpeg_path):
    print(f"✅ FFmpeg found at: {ffmpeg_path}")
else:
    print(f"❌ FFmpeg NOT found at: {ffmpeg_path}")
    print("Please ensure the ffmpeg directory is in your project folder with this structure:")
    print("project_folder/")
    print("├── your_script.py")
    print("└── ffmpeg/")
    print("    └── ffmpeg-2025-.../")
    print("        └── bin/")
    print("            └── ffmpeg.exe")