#!/usr/bin/env python3
"""
Pyrogram v2 Session String Generator
Run this script to generate a STRING_SESSION for your userbot
"""

import asyncio
from pyrogram import Client
from pyrogram.errors import (
    SessionPasswordNeeded, 
    FloodWait, 
    PhoneNumberInvalid, 
    ApiIdInvalid, 
    PhoneCodeInvalid,
    PhoneCodeExpired
)
import os
import platform

# Colors for better UX
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header():
    """Print beautiful header"""
    os.system('clear' if platform.system() != 'Windows' else 'cls')
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("╔═══════════════════════════════════════════╗")
    print("║     PYROGRAM V2 SESSION GENERATOR         ║")
    print("║          For AnnieXMusic Bot              ║")
    print("╚═══════════════════════════════════════════╝")
    print(f"{Colors.ENDC}\n")

async def generate_session():
    """Generate Pyrogram v2 session string"""
    print_header()
    
    # Get API credentials
    print(f"{Colors.OKCYAN}📋 Enter your Telegram API credentials:{Colors.ENDC}\n")
    
    while True:
        try:
            api_id = int(input(f"{Colors.OKGREEN}[+] API ID:{Colors.ENDC} "))
            break
        except ValueError:
            print(f"{Colors.FAIL}❌ API ID must be a number!{Colors.ENDC}\n")
    
    api_hash = input(f"{Colors.OKGREEN}[+] API Hash:{Colors.ENDC} ").strip()
    
    if not api_id or not api_hash:
        print(f"{Colors.FAIL}❌ API ID and Hash are required!{Colors.ENDC}")
        return
    
    print(f"\n{Colors.OKBLUE}ℹ️ Get your API credentials from: https://my.telegram.org{Colors.ENDC}\n")
    print(f"{Colors.WARNING}⏳ Initializing session...{Colors.ENDC}\n")
    
    # Create client
    client = Client(
        name="session_generator",
        api_id=api_id,
        api_hash=api_hash,
        app_version="2.0.0",
        device_model="Session Generator",
    )
    
    try:
        await client.connect()
        print(f"{Colors.OKGREEN}✅ Connected to Telegram!{Colors.ENDC}\n")
        
        # Send code
        sent_code = None
        while True:
            try:
                phone = input(f"{Colors.OKGREEN}[+] Enter your phone number (with country code):{Colors.ENDC} ")
                if not phone:
                    print(f"{Colors.FAIL}❌ Phone number is required!{Colors.ENDC}\n")
                    continue
                
                sent_code = await client.send_code(phone)
                print(f"{Colors.OKGREEN}✅ Verification code sent to {phone}{Colors.ENDC}\n")
                break
                
            except FloodWait as e:
                print(f"{Colors.FAIL}❌ Flood Wait: Please wait {e.value} seconds{Colors.ENDC}\n")
                await asyncio.sleep(e.value)
            except PhoneNumberInvalid:
                print(f"{Colors.FAIL}❌ Invalid phone number! Try again.{Colors.ENDC}\n")
            except Exception as e:
                print(f"{Colors.FAIL}❌ Error sending code: {e}{Colors.ENDC}\n")
        
        # Get code
        while True:
            try:
                code = input(f"{Colors.OKGREEN}[+] Enter the verification code:{Colors.ENDC} ").strip()
                if not code:
                    print(f"{Colors.FAIL}❌ Code is required!{Colors.ENDC}\n")
                    continue
                
                await client.sign_in(phone, sent_code.phone_code_hash, code)
                print(f"{Colors.OKGREEN}✅ Phone verified!{Colors.ENDC}\n")
                break
                
            except PhoneCodeInvalid:
                print(f"{Colors.FAIL}❌ Invalid code! Try again.{Colors.ENDC}\n")
            except PhoneCodeExpired:
                print(f"{Colors.FAIL}❌ Code expired! Restarting...{Colors.ENDC}\n")
                return
            except FloodWait as e:
                print(f"{Colors.FAIL}❌ Flood Wait: Please wait {e.value} seconds{Colors.ENDC}\n")
                await asyncio.sleep(e.value)
            except Exception as e:
                print(f"{Colors.FAIL}❌ Error signing in: {e}{Colors.ENDC}\n")
        
        # Check for 2FA
        try:
            await client.get_me()
        except SessionPasswordNeeded:
            print(f"{Colors.WARNING}⚠️ Two-Step Verification is enabled!{Colors.ENDC}\n")
            while True:
                try:
                    password = input(f"{Colors.OKGREEN}[+] Enter your 2FA password:{Colors.ENDC} ").strip()
                    if not password:
                        print(f"{Colors.FAIL}❌ Password is required!{Colors.ENDC}\n")
                        continue
                    
                    await client.check_password(password)
                    print(f"{Colors.OKGREEN}✅ 2FA verified!{Colors.ENDC}\n")
                    break
                    
                except FloodWait as e:
                    print(f"{Colors.FAIL}❌ Flood Wait: Please wait {e.value} seconds{Colors.ENDC}\n")
                    await asyncio.sleep(e.value)
                except Exception as e:
                    print(f"{Colors.FAIL}❌ Wrong password! {e}{Colors.ENDC}\n")
        
        # Get session string
        session_string = await client.export_session_string()
        
        # Display success
        print(f"\n{Colors.OKGREEN}{'='*60}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}{Colors.BOLD}🎉 SESSION GENERATED SUCCESSFULLY! 🎉{Colors.ENDC}")
        print(f"{Colors.OKGREEN}{'='*60}{Colors.ENDC}\n")
        
        print(f"{Colors.BOLD}Your STRING_SESSION:{Colors.ENDC}\n")
        print(f"{Colors.WARNING}{session_string}{Colors.ENDC}\n")
        
        print(f"{Colors.OKBLUE}{'='*60}{Colors.ENDC}\n")
        
        # Instructions
        print(f"{Colors.BOLD}📝 How to use this session:{Colors.ENDC}\n")
        print(f"1. Copy the session string above")
        print(f"2. Open your .env file")
        print(f"3. Replace STRING_SESSION value with this\n")
        print(f"{Colors.OKGREEN}Example:{Colors.ENDC}")
        print(f"   STRING_SESSION={session_string[:50]}...")
        print(f"\n{Colors.WARNING}⚠️ IMPORTANT:{Colors.ENDC}")
        print(f"   • Never share your session string with anyone!")
        print(f"   • Keep it private and secure")
        print(f"   • This gives access to your Telegram account\n")
        
        print(f"{Colors.OKGREEN}✅ After adding to .env, restart your bot!{Colors.ENDC}\n")
        
        # Save to file (optional)
        save = input(f"{Colors.OKGREEN}Do you want to save session to session.txt? (y/n):{Colors.ENDC} ").strip().lower()
        if save == 'y':
            with open("session.txt", "w") as f:
                f.write(session_string)
            print(f"{Colors.OKGREEN}✅ Session saved to session.txt{Colors.ENDC}\n")
        
    except ApiIdInvalid:
        print(f"{Colors.FAIL}❌ Invalid API ID or Hash! Please check and try again.{Colors.ENDC}\n")
    except FloodWait as e:
        print(f"{Colors.FAIL}❌ Flood Wait: Please wait {e.value} seconds and try again.{Colors.ENDC}\n")
    except Exception as e:
        print(f"{Colors.FAIL}❌ An error occurred: {e}{Colors.ENDC}\n")
    finally:
        await client.disconnect()
        print(f"{Colors.OKBLUE}👋 Session generator closed.{Colors.ENDC}\n")

if __name__ == "__main__":
    print(f"{Colors.BOLD}Starting session generator...{Colors.ENDC}\n")
    asyncio.run(generate_session())
