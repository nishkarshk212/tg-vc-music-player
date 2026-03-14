# 🚀 Quick Reference - New Features

## ✅ What's New?

### 1. ⏰ Auto-Restart (Every 6 Hours)
Your bot now automatically restarts every 6 hours to stay fresh and prevent crashes!

**What happens:**
- Bot clears old cache files
- Restarts cleanly
- Logs restart info
- Continues normal operation

### 2. 🗑️ Auto Cache Cleanup
Automatically removes temporary files before each restart

**Cleared directories:**
- `cache/` - Temp files
- `downloads/` - Old downloads  
- `playback/` - Speed adjustment files
- `couples/` - Image data

### 3. 🎬 Fixed vplay Command
Video playback now works perfectly!

**Working Commands:**
```
/vplay <YouTube link>     - Play video in VC
/play -v <YouTube link>   - Play with video
/cvplay <link>            - Channel video play
/vplayforce <link>        - Force video play
```

### 4. 💬 Fixed Start Message
Private chat start message now has 3-layer fallback:
1. Video (primary)
2. Photo (if video fails)
3. Text (if photo fails)

---

## 📊 Status Check

**Bot Status**: ✅ RUNNING  
**Scheduler**: ✅ ACTIVE  
**Server**: 140.245.240.202  
**Location**: /root/tg-vc-music-player  

---

## 🔍 How to Monitor

### Check if Scheduler is Running:
```bash
ssh root@140.245.240.202
cd /root/tg-vc-music-player
grep "Scheduler" bot.log | tail -5
```

### View Last Restart:
```bash
cat .auto_restart
```

### Check Bot Process:
```bash
ps aux | grep AnnieXMedia
```

---

## 🛠️ Troubleshooting

### If Bot Stops:
```bash
cd /root/tg-vc-music-player
python3 -m AnnieXMedia &
```

### Check Logs:
```bash
tail -f bot.log
```

### Manual Restart:
```bash
pkill -f 'python3 -m AnnieXMedia'
sleep 2
python3 -m AnnieXMedia &
```

---

## 📝 Recent Changes

### Files Added:
- `AnnieXMedia/utils/scheduler.py` - Auto-restart system
- `FEATURES_IMPLEMENTATION.md` - Full documentation
- `QUICK_REFERENCE.md` - This file

### Files Updated:
- `AnnieXMedia/__main__.py` - Scheduler integration
- `AnnieXMedia/plugins/bot/start.py` - Better error handling
- `AnnieXMedia/utils/decorators/play.py` - Fixed vplay logic

---

## ✨ Benefits

**For You:**
- No manual maintenance needed
- Cleaner server storage
- Better video playback
- Reliable welcome messages

**For Users:**
- Smoother experience
- Videos work properly
- Always gets welcome message
- More stable bot

---

## 🎯 All Features Working!

✅ Auto-restart scheduler  
✅ Cache cleanup  
✅ vplay command fixed  
✅ Start message fixed  
✅ Video playback working  
✅ Bot running smoothly  

---

**Need Help?** Check `FEATURES_IMPLEMENTATION.md` for detailed docs!

**Last Updated**: March 14, 2026  
**Status**: PRODUCTION READY ✅
