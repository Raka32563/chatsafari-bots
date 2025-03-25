import random
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import json
import os
from datetime import datetime
from test_config import TEST_CONFIG
from selenium.webdriver.common.keys import Keys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='chat_bots.log'
)

# Bot names
INDIAN_MALE_NAMES = [
    "Arjun", "Rahul", "Amit", "Rajesh", "Vikram", "Priyank", "Aditya", "Rohan",
    "Neeraj", "Sachin", "Ankit", "Deepak", "Ravi", "Sanjay", "Manoj", "Kunal",
    "Prakash", "Vishal", "Sunil", "Nitin"
]

AMERICAN_MALE_NAMES = [
    "James", "John", "Michael", "David", "William", "Richard", "Joseph", "Thomas",
    "Charles", "Christopher"
]

INDIAN_FEMALE_NAMES = [
    "Priya", "Neha", "Anjali", "Meera", "Pooja", "Ritu", "Anita", "Deepika",
    "Sneha", "Kavita", "Rani", "Sunita", "Lakshmi", "Geeta", "Maya"
]

AMERICAN_FEMALE_NAMES = [
    "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan",
    "Jessica", "Sarah", "Karen"
]

class ChatBot:
    def __init__(self, username, gender):
        self.username = username
        self.gender = gender
        self.age = random.randint(16, 32)
        self.driver = None
        self.is_active = False
        self.last_question_time = 0
        self.consecutive_questions = 0
        self.conversation_topics = TEST_CONFIG["conversation_settings"]["conversation_topics"].copy()
        random.shuffle(self.conversation_topics)
        self.current_topic_index = 0
        self.conversation_history = []
        self.thread = None
        
    def setup_driver(self):
        options = webdriver.ChromeOptions()
        if TEST_CONFIG["headless"]:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        
    def login(self):
        try:
            self.driver.get(TEST_CONFIG["website_url"])
            
            # Wait for login form elements
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            gender_select = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "gender"))
            )
            age_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "age"))
            )
            
            # Fill in the form
            username_field.send_keys(self.username)
            
            # Select gender
            gender_dropdown = Select(gender_select)
            gender_dropdown.select_by_value(self.gender)
            
            # Enter age
            age_field.send_keys(str(self.age))
            
            # Find and click login button
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            login_button.click()
            
            # Wait for successful login
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "chat-container"))
            )
            
            logging.info(f"Bot {self.username} logged in successfully")
            self.is_active = True
            return True
            
        except Exception as e:
            logging.error(f"Login failed for {self.username}: {str(e)}")
            self.is_active = False
            return False
            
    def get_random_response(self):
        responses = [
            "That's interesting! Tell me more.",
            "I can relate to that.",
            "Really? That's fascinating!",
            "I understand what you mean.",
            "That's a great point!",
            "I agree with you.",
            "That's something I hadn't considered.",
            "Interesting perspective!",
            "I see what you're saying.",
            "That makes sense to me."
        ]
        return random.choice(responses)

    def get_question_for_topic(self, topic):
        questions = {
            "hobbies": [
                "What do you like to do in your free time?",
                "Do you have any interesting hobbies?",
                "What activities do you enjoy most?"
            ],
            "movies": [
                "What kind of movies do you like?",
                "Who's your favorite actor?",
                "What's the last movie you watched?"
            ],
            "music": [
                "What type of music do you listen to?",
                "Who's your favorite artist?",
                "What's your favorite song?"
            ],
            "travel": [
                "Have you been to any interesting places?",
                "Where would you like to travel?",
                "What's your dream destination?"
            ],
            "food": [
                "What's your favorite cuisine?",
                "Do you like cooking?",
                "What's your favorite restaurant?"
            ],
            "sports": [
                "Do you follow any sports?",
                "What's your favorite team?",
                "Do you play any sports?"
            ],
            "technology": [
                "What gadgets do you use?",
                "Are you interested in new technology?",
                "What's your favorite app?"
            ],
            "books": [
                "Do you like reading?",
                "What's your favorite book?",
                "What genre do you prefer?"
            ],
            "fashion": [
                "What's your style like?",
                "Do you follow fashion trends?",
                "What's your favorite clothing brand?"
            ],
            "daily life": [
                "How do you usually spend your day?",
                "What's your morning routine?",
                "What do you do to relax?"
            ]
        }
        return random.choice(questions.get(topic, ["Tell me more about yourself."]))

    def simulate_typing(self, message):
        typing_delay = random.uniform(*TEST_CONFIG["conversation_settings"]["typing_delay"])
        time.sleep(typing_delay)
        # Add typing simulation logic here

    def ask_question(self):
        current_time = time.time()
        if (current_time - self.last_question_time >= TEST_CONFIG["conversation_settings"]["question_interval"] and 
            self.consecutive_questions < TEST_CONFIG["conversation_settings"]["max_consecutive_questions"]):
            
            topic = self.conversation_topics[self.current_topic_index]
            question = self.get_question_for_topic(topic)
            
            self.simulate_typing(question)
            # Add logic to send question
            
            self.last_question_time = current_time
            self.consecutive_questions += 1
            self.current_topic_index = (self.current_topic_index + 1) % len(self.conversation_topics)
            return True
        return False

    def monitor_chat(self):
        logging.info(f"Bot {self.username} started monitoring chat")
        while self.is_active:
            try:
                # First, check if we're in the chat room
                try:
                    chat_container = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "chat-container"))
                    )
                except:
                    logging.error(f"Bot {self.username} not in chat container, attempting to rejoin")
                    self.driver.refresh()
                    time.sleep(5)
                    continue

                # Check for notification bell icon
                try:
                    # Look for the bell icon button using exact class from Dashboard.tsx
                    bell_button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.p-2.text-gray-600"))
                    )
                    
                    # Click bell icon to open notification panel
                    bell_button.click()
                    logging.info(f"Bot {self.username} clicked notification bell")
                    time.sleep(1)  # Wait for notification panel to open
                    
                    # Look for users with unread messages in the dropdown
                    try:
                        unread_users = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.absolute.right-0.mt-2.w-64.bg-white.rounded-lg.shadow-lg.py-1.z-50.border.border-gray-200 div.px-4.py-3"))
                        )
                        
                        for user_element in unread_users:
                            try:
                                # Get user name from notification
                                user_name = user_element.find_element(By.CSS_SELECTOR, "span.font-medium.text-gray-900").text
                                logging.info(f"Bot {self.username} found unread message from: {user_name}")
                                
                                # Click on user to open chat
                                user_element.click()
                                logging.info(f"Bot {self.username} clicked on user: {user_name}")
                                time.sleep(2)  # Wait for chat window to open
                                
                                # Handle chat messages
                                try:
                                    chat_messages = WebDriverWait(self.driver, 5).until(
                                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.chat-message"))
                                    )
                                    
                                    for message in chat_messages:
                                        try:
                                            message_text = message.text.strip()
                                            if not message_text or message_text in self.conversation_history:
                                                continue
                                                
                                            self.conversation_history.append(message_text)
                                            logging.info(f"Bot {self.username} received new message from {user_name}: {message_text}")
                                            
                                            # Generate and send response
                                            response = self.get_random_response()
                                            logging.info(f"Bot {self.username} preparing to send response to {user_name}: {response}")
                                            
                                            # Find the message input field
                                            message_input = WebDriverWait(self.driver, 5).until(
                                                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Type your message']"))
                                            )
                                            
                                            if message_input:
                                                message_input.clear()
                                                message_input.send_keys(response)
                                                
                                                # Find and click the send button
                                                try:
                                                    send_button = WebDriverWait(self.driver, 3).until(
                                                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='send']"))
                                                    )
                                                    send_button.click()
                                                    logging.info(f"Bot {self.username} clicked send button to {user_name}")
                                                except:
                                                    # If no send button, try Enter key
                                                    message_input.send_keys(Keys.RETURN)
                                                    logging.info(f"Bot {self.username} sent message to {user_name} using Enter key")
                                                
                                                time.sleep(random.uniform(2, 4))
                                        except Exception as e:
                                            logging.error(f"Error processing message for {self.username} from {user_name}: {str(e)}")
                                            continue
                                            
                                except Exception as e:
                                    logging.error(f"Error handling chat messages for {self.username} with {user_name}: {str(e)}")
                                    continue
                                    
                            except Exception as e:
                                logging.error(f"Error handling user notification for {self.username}: {str(e)}")
                                continue
                                
                    except TimeoutException:
                        logging.debug(f"Bot {self.username} no unread users found")
                        # Close notification panel if open
                        try:
                            # Click outside the notification panel to close it
                            bell_button.click()
                        except:
                            pass
                        time.sleep(1)
                        continue
                        
                except TimeoutException:
                    # No notification bell found, continue monitoring
                    logging.debug(f"Bot {self.username} no notification bell found")
                    time.sleep(1)
                    continue
                    
                # Random delay between checks
                time.sleep(random.uniform(1, 3))
                
            except TimeoutException:
                logging.debug(f"Bot {self.username} timeout while monitoring, retrying...")
                time.sleep(1)
            except Exception as e:
                logging.error(f"Error monitoring chat for {self.username}: {str(e)}")
                self.is_active = False
                
    def start_monitoring(self):
        self.thread = threading.Thread(target=self.monitor_chat)
        self.thread.daemon = True
        self.thread.start()
                
    def cleanup(self):
        self.is_active = False
        if self.thread:
            self.thread.join()
        if self.driver:
            self.driver.quit()

class BotManager:
    def __init__(self):
        self.bots = []
        self.create_bots()
        
    def create_bots(self):
        # Create male bots
        for name in INDIAN_MALE_NAMES + AMERICAN_MALE_NAMES:
            self.bots.append(ChatBot(name, "male"))
            
        # Create female bots
        for name in INDIAN_FEMALE_NAMES + AMERICAN_FEMALE_NAMES:
            self.bots.append(ChatBot(name, "female"))
            
    def start_all_bots(self):
        for bot in self.bots:
            try:
                bot.setup_driver()
                if bot.login():
                    bot.start_monitoring()
            except Exception as e:
                logging.error(f"Failed to start bot {bot.username}: {str(e)}")
                
    def stop_all_bots(self):
        for bot in self.bots:
            bot.cleanup()

if __name__ == "__main__":
    manager = BotManager()
    try:
        manager.start_all_bots()
        # Keep the main thread running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        manager.stop_all_bots() 
