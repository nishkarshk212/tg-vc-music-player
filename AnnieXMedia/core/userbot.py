# Authored By Certified Coders © 2025
from pyrogram import Client

import config

from ..logging import LOGGER

assistants = []
assistantids = []

GROUPS_TO_JOIN = [
    "CertifiedDiscussion",
    "CertifiedCoders",
    "CertifiedCodes",
    "CertifiedDevs",
    "CertifiedNetwork",
]


# Initialize userbots
class Userbot:
    def __init__(self):
        self.one = Client(
            "AnnieAssis1",
            config.API_ID,
            config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
        )
        self.two = Client(
            "AnnieAssis2",
            config.API_ID,
            config.API_HASH,
            session_string=str(config.STRING2),
            no_updates=True,
        )
        self.three = Client(
            "AnnieAssis3",
            config.API_ID,
            config.API_HASH,
            session_string=str(config.STRING3),
            no_updates=True,
        )
        self.four = Client(
            "AnnieAssis4",
            config.API_ID,
            config.API_HASH,
            session_string=str(config.STRING4),
            no_updates=True,
        )
        self.five = Client(
            "AnnieAssis5",
            config.API_ID,
            config.API_HASH,
            session_string=str(config.STRING5),
            no_updates=True,
        )

    async def start_assistant(self, client: Client, index: int):
        string_attr = [
            config.STRING1,
            config.STRING2,
            config.STRING3,
            config.STRING4,
            config.STRING5,
        ][index - 1]
        if not string_attr:
            LOGGER(__name__).info(f"Assistant {index} session string not provided, skipping...")
            return

        try:
            # Validate session string format before starting
            if not string_attr.startswith("BQI") and not string_attr.startswith("A8E"):
                LOGGER(__name__).error(f"Assistant {index} has invalid session string format. Skipping...")
                return
            
            await client.start()
            for group in GROUPS_TO_JOIN:
                try:
                    await client.join_chat(group)
                except Exception as join_error:
                    LOGGER(__name__).debug(f"Assistant {index} couldn't join {group}: {join_error}")
                    pass

            assistants.append(index)

            try:
                await client.send_message(
                    config.LOGGER_ID, f"Annie's Assistant {index} Started"
                )
            except Exception as log_error:
                LOGGER(__name__).error(
                    f"Assistant {index} can't access the log group. Check permissions! Error: {log_error}"
                )
                # Don't exit, just continue without sending log message

            me = await client.get_me()
            client.id, client.name, client.username = me.id, me.first_name, me.username
            assistantids.append(me.id)

            LOGGER(__name__).info(f"Assistant {index} Started as {client.name}")

        except Exception as e:
            error_msg = str(e)
            if "unpack requires a buffer" in error_msg or "Invalid session string" in error_msg:
                LOGGER(__name__).error(f"Assistant {index} has corrupted session string. Please regenerate STRING{index}. Error: {e}")
            else:
                LOGGER(__name__).error(f"Failed to start Assistant {index}: {e}")

    async def start(self):
        LOGGER(__name__).info("Starting Annie's Assistants...")
        await self.start_assistant(self.one, 1)
        await self.start_assistant(self.two, 2)
        await self.start_assistant(self.three, 3)
        await self.start_assistant(self.four, 4)
        await self.start_assistant(self.five, 5)

    async def stop(self):
        LOGGER(__name__).info("Stopping Assistants...")
        try:
            if config.STRING1:
                await self.one.stop()
            if config.STRING2:
                await self.two.stop()
            if config.STRING3:
                await self.three.stop()
            if config.STRING4:
                await self.four.stop()
            if config.STRING5:
                await self.five.stop()
        except Exception as e:
            LOGGER(__name__).error(f"Error while stopping assistants: {e}")
