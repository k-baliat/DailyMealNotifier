import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import requests
import random
import string
import time

def check_bot_status():
    """Check if the bot is active and responding to API calls."""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    try:
        response = requests.get(url)
        if response.status_code == 200 and response.json().get("ok"):
            return True
        return False
    except requests.exceptions.RequestException:
        return False

def get_real_chat_id(max_retries=3, retry_delay=5):
    """
    Get the chat ID from the most recent message to the bot.
    
    Args:
        max_retries (int): Maximum number of retry attempts
        retry_delay (int): Delay between retries in seconds
    
    Returns:
        int: The chat ID
    
    Raises:
        Exception: If no chat ID is found after all retries
    """
    if not check_bot_status():
        raise Exception("❌ Bot is not active. Please check your bot token and internet connection.")
    
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url).json()
            if response.get("ok") and response.get("result"):
                return response["result"][-1]["message"]["chat"]["id"]
            
            if attempt < max_retries - 1:
                print(f"[APP]\t No messages found. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
        except (KeyError, IndexError, requests.exceptions.RequestException) as e:
            if attempt < max_retries - 1:
                print(f"[APP]\t Error occurred: {str(e)}. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                raise Exception(f"❌ Failed to get chat ID after {max_retries} attempts. Please send a message to your bot and try again.")
    
    raise Exception("❌ No chat ID found. Please send a message to your bot and try again.")


def send_telegram_message(message):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    chat_id = get_real_chat_id()
    print(f'[APP]\t Chat ID: {chat_id}')
    data = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, data=data)
    print("[APP]\t ✅Successfully Sent Notification to the BOT!")
    return response.json()
