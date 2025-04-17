import os
import json
import base64
import logging
from datetime import datetime, timedelta
import pytz
from utils.text_utils import send_telegram_message
import firebase_admin
from firebase_admin import credentials, initialize_app, firestore
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import signal
import sys
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('daily_meal_notifier.log'),
        logging.StreamHandler()
    ]
)

# Global scheduler instance
scheduler = None

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logging.info("Received shutdown signal")
    if scheduler:
        scheduler.shutdown()
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Decode base64-encoded JSON from env var
#Ran the following in terminal and added the result in .env: base64 -i FirebaseConfig.json 
load_dotenv()
service_account_info = json.loads(
    base64.b64decode(os.getenv("FIREBASE_SERVICE_ACCOUNT_BASE64"))
)

# Initialize Firebase
try:
    cred = credentials.Certificate(service_account_info)
    initialize_app(cred)
    db = firestore.client()
    logging.info("Firebase initialized successfully")
except Exception as e:
    logging.error(f"Failed to initialize Firebase: {str(e)}")
    raise

def get_today_meal():
    """
    Get today's meal information from Firestore
    Returns a formatted string with the meal details
    """
    try:
        # Get today's date in PST
        pst = pytz.timezone('America/Los_Angeles')
        today = datetime.now(pst)
        day_of_week = today.strftime('%A')
        date_str = today.strftime('%B %d, %Y')
        
        # Get the week range
        week_range = get_week_range(today)
        
        # Get meal plan for this week
        meal_plan_ref = db.collection('mealPlans').document(week_range)
        meal_plan = meal_plan_ref.get()
        
        if not meal_plan.exists:
            logging.info(f"No meal plan found for {week_range}")
            return f"No meal planned for {day_of_week}, {date_str}"
            
        meal_data = meal_plan.to_dict()
        recipe_ids = meal_data.get(day_of_week, '').split(',')
        
        if not recipe_ids or recipe_ids[0] == '':
            logging.info(f"No meal planned for {day_of_week}, {date_str}")
            return f"No meal planned for {day_of_week}, {date_str}"
            
        # Get recipe details
        message = f"🍽️ Today's Meal ({day_of_week}, {date_str}):\n\n"
        
        for recipe_id in recipe_ids:
            recipe_ref = db.collection('recipes').document(recipe_id)
            recipe = recipe_ref.get()
            
            if recipe.exists:
                recipe_data = recipe.to_dict()
                message += f"📌 {recipe_data['name']}\n"
                message += "Ingredients:\n"
                for ingredient in recipe_data['ingredients']:
                    message += f"• {ingredient}\n"
                message += "\n"
            else:
                logging.warning(f"Recipe {recipe_id} not found")
        
        return message.strip()
    except Exception as e:
        error_msg = f"Error getting meal information: {str(e)}"
        logging.error(error_msg)
        return error_msg


def get_week_range(date):
    """
    Get the week range string for a given date
    """
    start_of_week = date - timedelta(days=date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return f"{start_of_week.strftime('%B %d, %Y')} - {end_of_week.strftime('%B %d, %Y')}"


def send_daily_meal():
    """
    Send today's meal information via Telegram
    """
    try:
        message = get_today_meal()
        print(f'[INFO]\t{message}')
        send_telegram_message(message)
        logging.info("Successfully sent daily meal notification")
    except Exception as e:
        error_msg = f"Error sending daily meal notification: {str(e)}"
        logging.error(error_msg)
        # Try to send error notification
        try:
            send_telegram_message(f"❌ {error_msg}")
        except:
            logging.error("Failed to send error notification")

def main():
    global scheduler
    
    try:
        # Initialize scheduler
        scheduler = BackgroundScheduler()
        
        # Set up the job to run at 12 PM PST
        trigger = CronTrigger(
            hour=12,
            minute=0,
            timezone="US/Pacific"
        )
        
        
        scheduler.add_job(
            send_daily_meal,
            trigger=trigger,
            id='daily_meal_notification',
            replace_existing=True
        )
        
        # Start the scheduler
        scheduler.start()
        logging.info("Scheduler started successfully")
        
        # Send startup notification
        try:
            send_telegram_message("✅ Daily meal notifier service started successfully")
        except Exception as e:
            logging.error(f"Failed to send startup notification: {str(e)}")
        
        # Keep the script running
        while True:
            if not scheduler.running:
                logging.error("Scheduler stopped unexpectedly")
                break
            time.sleep(60)
            
    except Exception as e:
        logging.error(f"Fatal error in main loop: {str(e)}")
        if scheduler:
            scheduler.shutdown()
        raise

if __name__ == "__main__":
    send_daily_meal()
