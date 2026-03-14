# Authored By Certified Coders © 2025
import asyncio
import sys
from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus

import config
from ..logging import LOGGER


class MusicBotClient(Client):
    def __init__(self):
        super().__init__(
            name="AnnieXMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            workers=48,
            max_concurrent_transmissions=7,
        )
        LOGGER(__name__).info("Bot client initialized.")

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.username, self.id = me.username, me.id
        self.name = f"{me.first_name} {me.last_name or ''}".strip()
        self.mention = me.mention

        try:
            await asyncio.sleep(2)  # Wait for bot to fully initialize
            msg = (
                f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\n"
                f"ɪᴅ : <code>{self.id}</code>\n"
                f"ɴᴀᴍᴇ : {self.name}\n"
                f"ᴜsᴇʀɴᴀᴍᴇ : @{self.username}"
            )
            LOGGER(__name__).info(f"Attempting to send message to log group {config.LOGGER_ID}...")
            await self.send_message(config.LOGGER_ID, msg)
            LOGGER(__name__).info("Successfully sent message to log group!")
        except (errors.ChannelInvalid, errors.PeerIdInvalid) as e:
            LOGGER(__name__).error(f"❌ Bot cannot access the log group/channel – add & promote it first! Error: {type(e).__name__}: {e}")
            sys.exit()
        except Exception as exc:
            LOGGER(__name__).error(f"❌ Bot has failed to access the log group. Reason: {type(exc).__name__}: {exc}")
            sys.exit()

        try:
            member = await self.get_chat_member(config.LOGGER_ID, self.id)
            if member.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error("❌ Promote the bot as admin in the log group/channel.")
                sys.exit()
        except Exception as e:
            LOGGER(__name__).error(f"❌ Could not check admin status: {e}")
            sys.exit()

        LOGGER(__name__).info(f"✅ Music Bot started as {self.name} (@{self.username})")
