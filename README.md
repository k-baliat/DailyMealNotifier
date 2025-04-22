# 🍽️ Daily Meal Notifier

> A personal automation project that sends daily meal notifications via Telegram, helping maintain a consistent meal planning routine. This project was developed as a personal tool to streamline meal planning and notification delivery.

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Personal%20Use-lightgrey.svg)]()

## 📋 Overview

The Daily Meal Notifier is a Python-based service that automatically sends daily meal information to a specified Telegram group. It integrates with Firebase for meal plan storage and uses Telegram's API for notifications. The service runs on a scheduled basis, sending meal details including ingredients at a specified time each day.

```ascii
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │             │    │             │    │             │      │
│  │  Firebase   │◄──►│  Python     │◄──►│  Telegram   │      │
│  │  Firestore  │    │  Service    │    │  Bot API    │      │
│  │             │    │             │    │             │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🏗️ Technical Architecture

### Core Components

```ascii
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │  Firebase   │    │  Python     │    │  Telegram   │      │
│  │  Firestore  │    │  Backend    │    │  Bot API    │      │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘      │
│         │                  │                  │             │
│         └──────────────────┴──────────────────┘             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

- **Python Backend**: Built with Python 3.10, utilizing modern async patterns and robust error handling
- **Firebase Integration**: Uses Firestore for storing meal plans and recipe data
- **Telegram API**: Sends notifications through Telegram's bot API
- **Scheduling**: Implements APScheduler for reliable daily notifications
- **Environment Management**: Uses python-dotenv for secure configuration management

### 🔑 Key Features

```ascii
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │  Automated  │    │  Timezone   │    │  Error      │      │
│  │Notifications│    │  Aware      │    │  Handling   │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

- Automated daily meal notifications
- Timezone-aware scheduling (PST)
- Robust error handling and logging
- Secure credential management
- Graceful shutdown handling

## 🛠️ Technical Stack

```ascii
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │  Python     │    │  Firebase   │    │  Telegram   │      │
│  │  3.10       │    │  Admin      │    │  Bot API    │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

- **Language**: Python 3.x
- **Dependencies**:
  - `firebase-admin`: Firebase integration
  - `python-dotenv`: Environment management
  - `pytz`: Timezone handling
  - `apscheduler`: Job scheduling
  - `requests`: HTTP client
  - `python-telegram-bot`: Telegram integration

## 📁 Project Structure

```ascii
DailyMealNotifier/
├── 📄 daily_meal_notifier.py    # Main application logic
├── 📁 utils/
│   └── 📄 text_utils.py         # Telegram notification utilities
├── 📄 requirements.txt          # Project dependencies
└── 📄 .env                      # Environment configuration
```

## ⚙️ Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables in `.env`:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_GROUP_ID`
   - `FIREBASE_SERVICE_ACCOUNT_BASE64`

## 🚀 Usage

Run the application:
```bash
python daily_meal_notifier.py
```

The service will:
- Initialize Firebase connection
- Start the scheduler
- Send a startup notification
- Run daily at 12 PM PST

## 📝 Development Notes

This project was developed as a personal automation tool to:
- Streamline meal planning
- Ensure consistent meal notifications
- Practice Python development
- Implement robust error handling
- Work with external APIs (Firebase, Telegram)
