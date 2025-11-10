import requests
import json
import os
from datetime import datetime
import hashlib

# Get secrets from environment variables
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
PERPLEXITY_API_KEY = os.environ.get('PERPLEXITY_API_KEY')
PERPLEXITY_QUERY = os.environ.get('PERPLEXITY_QUERY')
IMAGE_PROMPT = os.environ.get('IMAGE_PROMPT', 
    'crypto market trading floor, bitcoin ethereum coins, financial charts screens, '
    'cinematic scene, HDR lighting, epic composition, hyper-realistic, '
    'cinematic photo, professional photography, 8k quality, dramatic lighting')

def query_perplexity(prompt):
    """Query Perplexity API with the given prompt"""
    url = "https://api.perplexity.ai/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Get current date for the query
    current_date = datetime.utcnow().strftime('%B %d, %Y')
    
    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": "You are a professional crypto news analyst. Follow user instructions exactly regarding formatting, length, emojis, and hashtags. Do not mention images."
            },
            {
                "role": "user",
                "content": f"Today's date is {current_date}. {prompt}"
            }
        ],
        "max_tokens": 2000,
        "temperature": 0.3,
        "top_p": 0.9
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Extract the response content
        content = data['choices'][0]['message']['content']
        
        return content
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error querying Perplexity API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response: {e.response.text}")
        return None

def generate_crypto_image():
    """Generate crypto-themed image using Pollinations.ai (free)"""
    
    # Add date to make each day's image unique
    date_suffix = datetime.utcnow().strftime('%Y%m%d')
    prompt_with_date = f"{IMAGE_PROMPT}, seed {date_suffix}"
    
    # Encode prompt for URL
    encoded_prompt = requests.utils.quote(prompt_with_date)
    
    # Pollinations.ai - Free AI image generation
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&enhance=true"
    
    print(f"🎨 Generated image URL: {image_url[:100]}...")
    return image_url

def send_telegram_photo_with_caption(photo_url, caption):
    """Send photo to Telegram with caption"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    
    # Telegram caption limit is 1024 characters
    if len(caption) > 1020:
        caption = caption[:1020] + "..."
    
    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "photo": photo_url,
        "caption": caption,
        "parse_mode": "Markdown"
    }
    
    try:
        print(f"📤 Sending photo to Telegram...")
        response = requests.post(url, data=params, timeout=60)
        response.raise_for_status()
        print("✅ Photo with caption sent successfully!")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending photo: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        
        # Fallback: Try sending as text only if photo fails
        print("⚠️ Photo failed, attempting to send as text only...")
        return send_telegram_message(caption)

def send_telegram_message(text):
    """Fallback: Send text-only message to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    
    try:
        response = requests.post(url, data=params, timeout=10)
        response.raise_for_status()
        print("✅ Text message sent successfully!")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending text message: {e}")
        return False

def main():
    """Main function to orchestrate the bot"""
    print("=" * 70)
    print(f"🤖 Crypto News Bot with Image Generation")
    print(f"⏰ Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("=" * 70)
    
    # Validate environment variables
    required_vars = {
        'TELEGRAM_BOT_TOKEN': TELEGRAM_BOT_TOKEN,
        'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID,
        'PERPLEXITY_API_KEY': PERPLEXITY_API_KEY,
        'PERPLEXITY_QUERY': PERPLEXITY_QUERY
    }
    
    missing_vars = [name for name, value in required_vars.items() if not value]
    
    if missing_vars:
        print("❌ ERROR: Missing required environment variables!")
        for var_name, var_value in required_vars.items():
            status = '✅ SET' if var_value else '❌ MISSING'
            print(f"   {var_name}: {status}")
        
        # Send error notification
        if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
            error_msg = (
                f"⚠️ *Bot Configuration Error*\n\n"
                f"Missing variables: {', '.join(missing_vars)}\n\n"
                f"Check GitHub Actions secrets."
            )
            send_telegram_message(error_msg)
        return
    
    # Step 1: Query Perplexity for crypto news
    print(f"\n📡 Step 1: Querying Perplexity API for crypto news...")
    print(f"Query preview: {PERPLEXITY_QUERY[:80]}...")
    
    content = query_perplexity(PERPLEXITY_QUERY)
    
    if not content:
        print("\n❌ Failed to get content from Perplexity API")
        error_msg = (
            f"⚠️ *Daily Report Failed*\n\n"
            f"Could not generate crypto news.\n"
            f"Time: {datetime.utcnow().strftime('%H:%M UTC')}"
        )
        send_telegram_message(error_msg)
        return
    
    print(f"✅ Received response ({len(content)} characters)")
    
    # Step 2: Generate image
    print(f"\n🎨 Step 2: Generating crypto-themed image...")
    image_url = generate_crypto_image()
    print(f"✅ Image generated successfully!")
    
    # Step 3: Send to Telegram (photo with caption)
    print(f"\n📤 Step 3: Sending to Telegram...")
    success = send_telegram_photo_with_caption(image_url, content)
    
    # Final status
    print("\n" + "=" * 70)
    if success:
        print("✅ COMPLETE: Daily crypto report with image sent successfully!")
    else:
        print("⚠️ PARTIAL: Report generated but delivery had issues")
    print("=" * 70)

if __name__ == "__main__":
    main()
