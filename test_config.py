# Test Configuration
TEST_CONFIG = {
    "website_url": "https://chatsafari.com",
    "test_bots": {
        "male": 30,  # 20 Indian + 10 American
        "female": 25  # 15 Indian + 10 American
    },
    "headless": False,  # Set to True to run without browser window
    "debug": True,  # Enable debug logging
    "response_delay": (1, 3),  # Delay between responses
    "test_duration": 86400,  # Test duration in seconds (24 hours)
    "conversation_settings": {
        "question_interval": 30,  # Ask a question every 30 seconds
        "max_consecutive_questions": 3,  # Maximum questions in a row
        "typing_delay": (0.5, 1.5),  # Simulate typing delay
        "conversation_topics": [
            "hobbies", "movies", "music", "travel", "food",
            "sports", "technology", "books", "fashion", "daily life"
        ]
    }
}

# Logging Configuration
LOGGING_CONFIG = {
    "filename": "test_bots.log",
    "level": "DEBUG",
    "format": "%(asctime)s - %(levelname)s - %(message)s"
} 