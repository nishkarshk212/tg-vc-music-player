# Authored By Certified Coders © 2025
import asyncio
import logging
import requests
from pathlib import Path
from urllib.parse import urlsplit

from config import COOKIE_URL
from AnnieXMedia.utils.errors import capture_internal_err

COOKIE_PATH = Path("AnnieXMedia/assets/cookies.txt")


def _extract_paste_id(url: str) -> str:
    path = urlsplit(url).path.rstrip("/")
    parts = [p for p in path.split("/") if p]
    return parts[-1] if parts else ""


def resolve_raw_cookie_url(url: str) -> str:
    url = (url or "").strip()
    low = url.lower()

    if "pastebin.com/" in low and "/raw/" not in low:
        paste_id = _extract_paste_id(url)
        return f"https://pastebin.com/raw/{paste_id}" if paste_id else url

    if "batbin.me/" in low:
        if "/api/v2/paste/" in low:
            return url
        paste_id = _extract_paste_id(url)
        return f"https://batbin.me/api/v2/paste/{paste_id}" if paste_id else url

    return url


@capture_internal_err
async def fetch_and_store_cookies():
    if not COOKIE_URL:
        LOGGER = logging.getLogger("AnnieXMedia.cookie_handler")
        LOGGER.warning("⚠️ ᴄᴏᴏᴋɪᴇ_ᴜʀʟ ɴᴏᴛ sᴇᴛ ɪɴ ᴇɴᴠ. Cᴏᴏᴋɪᴇ-ʙᴀsᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅs ᴡɪʟʟ ɴᴏᴛ ᴡᴏʀᴋ.")
        return None

    raw_url = resolve_raw_cookie_url(COOKIE_URL)

    try:
        response = await asyncio.to_thread(
            requests.get,
            raw_url,
            timeout=15,
            headers={"User-Agent": "annie-cookie-fetcher/1.0"},
        )
        response.raise_for_status()
    except Exception as e:
        LOGGER = logging.getLogger("AnnieXMedia.cookie_handler")
        LOGGER.error(f"⚠️ ᴄᴀɴ'ᴛ ꜰᴇᴛᴄʜ ᴄᴏᴏᴋɪᴇs:\n{e}")
        return None

    cookies = (response.text or "").strip()

    if not cookies.startswith("# Netscape"):
        LOGGER = logging.getLogger("AnnieXMedia.cookie_handler")
        LOGGER.error("⚠️ ɪɴᴠᴀʟɪᴅ ᴄᴏᴏᴋɪᴇ ꜰᴏʀᴍᴀᴛ. ɴᴇᴇᴅs ɴᴇᴛsᴄᴀᴘᴇ ꜰᴏʀᴍᴀᴛ.")
        return None

    if len(cookies) < 100:
        LOGGER = logging.getLogger("AnnieXMedia.cookie_handler")
        LOGGER.error("⚠️ ᴄᴏᴏᴋɪᴇ ᴄᴏɴᴛᴇɴᴛ ᴛᴏᴏ sʜᴏʀᴛ. ᴘᴏssɪʙʟʏ ɪɴᴠᴀʟɪᴅ.")
        return None

    COOKIE_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        COOKIE_PATH.write_text(cookies, encoding="utf-8")
        LOGGER = logging.getLogger("AnnieXMedia.cookie_handler")
        LOGGER.info("✅ Cᴏᴏᴋɪᴇs ғᴇᴛᴄʜᴇᴅ ᴀɴᴅ sᴀᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!")
    except Exception as e:
        LOGGER = logging.getLogger("AnnieXMedia.cookie_handler")
        LOGGER.error(f"⚠️ ғᴀɪʟᴇᴅ ᴛᴏ sᴀᴠᴇ ᴄᴏᴏᴋɪᴇs: {e}")
        return None
