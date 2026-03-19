# 📢 Promotion Message Features - AnnieXMusic Bot

## ✅ YES - Promotion Features ARE Available!

Your bot has **multiple promotion/broadcast features** built-in for sending messages to groups and members.

---

## 🎯 Available Promotion Commands

### 1. **/broadcast** - Mass Messaging (SUDOERS ONLY)
Send messages to all groups/users that have the bot.

#### Usage:
```bash
# Basic broadcast
/broadcast Your promotional message here

# Reply to a message and broadcast it
/broadcast

# With options
/broadcast -user -pin Testing broadcast
```

#### Options:
- `-user` : Broadcast to all users who use the bot
- `-assistant` : Broadcast via assistant accounts
- `-pin` : Pin the message in groups
- `-pinloud` : Pin with notification
- `-nobot` : Don't broadcast to bots

#### Example:
```bash
/broadcast -user -pin 🎉 New Feature Alert! Our bot now supports video playback with NEXGEN API!
```

#### Features:
✅ Sends to all served chats  
✅ Can forward messages or send custom text  
✅ Optional pinning  
✅ Assistant broadcasting  
✅ Flood control handling  
✅ Progress tracking  

---

### 2. **/tagall** - Group Member Mention
Tag all members in a group with fun messages.

#### Usage:
```bash
/tagall
```

#### Features:
- Automatically mentions all group members
- Uses pre-defined fun messages from `funtag_messages.py`
- Admin-only command
- Can be stopped with `/tagstop` or `/tagoff`

#### Message Categories Available:
- **GM_MESSAGES** - Good Morning wishes
- **GN_MESSAGES** - Good Night wishes
- **HI_MESSAGES** - Hello/Greeting messages
- **QUOTES** - Inspirational quotes
- **SHAYARI** - Poetry/shayari
- **TAG_ALL** - Fun tagging messages

---

### 3. **Specialized Tag Commands**

#### /gm - Good Morning Tag
```bash
/gm
```
Sends random good morning messages while tagging members.

#### /gn - Good Night Tag
```bash
/gn
```
Sends random good night messages while tagging members.

#### /hi - Hello Tag
```bash
/hi
```
Sends random greeting messages while tagging members.

#### /life - Life Quotes Tag
```bash
/life
```
Shares inspirational life quotes while tagging.

#### /shayari - Poetry Tag
```bash
/shayari
```
Shares Urdu/Hindi shayari while tagging members.

---

### 4. **Stop Commands**
Stop any running tag session:

```bash
/tagstop
/tagoff
/gmstop
/gnstop
/histop
/lifestop
/shayarioff
```

---

## 📊 Technical Details

### File Locations:
- **Broadcast**: `AnnieXMedia/plugins/misc/broadcast.py`
- **Tag All**: `AnnieXMedia/plugins/Manager/funtag.py`
- **Messages**: `AnnieXMedia/plugins/misc/funtag_messages.py`

### Database Functions Used:
- `get_served_chats()` - Get all groups with bot
- `get_served_users()` - Get all bot users
- `get_active_chats()` - Get currently active voice chats

### Access Control:
- **/broadcast**: SUDOERS only (OWNER_ID + sudo users)
- **/tagall**: Group admins only
- **Special tags**: Group admins only

---

## 💡 Use Cases

### For Bot Promotion:
1. **Feature Announcements**
   ```bash
   /broadcast 🎵 New: Video quality improved with NEXGEN API! Try /play now.
   ```

2. **Event Notifications**
   ```bash
   /broadcast -pin 🎉 Weekend special: Join our support group for music requests!
   ```

3. **User Engagement**
   ```bash
   /broadcast -user Thanks for using AnnieXMusic! We've reached 10K users! 🎊
   ```

### For Group Activity:
1. **Morning Greetings**
   ```bash
   /gm  # Tag everyone with good morning message
   ```

2. **Group Engagement**
   ```bash
   /tagall  # Fun way to mention everyone
   ```

3. **Inspirational Content**
   ```bash
   /life  # Share motivational quotes
   ```

---

## 🔧 Configuration

### Add More Messages:
Edit `AnnieXMedia/plugins/misc/funtag_messages.py`:

```python
PROMO_MESSAGES = [
    "**❅ Check out our new feature! 🎉**",
    "**❅ Join our support group! 💬**",
    # Add more...
]
```

### Create Custom Command:
```python
@app.on_message(filters.command("promo"))
async def promo_tag(client, message):
    await mention_members(client, message, PROMO_MESSAGES, "promostop")
```

---

## ⚠️ Important Notes

### Broadcasting Ethics:
1. **Don't spam** - Use broadcasts sparingly
2. **Important info only** - Don't broadcast trivial things
3. **Respect users** - Too many broadcasts = users blocking bot
4. **Flood control** - Built-in delays prevent Telegram bans

### Tag All Best Practices:
1. **Admin control** - Only admins can use
2. **Can be stopped** - Users can complain if annoyed
3. **Use sparingly** - Don't overuse in active groups
4. **Fun messages** - Keep it light and entertaining

---

## 📈 Statistics Tracking

The broadcast command shows:
- Number of chats messaged
- Number of messages pinned
- Number of users messaged (if `-user` flag used)
- Assistant broadcast stats (if `-assistant` flag used)

Example Output:
```
✅ Bʀᴏᴀᴅᴄᴀsᴛ Cᴏᴍᴘʟᴇᴛᴇᴅ!

📊 Sᴇɴᴛ ᴛᴏ: 1250 ᴄʜᴀᴛs
📌 Pɪɴɴᴇᴅ: 876 ᴄʜᴀᴛs
👥 Usᴇʀs: 3420 ᴜsᴇʀs
```

---

## 🛠️ Troubleshooting

### Broadcast Not Working:
1. Check if user is in SUDOERS
2. Verify bot has database access
3. Check logs for errors

### Tag All Not Working:
1. Ensure command is from admin
2. Check bot has delete messages permission
3. Verify group isn't too large (may take time)

### Stuck Tagging:
Use stop commands:
```bash
/tagstop
```

Or manually clear in code:
```python
spam_chats.clear()
active_tags.clear()
```

---

## 🎨 Customization Ideas

### Seasonal Messages:
```python
DIWALI_MESSAGES = [...]
HOLI_MESSAGES = [...]
CHRISTMAS_MESSAGES = [...]
```

### Promotional Templates:
```python
FEATURE_ANNOUNCE = """
🎉 NEW FEATURE ALERT! 🎉

{} 

Try it now with /play
"""
```

### Multi-language Support:
Already available in:
- English (`en.yml`)
- Hindi (`hi.yml`)
- Hinglish (`hinglish.yml`)
- Russian (`ru.yml`)
- Arabic (`ar.yml`)
- Turkish (`tr.yml`)
- Bhojpuri (`bhojpuri.yml`)

---

## 📝 Summary

| Feature | Command | Access | Description |
|---------|---------|--------|-------------|
| Mass Broadcast | `/broadcast` | SUDOERS | Send to all chats/users |
| Tag All | `/tagall` | Admins | Mention all members |
| Good Morning | `/gm` | Admins | GM messages + tags |
| Good Night | `/gn` | Admins | GN messages + tags |
| Hello | `/hi` | Admins | Greeting messages + tags |
| Life Quotes | `/life` | Admins | Inspirational quotes |
| Shayari | `/shayari` | Admins | Poetry messages |

---

## ✅ Conclusion

**YES**, your bot has comprehensive promotion messaging features:

1. ✅ **Broadcast system** for mass announcements
2. ✅ **Group tagging** for member engagement  
3. ✅ **Multiple message types** (GM, GN, HI, quotes, shayari, fun tags)
4. ✅ **Admin controls** to start/stop
5. ✅ **Safe implementation** with flood control
6. ✅ **Multi-language support**

All features are production-ready and currently active on your server!

---

**Last Updated**: March 17, 2026  
**Status**: ✅ FULLY OPERATIONAL
