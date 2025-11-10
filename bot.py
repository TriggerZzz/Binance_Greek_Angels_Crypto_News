import requests
import json
import os
from datetime import datetime

# Get secrets from environment variables
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
PERPLEXITY_API_KEY = os.environ.get('PERPLEXITY_API_KEY')
PERPLEXITY_QUERY = os.environ.get('PERPLEXITY_QUERY', 'Summarize today\'s top technology news')

def query_perplexity(prompt):
    """Query Perplexity API with the given prompt"""
    url = "https://api.perplexity.ai/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "sonar",  # Online model with web search
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that provides concise, well-structured daily reports."
            },
            {
                "role": "user",
                "content": f"{prompt} for {datetime.now().strftime('%B %d, %Y')}"
            }
        ],
        "max_tokens": 1500,
        "temperature": 0.2
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Extract the response content
        content = data['choices'][0]['message']['content']
        
        # Get sources if available
        sources = []
        if 'citations' in data:
            sources = [cite for cite in data.get('citations', [])]
        
        return content, sources
        
    except requests.exceptions.RequestException as e:
        print(f"Error querying Perplexity API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None, []

def send_telegram_message(text):
    """Send message to Telegram chat"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # Split message if it's too long (Telegram limit is 4096 characters)
    max_length = 4000
    messages = []
    
    if len(text) <= max_length:
        messages.append(text)
    else:
        # Split by paragraphs to maintain readability
        paragraphs = text.split('\n\n')
        current_message = ""
        
        for para in paragraphs:
            if len(current_message) + len(para) + 2 <= max_length:
                current_message += para + "\n\n"
            else:
                if current_message:
                    messages.append(current_message.strip())
                current_message = para + "\n\n"
        
        if current_message:
            messages.append(current_message.strip())
    
    # Send all message parts
    for i, msg in enumerate(messages):
        params = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            print(f"Message part {i+1}/{len(messages)} sent successfully!")
            
        except requests.exceptions.RequestException as e:
            print(f"Error sending Telegram message: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return False
    
    return True

def main():
    """Main function to orchestrate the bot"""
    print(f"Starting Perplexity-Telegram bot at {datetime.now()}")
    
    # Validate environment variables
    if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, PERPLEXITY_API_KEY]):
        print("ERROR: Missing required environment variables!")
        print(f"TELEGRAM_BOT_TOKEN: {'SET' if TELEGRAM_BOT_TOKEN else 'MISSING'}")
        print(f"TELEGRAM_CHAT_ID: {'SET' if TELEGRAM_CHAT_ID else 'MISSING'}")
        print(f"PERPLEXITY_API_KEY: {'SET' if PERPLEXITY_API_KEY else 'MISSING'}")
        return
    
    # Query Perplexity
    print(f"Querying Perplexity with: {PERPLEXITY_QUERY}")
    content, sources = query_perplexity(PERPLEXITY_QUERY)
    
    if content:
        # Format the message
        header = f"📊 *Daily Report - {datetime.now().strftime('%B %d, %Y')}*\n\n"
        footer = f"\n\n_Generated at {datetime.now().strftime('%H:%M UTC')}_"
        
        message = header + content + footer
        
        # Send to Telegram
        print("Sending message to Telegram...")
        success = send_telegram_message(message)
        
        if success:
            print("✅ Report sent successfully!")
        else:
            print("❌ Failed to send report")
    else:
        print("❌ Failed to get content from Perplexity")
        # Send error notification
        error_msg = f"⚠️ *Error Report*\n\nFailed to generate daily report at {datetime.now().strftime('%H:%M UTC')}"
        send_telegram_message(error_msg)

if __name__ == "__main__":
    main()
