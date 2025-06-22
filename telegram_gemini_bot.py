import os
import requests
import google.genai as genai
from google.genai import types
from datetime import datetime
import pytz
from dotenv import load_dotenv
load_dotenv()

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
                'disable_web_page_preview': True
            }
            response = requests.post(url, json=payload, timeout=10)
            if not response.ok:
                print(f"Failed to send message chunk: {response.text}")
            else:
                print(f"Message chunk sent successfully!")
    else:
        payload = {
            'chat_id': chat_id,
            'text': message,
            'disable_web_page_preview': True
        }
        response = requests.post(url, json=payload, timeout=10)
        if response.ok:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message: {response.text}")


def get_gemini_response(api_key, prompt):
    try:
        # Configure the client
        client = genai.Client(api_key=api_key)

        # Define the grounding tool
        grounding_tool = types.Tool(
            google_search=types.GoogleSearch()
        )

        # Configure generation settings
        config = types.GenerateContentConfig(
            tools=[grounding_tool],
            temperature=0.7,
            top_p=0.9,
            top_k=40,
            max_output_tokens=1500  # Reduced to avoid long responses
        )

        print("DEBUG: Using model with Google Search grounding tool")

        # Make the request with grounding
        print("DEBUG: Making API request...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )

        print("DEBUG: API response received")

        # Get the response text and add grounding info if available
        response_text = response.text
        print(f"DEBUG: Response text length: {len(response_text)}")

        return response_text

    except Exception as e:
        error_msg = f"Error getting Gemini response: {str(e)}"
        print(f"DEBUG: {error_msg}")  # Add debug logging
        import traceback
        traceback.print_exc()
        return error_msg


def main():
    # Get environment variables
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    
    if not all([bot_token, chat_id, gemini_api_key]):
        print("Missing required environment variables!")
        return
    
    # Create daily prompt
    prompt = """
    Give me a brief summary of today's news from Indonesia.
    Focus on 5 most important events and avoid unnecessary details.
    Don't repeat the same news and make sure it's only a single list of news.
    Give short headline for each news with this format '1. {Headline Title}' and then start a new line.
    Give 1 line spacing between news items. Don't use any markdown styling.
    Start directly with the list. No need for any introduction.
    Also end directly with the list. No need for any closing remark.
    """
    
    # Get Gemini response
    print(f"Getting Gemini response for prompt: {prompt}")
    gemini_response = get_gemini_response(gemini_api_key, prompt)
    
    # Format message with Indonesia timezone (UTC+7)
    indonesia_tz = pytz.timezone('Asia/Jakarta')
    current_time = datetime.now(indonesia_tz).strftime("%Y-%m-%d %H:%M:%S %Z")
    message = f"""📰 News from Indonesia
📅 {current_time}

{gemini_response}

---
Sent automatically via GitHub Actions"""
    
    # Send to Telegram
    send_telegram_message(bot_token, chat_id, message)

if __name__ == "__main__":
    main()