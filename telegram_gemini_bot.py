import os
import requests
import google.generativeai as genai
from datetime import datetime
import json

def send_telegram_message(bot_token, chat_id, message):
    """Send message to Telegram chat"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    # Split long messages if needed (Telegram has 4096 char limit)
    if len(message) > 4000:
        chunks = [message[i:i+4000] for i in range(0, len(message), 4000)]
        for chunk in chunks:
            payload = {
                'chat_id': chat_id,
                'text': chunk,
                'parse_mode': 'Markdown'
            }
            response = requests.post(url, json=payload)
            if not response.ok:
                print(f"Failed to send message chunk: {response.text}")
    else:
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        response = requests.post(url, json=payload)
        if response.ok:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message: {response.text}")

def get_gemini_response(api_key, prompt):
    """Get response from Gemini AI"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error getting Gemini response: {str(e)}"

def create_daily_prompt():
    """Create a daily prompt - customize this function"""
    today = datetime.now().strftime("%B %d, %Y")
    
    prompts = [
        f"Give me 3 interesting tech facts for {today}",
        f"What's a productivity tip for {today}?",
        f"Share an inspiring quote and explain why it's meaningful for {today}",
        f"What's happening in the world of AI today, {today}?",
        f"Give me a brief summary of an interesting scientific discovery and its implications for {today}"
    ]
    
    # You can rotate prompts or use random selection
    import random
    return random.choice(prompts)

def main():
    # Get environment variables
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    
    if not all([bot_token, chat_id, gemini_api_key]):
        print("Missing required environment variables!")
        return
    
    # Create daily prompt
    prompt = create_daily_prompt()
    
    # Get Gemini response
    print(f"Getting Gemini response for prompt: {prompt}")
    gemini_response = get_gemini_response(gemini_api_key, prompt)
    
    # Format message
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    message = f"""🤖 **Daily Gemini Update**
📅 {current_time}

**Prompt:** {prompt}

**Response:**
{gemini_response}

---
_Sent automatically via GitHub Actions_"""
    
    # Send to Telegram
    send_telegram_message(bot_token, chat_id, message)

if __name__ == "__main__":
    main()