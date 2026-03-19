#!/bin/bash
# Emergency Bot Fix Script
# Fixes database lock and restarts bot safely

echo "🔧 Starting emergency fix for AnnieXMusic Bot..."
echo "Time: $(date)"
echo ""

# Navigate to bot directory
cd /root/tg-vc-music-player

echo "📁 Step 1: Stopping existing bot process..."
pkill -f "python.*AnnieXMedia" || true
sleep 3

echo "🗑️ Step 2: Clearing locked session files..."
rm -f AnnieXMusic.session
rm -f AnnieXMusic.session-journal
rm -f session_generator.session
rm -f session_generator.session-journal
echo "✅ Session files cleared"

echo "🧹 Step 3: Clearing cache directories..."
rm -rf cache/*
rm -rf downloads/*
rm -rf playback/*
echo "✅ Cache cleared"

echo "🔍 Step 4: Checking Python environment..."
python3 --version
which python3

echo "📦 Step 5: Verifying dependencies..."
pip3 list | grep -i pyrogram || echo "⚠️ Pyrogram not found!"

echo "🚀 Step 6: Starting bot fresh..."
nohup python3 -m AnnieXMedia > bot.log 2>&1 &
sleep 5

echo ""
echo "✅ Fix complete! Checking bot status..."
ps aux | grep -i "python.*AnnieXMedia" | grep -v grep

echo ""
echo "📊 Last 20 log lines:"
tail -20 bot.log

echo ""
echo "🎉 Bot restart initiated!"
echo "Monitor logs with: tail -f bot.log"
