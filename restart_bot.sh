#!/bin/bash
# Bot restart script

echo "🔄 Stopping AnnieXMusic bot..."

# Kill the existing bot process
pkill -f "python3 -m AnnieXMedia"
sleep 2

echo "🚀 Starting AnnieXMusic bot..."

# Navigate to bot directory
cd /root/tg-vc-music-player

# Activate virtual environment
source venv/bin/activate

# Start bot in background
nohup python3 -m AnnieXMedia > bot.log 2>&1 &
BOT_PID=$!
echo $BOT_PID > bot.pid

echo "✅ Bot restarted successfully!"
echo "📊 Process ID: $BOT_PID"
echo "📄 Log file: bot.log"

# Show initial logs
sleep 3
echo ""
echo "📝 Initial logs:"
tail -20 bot.log
