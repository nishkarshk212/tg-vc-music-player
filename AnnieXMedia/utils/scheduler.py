# Authored By Certified Coders © 2025
"""
Auto-restart and cache cleanup scheduler
Restarts bot every 6 hours and clears cache files
"""
import asyncio
import os
import shutil
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
    """Schedule auto-restart every 6 hours with cache cleanup"""
    RESTART_INTERVAL = 6 * 60 * 60  # 6 hours in seconds
    
    LOGGER("Scheduler").info(f"Auto-restart scheduler started (interval: 6 hours)")
    
    while True:
        try:
            # Wait for 6 hours
            await asyncio.sleep(RESTART_INTERVAL)
            
            # Clear cache before restart
            LOGGER("Scheduler").info("Starting cache cleanup before restart...")
            cleared = await clear_cache()
            LOGGER("Scheduler").info(f"Cache cleanup completed: {cleared} items cleared")
            
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
                    f"🗑️ Cache cleared: <b>{cleared} items</b>\n\n"
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
            
            # Restart the bot
            LOGGER("Scheduler").info("Restarting bot...")
            os.execl("/usr/bin/python3", "/usr/bin/python3", "-m", "AnnieXMedia")
            
        except Exception as e:
            LOGGER("Scheduler").error(f"Scheduler error: {e}")
            # Wait 5 minutes before retrying on error
            await asyncio.sleep(300)


async def start_scheduler():
    """Start the scheduler in background"""
    LOGGER("Scheduler").info("Starting auto-restart and cache cleanup scheduler...")
    asyncio.create_task(schedule_auto_restart())
    LOGGER("Scheduler").info("Scheduler started successfully")
