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

def get_all_chat_ids(max_retries=3, retry_delay=5):
    """
    Get all unique chat IDs that have interacted with the bot.
    
    Args:
        max_retries (int): Maximum number of retry attempts
        retry_delay (int): Delay between retries in seconds
    
    Returns:
        set: A set of unique chat IDs
    
    Raises:
        Exception: If no chat IDs are found after all retries
    """
    if not check_bot_status():
        raise Exception("❌ Bot is not active. Please check your bot token and internet connection.")
    
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url).json()
            if response.get("ok") and response.get("result"):
                # Extract all unique chat IDs from the updates
                chat_ids = set()
                for update in response["result"]:
                    if "message" in update and "chat" in update["message"]:
                        chat_ids.add(update["message"]["chat"]["id"])
                
                if chat_ids:
                    return chat_ids
                
            if attempt < max_retries - 1:
                print(f"[APP]\t No messages found. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
        except (KeyError, IndexError, requests.exceptions.RequestException) as e:
            if attempt < max_retries - 1:
                print(f"[APP]\t Error occurred: {str(e)}. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                raise Exception(f"❌ Failed to get chat IDs after {max_retries} attempts. Please send a message to your bot and try again.")
    
    raise Exception("❌ No chat IDs found. Please send a message to your bot and try again.")

def send_telegram_message(message):
    """
    Send a message to all users who have interacted with the bot.
    
    Args:
        message (str): The message to send
    
    Returns:
        list: List of responses from the Telegram API
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    # chat_ids = get_all_chat_ids()
    chat_id = os.getenv("TELEGRAM_GROUP_ID") #GroupChat ID
    
    responses = []
    # for chat_id in chat_ids:
    print(f'[APP]\t Sending message to Chat ID: {chat_id}')
    data = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        response = requests.post(url, data=data)
        responses.append(response.json())
        print(f"[APP]\t ✅ Successfully sent notification to chat ID {chat_id}")
    except requests.exceptions.RequestException as e:
        print(f"[APP]\t ❌ Failed to send message to chat ID {chat_id}: {str(e)}")
    
    return responses