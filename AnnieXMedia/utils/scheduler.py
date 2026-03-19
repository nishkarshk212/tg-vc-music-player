# Authored By Certified Coders © 2025
"""
Auto-restart, cache cleanup, and auto-update scheduler
Restarts bot every 6 hours, clears cache, pulls latest updates, and prevents database locks
"""
import asyncio
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from AnnieXMedia import LOGGER, app
from AnnieXMedia.utils.database import get_served_chats


async def clear_cache():
    """Clear cache directories and temporary files"""
    try:
        cache_dirs = [
            "cache",
            "downloads",
            "playback",
            "couples",
        ]
        
        cleared_count = 0
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                for filename in os.listdir(cache_dir):
                    file_path = os.path.join(cache_dir, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            cleared_count += 1
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                            cleared_count += 1
                    except Exception as e:
                        LOGGER("Scheduler").error(f"Failed to clear {file_path}: {e}")
        
        LOGGER("Scheduler").info(f"Cleared {cleared_count} cache files/directories")
        return cleared_count
    except Exception as e:
        LOGGER("Scheduler").error(f"Cache cleanup failed: {e}")
        return 0


async def schedule_auto_restart():
    """Schedule auto-restart every 6 hours with cache cleanup, auto-update, and graceful shutdown"""
    RESTART_INTERVAL = 6 * 60 * 60  # 6 hours in seconds
    
    LOGGER("Scheduler").info(f"Auto-restart scheduler started (interval: 6 hours with auto-update)")
    
    while True:
        try:
            # Wait for 6 hours
            await asyncio.sleep(RESTART_INTERVAL)
            
            # Clear cache before restart
            LOGGER("Scheduler").info("Starting cache cleanup before restart...")
            cleared = await clear_cache()
            LOGGER("Scheduler").info(f"Cache cleanup completed: {cleared} items cleared")
            
            # Auto-update: Pull latest changes from git repository
            try:
                LOGGER("Scheduler").info("Checking for updates from upstream repository...")
                result = subprocess.run(
                    ["git", "pull", "origin", "main"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    if "Already up to date." in result.stdout:
                        LOGGER("Scheduler").info("No updates available - already up to date")
                        update_status = "No updates"
                    else:
                        LOGGER("Scheduler").info(f"Updates pulled successfully: {result.stdout}")
                        update_status = "Updated"
                        # Install new dependencies if requirements.txt changed
                        if os.path.exists("requirements.txt"):
                            LOGGER("Scheduler").info("Installing updated dependencies...")
                            subprocess.run(
                                ["pip3", "install", "--no-cache-dir", "-r", "requirements.txt"],
                                capture_output=True,
                                timeout=120
                            )
                else:
                    LOGGER("Scheduler").error(f"Git pull failed: {result.stderr}")
                    update_status = "Failed"
            except subprocess.TimeoutExpired:
                LOGGER("Scheduler").error("Git pull timed out")
                update_status = "Timeout"
            except Exception as update_error:
                LOGGER("Scheduler").error(f"Auto-update failed: {update_error}")
                update_status = "Error"
            
            # Log restart info
            restart_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            LOGGER("Scheduler").info(f"Scheduled restart initiated at {restart_time}")
            
            # Send notification to all served chats about scheduled restart
            try:
                served_chats = await get_served_chats()
                notification_message = (
                    f"🔄 <b>Scheduled Maintenance Restart</b>\n\n"
                    f"{app.mention} will restart now for performance optimization.\n\n"
                    f"⏱️ Expected downtime: <b>10-15 seconds</b>\n"
                    f"🗑️ Cache cleared: <b>{cleared} items</b>\n"
                    f"📦 Auto-update: <b>{update_status}</b>\n\n"
                    f"✅ Bot will be back online shortly!"
                )
                
                sent_count = 0
                for chat in served_chats:
                    try:
                        chat_id = int(chat["chat_id"])
                        await app.send_message(chat_id, notification_message)
                        sent_count += 1
                        await asyncio.sleep(0.1)  # Small delay to avoid flood
                    except Exception:
                        # Skip chats where bot can't send messages
                        continue
                
                LOGGER("Scheduler").info(f"Restart notification sent to {sent_count} chats")
            except Exception as notify_error:
                LOGGER("Scheduler").error(f"Failed to send restart notifications: {notify_error}")
            
            # Save restart flag
            with open(".auto_restart", "w") as f:
                f.write(f"Auto-restarted at: {restart_time}\n")
                f.write(f"Cache cleared: {cleared} items\n")
                f.write(f"Notifications sent: {sent_count if 'sent_count' in locals() else 0}\n")
                f.write(f"Auto-update status: {update_status}\n")
            
            # Graceful shutdown to prevent database locks
            LOGGER("Scheduler").info("Performing graceful shutdown...")
            try:
                # Stop accepting new requests
                await asyncio.sleep(1)
                # Close session files gracefully
                if hasattr(app, 'stop'):
                    await app.stop()
                    await asyncio.sleep(2)  # Wait for session files to close
            except Exception as e:
                LOGGER("Scheduler").error(f"Graceful shutdown error: {e}")
            
            # Restart the bot
            LOGGER("Scheduler").info("Restarting bot...")
            os.execl(sys.executable, sys.executable, "-m", "AnnieXMedia")
            
        except Exception as e:
            LOGGER("Scheduler").error(f"Scheduler error: {e}")
            # Wait 5 minutes before retrying on error
            await asyncio.sleep(300)


async def start_scheduler():
    """Start the scheduler in background"""
    LOGGER("Scheduler").info("Starting auto-restart and cache cleanup scheduler...")
    asyncio.create_task(schedule_auto_restart())
    LOGGER("Scheduler").info("Scheduler started successfully")
