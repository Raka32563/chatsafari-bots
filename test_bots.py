import time
import logging
import sys
from chat_bots import ChatBot, BotManager, INDIAN_MALE_NAMES, AMERICAN_MALE_NAMES, INDIAN_FEMALE_NAMES, AMERICAN_FEMALE_NAMES
from test_config import TEST_CONFIG, LOGGING_CONFIG

def setup_logging():
    # Set up logging to both file and console
    logging.basicConfig(
        level=getattr(logging, LOGGING_CONFIG["level"]),
        format=LOGGING_CONFIG["format"],
        handlers=[
            logging.FileHandler(LOGGING_CONFIG["filename"]),
            logging.StreamHandler(sys.stdout)
        ]
    )

def print_bot_details(bot):
    """Print detailed information about a bot"""
    logging.info(f"""
Bot Details:
------------
Username: {bot.username}
Gender: {bot.gender}
Age: {bot.age}
Status: {'Active' if bot.is_active else 'Inactive'}
    """)

def test_single_bot():
    """Test a single bot"""
    logging.info("Starting single bot test...")
    
    # Create a test bot
    bot = ChatBot("TestBot", "male")
    print_bot_details(bot)
    
    try:
        # Setup and login
        logging.info("Setting up Chrome driver...")
        bot.setup_driver()
        
        logging.info("Attempting to login...")
        if bot.login():
            logging.info("Bot login successful")
            
            # Monitor for 1 minute
            start_time = time.time()
            logging.info("Starting chat monitoring...")
            while time.time() - start_time < 60:
                try:
                    bot.monitor_chat()
                    time.sleep(1)
                except Exception as e:
                    logging.error(f"Error during chat monitoring: {str(e)}")
                    break
        else:
            logging.error("Bot login failed")
            
    except Exception as e:
        logging.error(f"Error in single bot test: {str(e)}")
    finally:
        logging.info("Cleaning up bot...")
        bot.cleanup()

def test_multiple_bots():
    """Test multiple bots"""
    logging.info("Starting multiple bots test...")
    
    # Create bot manager with test configuration
    manager = BotManager()
    
    # Log bot creation details
    logging.info("\nBot Creation Summary:")
    logging.info("--------------------")
    logging.info(f"Indian Male Bots: {len(INDIAN_MALE_NAMES)}")
    logging.info(f"American Male Bots: {len(AMERICAN_MALE_NAMES)}")
    logging.info(f"Indian Female Bots: {len(INDIAN_FEMALE_NAMES)}")
    logging.info(f"American Female Bots: {len(AMERICAN_FEMALE_NAMES)}")
    logging.info(f"Total Bots: {len(manager.bots)}")
    
    # Limit bots based on test configuration
    manager.bots = manager.bots[:TEST_CONFIG["test_bots"]["male"] + TEST_CONFIG["test_bots"]["female"]]
    logging.info(f"\nUsing {len(manager.bots)} bots for testing")
    
    try:
        # Start all bots
        logging.info("\nStarting all bots...")
        for bot in manager.bots:
            print_bot_details(bot)
            try:
                bot.setup_driver()
                if bot.login():
                    bot.start_monitoring()
                    logging.info(f"Successfully started bot: {bot.username}")
                else:
                    logging.error(f"Failed to login bot: {bot.username}")
            except Exception as e:
                logging.error(f"Error starting bot {bot.username}: {str(e)}")
        
        # Monitor for test duration
        start_time = time.time()
        while time.time() - start_time < TEST_CONFIG["test_duration"]:
            active_bots = sum(1 for bot in manager.bots if bot.is_active)
            logging.info(f"\nStatus Update:")
            logging.info(f"Active bots: {active_bots}/{len(manager.bots)}")
            logging.info(f"Time elapsed: {int(time.time() - start_time)} seconds")
            time.sleep(10)
            
    except Exception as e:
        logging.error(f"Error in multiple bots test: {str(e)}")
    finally:
        logging.info("\nStopping all bots...")
        manager.stop_all_bots()

def main():
    setup_logging()
    logging.info("Starting bot tests...")
    
    try:
        # Test single bot
        logging.info("=== Starting Single Bot Test ===")
        test_single_bot()
        time.sleep(5)  # Wait between tests
        
        # Test multiple bots
        logging.info("=== Starting Multiple Bots Test ===")
        test_multiple_bots()
        
        logging.info("All tests completed successfully")
        
    except Exception as e:
        logging.error(f"Test suite failed: {str(e)}")
    finally:
        logging.info("Test suite finished")

if __name__ == "__main__":
    main() 