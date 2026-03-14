#!/usr/bin/env python3
"""
Diagnostic script to check video playback dependencies
"""
import subprocess
import sys
import os

def check_ffmpeg():
    """Check if ffmpeg is installed and accessible"""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        print("✅ FFmpeg is installed!")
        print(f"Version: {result.stdout.split()[2] if result.stdout else 'Unknown'}")
        return True
    except FileNotFoundError:
        print("❌ FFmpeg is NOT installed or not in PATH")
        return False
    except Exception as e:
        print(f"❌ Error checking ffmpeg: {e}")
        return False

def check_ffprobe():
    """Check if ffprobe is installed"""
    try:
        result = subprocess.run(
            ["ffprobe", "-version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        print("✅ FFprobe is installed!")
        return True
    except FileNotFoundError:
        print("❌ FFprobe is NOT installed or not in PATH")
        return False
    except Exception as e:
        print(f"❌ Error checking ffprobe: {e}")
        return False

def check_python_packages():
    """Check required Python packages"""
    required = [
        "ffmpeg-python",
        "py-tgcalls",
        "ntgcalls"
    ]
    
    print("\n📦 Checking Python packages...")
    for package in required:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is NOT installed")

def check_system_info():
    """Display system information"""
    print("\n💻 System Information:")
    print(f"OS: {os.uname().sysname}")
    print(f"Release: {os.uname().release}")
    print(f"Machine: {os.uname().machine}")
    
    # Check RAM
    try:
        with open('/proc/meminfo', 'r') as f:
            meminfo = f.readlines()
            total_mem = int(meminfo[0].split()[1]) / 1024 / 1024  # Convert to GB
            free_mem = int(meminfo[1].split()[1]) / 1024 / 1024
            print(f"RAM: {free_mem:.2f}GB free / {total_mem:.2f}GB total")
    except:
        pass

def test_video_download():
    """Test if yt-dlp can download videos"""
    print("\n🎬 Testing video download capability...")
    try:
        import yt_dlp
        ydl_opts = {
            'format': 'bestvideo[height<=720]+bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'simulate': True  # Don't actually download
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ", download=False)
            print(f"✅ Can access YouTube via yt-dlp")
            print(f"   Video formats available: {len(info.get('formats', []))}")
    except Exception as e:
        print(f"⚠️  YouTube access test failed: {e}")

def main():
    print("=" * 60)
    print("AnnieXMusic - Video Playback Diagnostic Tool")
    print("=" * 60)
    
    check_system_info()
    print("\n🔍 Checking system dependencies...")
    ffmpeg_ok = check_ffmpeg()
    ffprobe_ok = check_ffprobe()
    
    check_python_packages()
    
    if ffmpeg_ok:
        test_video_download()
    
    print("\n" + "=" * 60)
    if not ffmpeg_ok or not ffprobe_ok:
        print("❌ CRITICAL: FFmpeg/FFprobe is missing!")
        print("\nTo fix this issue, run:")
        print("  sudo apt-get update")
        print("  sudo apt-get install -y ffmpeg")
    else:
        print("✅ All dependencies appear to be installed correctly")
    print("=" * 60)

if __name__ == "__main__":
    main()
