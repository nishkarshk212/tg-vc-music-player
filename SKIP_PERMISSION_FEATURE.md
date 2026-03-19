# 🎵 Skip Permission Settings Feature

## 📋 Overview

The **Skip Permission** feature allows group admins to control **who can use the skip command** in their group chat. This gives administrators fine-grained control over music playback management.

---

## ✨ What Was Added

### **Three Permission Levels:**

1. **👑 Admins Only** (Default)
   - Only group admins and authorized users can skip songs
   - Maintains strict control over playback
   - Best for large groups

2. **👥 All Members**
   - Any group member (except bots) can skip songs
   - Excludes bots from skipping
   - Good for active communities

3. **🌍 Everyone**
   - Anyone in the group can skip songs
   - Most permissive setting
   - Best for small, trusted groups

---

## 🎛️ How to Use

### **Accessing Skip Permission Settings:**

1. Open your group chat
2. Send `/settings` or `/setting` command
3. Click on **"Skip Permission"** button
4. Choose your preferred option:
   - ✓ Admins Only
   - ✓ All Members
   - ✓ Everyone

### **Visual Interface:**

```
┌─────────────────────────────┐
│  Skip Permission Settings   │
├─────────────────────────────┤
│                             │
│  [✓ Admins Only]           │
│  [  All Members]            │
│  [  Everyone]               │
│                             │
│  [Back]  [Close]           │
└─────────────────────────────┘
```

The checkmark (✓) shows the currently selected option.

---

## 🔧 Technical Implementation

### **Files Modified:**

#### **1. Database Layer** (`AnnieXMedia/utils/database.py`)

**New Functions:**
- `get_skip_permission(chat_id)` - Get current permission setting
- `set_skip_permission(chat_id, permission)` - Set new permission
- `can_skip_song(chat_id, user_id)` - Check if user can skip

**Database Collection:**
- `mongodb.skip_permission` - Stores permission settings per chat

**Cache:**
- `skip_permissions_cache` - In-memory cache for fast lookups

#### **2. Inline Keyboard** (`AnnieXMedia/utils/inline/settings.py`)

**New Function:**
- `skip_permission_markup(_, current_permission)` - Generates 3-button layout

**Button Callbacks:**
- `SKIP_PERM_ADMIN` → Sets "admin" permission
- `SKIP_PERM_MEMBERS` → Sets "members" permission
- `SKIP_PERM_EVERYONE` → Sets "everyone" permission

#### **3. Settings Handler** (`AnnieXMedia/plugins/bot/settings.py`)

**New Routes:**
- `SKIP_PERMISSION_SETTINGS` - Opens skip permission panel
- `SKIP_PERM_*` callbacks - Handle permission changes

**Imports Added:**
```python
from AnnieXMedia.utils.database import (
    get_skip_permission,
    set_skip_permission,
)
from AnnieXMedia.utils.inline.settings import skip_permission_markup
```

#### **4. Admin Decorator** (`AnnieXMedia/utils/decorators/admins.py`)

**Updated Logic:**
```python
# New permission system check
if await can_skip_song(message.chat.id, message.from_user.id):
    pass  # User has permission
else:
    # Fallback to old voting system
    if await is_skipmode(message.chat.id):
        # Show vote request
```

#### **5. Language Files**

**English (`strings/langs/en.yml`):**
```yaml
ST_B_15 : "sᴋɪᴘ ᴘᴇʀᴍɪssɪᴏɴ"
ST_B_16 : "ᴀᴅᴍɪɴs ᴏɴʟʏ"
ST_B_17 : "ᴀʟʟ ᴍᴇᴍʙᴇʀs"
ST_B_18 : "ᴇᴠᴇʀʏᴏɴᴇ"
setting_13 : "Sᴋɪᴘ Pᴇʀᴍɪssɪᴏɴ Sᴇᴛᴛɪɴɢs..."
set_cb_6 : "» ɢᴇᴛᴛɪɴɢ sᴋɪᴘ ᴘᴇʀᴍɪssɪᴏɴ sᴇᴛᴛɪɴɢs..."
```

**Hinglish (`strings/langs/hinglish.yml`):**
```yaml
ST_B_15 : "Skip Permission"
ST_B_16 : "Admins Only"
ST_B_17 : "All Members"
ST_B_18 : "Everyone"
```

---

## 🎯 Permission Logic

### **Admins Only Mode:**
```python
✓ Group Owner
✓ Group Administrators
✓ Authorized Users (via /auth)
✗ Regular Members
✗ Bots
```

### **All Members Mode:**
```python
✓ Group Owner
✓ Group Administrators
✓ Authorized Users
✓ Regular Members (humans only)
✗ Bots
```

### **Everyone Mode:**
```python
✓ Everyone in the group
✓ Bots included
```

---

## 🔄 Backwards Compatibility

### **Voting System Integration:**

The new system **coexists** with the existing voting system:

1. **If skip permission = "admin"**: Uses new permission check
2. **If skip permission = "members"**: All members can skip
3. **If skip permission = "everyone"**: Everyone can skip

**Fallback Behavior:**
- If permission check fails AND voting mode is enabled → Shows vote request
- If permission check fails AND voting mode disabled → Denies access

---

## 📊 Use Cases

### **Scenario 1: Large Group (500+ members)**
**Recommended:** Admins Only
- Prevents spam skipping
- Maintains quality control
- Reduces disruptions

### **Scenario 2: Medium Community (50-500 members)**
**Recommended:** All Members
- Allows participation
- Excludes bots
- Balanced approach

### **Scenario 3: Small Friend Group (<50 members)**
**Recommended:** Everyone
- Maximum flexibility
- Trust-based
- No restrictions

---

## 🔍 Monitoring & Debugging

### **Check Current Setting:**
```bash
# In MongoDB
db.skip_permission.find({chat_id: YOUR_CHAT_ID})

# Expected output:
{
  "_id": ObjectId("..."),
  "chat_id": -1001234567890,
  "permission": "admin"  // or "members" or "everyone"
}
```

### **Logs:**
No specific logs are generated for permission checks (to reduce noise).

### **Testing:**
1. Set permission to "admin"
2. Try to skip as regular member → Should fail
3. Try to skip as admin → Should succeed
4. Change to "everyone"
5. Try to skip as anyone → Should succeed

---

## 🎛️ Commands Reference

### **For Users:**
- `/skip` or `/next` - Skip current song (if permitted)
- `/settings` - Access settings menu

### **For Admins:**
- `/settings` → "Skip Permission" - Change skip permissions
- `/auth <user>` - Add authorized user (works with "Admins Only" mode)
- `/unauth <user>` - Remove authorized user

---

## ⚠️ Important Notes

### **Default Behavior:**
- **Default setting:** "Admins Only" (most restrictive)
- **Applies to:** All skip commands (`/skip`, `/next`, `/cskip`)
- **Cached:** Yes, for performance (in `skip_permissions_cache`)

### **Permission Hierarchy:**
1. SUDOERS → Always bypass checks
2. Chat Owner → Always allowed
3. Based on setting → Admin/Members/Everyone

### **Bot Detection:**
- In "All Members" mode, bots are automatically excluded
- Prevents bot loops and automated abuse

---

## 🚀 Features Summary

### **What Users Get:**
✅ Clear UI with 3 options  
✅ Instant feedback on selection  
✅ Visual checkmark showing current setting  
✅ Works seamlessly with existing features  

### **What Admins Get:**
✅ Granular control over skip permissions  
✅ Easy to change via settings menu  
✅ Flexible for different group sizes  
✅ Backwards compatible with voting system  

### **What Developers Get:**
✅ Clean database abstraction  
✅ Reusable permission check function  
✅ Well-documented code  
✅ Extensible architecture  

---

## 📝 Example User Flow

### **Admin Changes Setting:**

1. Admin sends `/settings`
2. Bot shows settings menu
3. Admin clicks "Skip Permission"
4. Bot shows 3 options with current selection marked
5. Admin clicks "All Members"
6. Bot updates setting and refreshes keyboard
7. Checkmark moves to "All Members"
8. All members can now skip (except bots)

### **Member Tries to Skip:**

**With "Admins Only":**
```
User: /skip
Bot: ❌ Admin rights needed
     Refresh admin cache via: /reload
     » 5 votes needed for performing this action.
     [Vote Button]
```

**With "All Members":**
```
User: /skip
Bot: ➻ sᴛʀᴇᴀᴍ sᴋɪᴩᴩᴇᴅ 🎄
     │ 
     └ʙʏ : @username 🥀
```

---

## 🔮 Future Enhancements

### **Potential Additions:**
1. **Custom Roles** - Allow specific non-admin users
2. **Time-based Permissions** - Different rules at different times
3. **Song-specific Permissions** - VIP songs only admins can skip
4. **Temporary Permissions** - Grant skip access for X minutes
5. **Auto-demote** - Demote skip permission after abuse detection

---

## ✅ Testing Checklist

- [x] Default permission is "admin"
- [x] Can change to "members"
- [x] Can change to "everyone"
- [x] Admins can always skip in "admin" mode
- [x] Auth users can skip in "admin" mode
- [x] Regular members cannot skip in "admin" mode
- [x] All members can skip in "members" mode
- [x] Bots cannot skip in "members" mode
- [x] Everyone can skip in "everyone" mode
- [x] SUDOERS bypass all checks
- [x] Voting system still works as fallback
- [x] Settings UI displays correctly
- [x] Language strings load properly
- [x] Cache updates on permission change

---

## 🎉 Summary

The **Skip Permission** feature provides flexible, granular control over who can skip songs in group chats. It integrates seamlessly with existing systems while providing a modern, user-friendly interface.

**Status:** ✅ PRODUCTION READY  
**Complexity:** Medium  
**Impact:** High (affects all group interactions)  
**Backwards Compatible:** ✅ Yes  

---

**Last Updated:** March 19, 2026  
**Version:** 4.0 Enhanced  
**Author:** Certified Coders  
**Feature Status:** Ready for Deployment
