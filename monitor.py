#!/usr/bin/env python3
"""
API Monitor Script
Monitors https://api-beta.luca.education and sends Telegram notifications on failures.
"""

import os
import sys
import time
import logging
import requests
from typing import Optional
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('monitor.log')
    ]
)
logger = logging.getLogger(__name__)

class APIMonitor:
    def __init__(self, api_url: str, telegram_bot_token: str, telegram_chat_id: str):
        self.api_url = api_url
        self.telegram_bot_token = telegram_bot_token
        self.telegram_chat_id = telegram_chat_id
        self.session = requests.Session()
        self.session.timeout = 30
        
    def check_api_health(self) -> tuple[bool, int, str]:
        """
        Check the API health and return status information.
        
        Returns:
            tuple: (is_healthy, status_code, message)
        """
        try:
            logger.info(f"Checking API health: {self.api_url}")
            response = self.session.get(self.api_url)
            
            if response.status_code == 200:
                logger.info("API is healthy - status 200")
                return True, response.status_code, "API is responding normally"
            else:
                logger.warning(f"API returned non-200 status: {response.status_code}")
                return False, response.status_code, f"API returned status {response.status_code}"
                
        except requests.exceptions.Timeout:
            error_msg = "API request timed out"
            logger.error(error_msg)
            return False, 0, error_msg
        except requests.exceptions.ConnectionError:
            error_msg = "Failed to connect to API"
            logger.error(error_msg)
            return False, 0, error_msg
        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {str(e)}"
            logger.error(error_msg)
            return False, 0, error_msg
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            return False, 0, error_msg
    
    def send_telegram_message(self, message: str) -> bool:
        """
        Send a message via Telegram bot.
        
        Args:
            message: The message to send
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        if not self.telegram_bot_token or not self.telegram_chat_id:
            logger.error("Telegram bot token or chat ID not configured")
            return False
            
        telegram_url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        
        payload = {
            "chat_id": self.telegram_chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        try:
            response = requests.post(telegram_url, json=payload, timeout=10)
            if response.status_code == 200:
                logger.info("Telegram message sent successfully")
                return True
            else:
                logger.error(f"Failed to send Telegram message: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Error sending Telegram message: {str(e)}")
            return False
    
    def monitor(self, check_interval: int = 60):
        """
        Start monitoring the API with the specified interval.
        
        Args:
            check_interval: Interval between checks in seconds (default: 60)
        """
        logger.info(f"Starting API monitor for {self.api_url}")
        logger.info(f"Check interval: {check_interval} seconds")

        previous_healthy = True
        
        while True:
            try:
                is_healthy, status_code, message = self.check_api_health()
                
                if not is_healthy:
                    previous_healthy = False
                    # Send Telegram notification
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    telegram_message = (
                        f"🚨 <b>Server is down</b>\n\n"
                        f"<b>URL:</b> {self.api_url}\n"
                        f"<b>Status Code:</b> {status_code}\n"
                        f"<b>Message:</b> {message}\n"
                        f"<b>Time:</b> {timestamp}"
                    )
                    
                    if self.send_telegram_message(telegram_message):
                        logger.info("Alert sent to Telegram")
                    else:
                        logger.error("Failed to send alert to Telegram")
                else:
                    if not previous_healthy:
                        # Send Telegram notification if server is back online
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        telegram_message = (
                            f"🟢 <b>Server is back online</b>\n\n"
                            f"<b>URL:</b> {self.api_url}\n"
                            f"<b>Status Code:</b> {status_code}\n"
                            f"<b>Message:</b> {message}\n"
                            f"<b>Time:</b> {timestamp}"
                        )
                        if self.send_telegram_message(telegram_message):
                            logger.info("Alert sent to Telegram")
                        else:
                            logger.error("Failed to send alert to Telegram")
                        previous_healthy = True
                
                # Wait before next check
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error in monitoring loop: {str(e)}")
                time.sleep(check_interval)

def main():
    """Main function to run the API monitor."""
    # Configuration from environment variables
    api_url = os.getenv("API_URL")
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    check_interval = int(os.getenv("CHECK_INTERVAL", "300"))

     # Validate required environment variables
    if not api_url:
        logger.error("API_URL environment variable is required")
        sys.exit(1)
    
    # Validate required environment variables
    if not telegram_bot_token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable is required")
        sys.exit(1)
    
    if not telegram_chat_id:
        logger.error("TELEGRAM_CHAT_ID environment variable is required")
        sys.exit(1)
    
    # Create and start monitor
    monitor = APIMonitor(api_url, telegram_bot_token, telegram_chat_id)
    monitor.monitor(check_interval)

if __name__ == "__main__":
    main() 