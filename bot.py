"""
Crypto News Telegram Bot with AI Image Generation

This bot automatically fetches crypto market news using Perplexity AI,
generates accompanying images, and posts them to Telegram channels / groups.

Author: TriggerZ
License: MIT
Repository: https://github.com/TriggerZzz/Binance_Greek_Angels_Crypto_News
"""

import requests
import json
import os
from datetime import datetime
import sys

# ============================================================================
# CONFIGURATION - All sensitive data loaded from environment variables
# ============================================================================

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
PERPLEXITY_API_KEY = os.environ.get('PERPLEXITY_API_KEY')
PERPLEXITY_QUERY = os.environ.get('PERPLEXITY_QUERY')
IMAGE_PROMPT = os.environ.get('IMAGE_PROMPT')

# API Configuration
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
PERPLEXITY_MODEL = "sonar"  # Fast online model with web search
PERPLEXITY_MAX_TOKENS = 2000
PERPLEXITY_TEMPERATURE = 0.3

# Image Generation Configuration
IMAGE_API_URL = "https://image.pollinations.ai/prompt/"
IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 1024

# Telegram Configuration
TELEGRAM_MAX_CAPTION_LENGTH = 1020  # Telegram limit is 1024, leave buffer


# ============================================================================
# PERPLEXITY AI FUNCTIONS
# ============================================================================

def query_perplexity(prompt):
    """
    Query Perplexity AI API for crypto market news.
    
    Args:
        prompt (str): The query prompt to send to Perplexity
        
    Returns:
        str: The generated content, or None if request fails
    """
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Get current date for the query context
    current_date = datetime.utcnow().strftime('%B %d, %Y')
    
    payload = {
        "model": PERPLEXITY_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a professional crypto news analyst. "
                    "Follow user instructions exactly regarding formatting, "
                    "length, emojis, and hashtags. Do not mention images or "
                    "any visual content in your response."
                )
            },
            {
                "role": "user",
                "content": f"Today's date is {current_date}. {prompt}"
            }
        ],
        "max_tokens": PERPLEXITY_MAX_TOKENS,
        "temperature": PERPLEXITY_TEMPERATURE,
        "top_p": 0.9
    }
    
    try:
        print(f"📡 Querying Perplexity API...")
        response = requests.post(
            PERPLEXITY_API_URL, 
            headers=headers, 
            json=payload, 
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        # Extract the response content
        content = data['choices'][0]['message']['content']
        print(f"✅ Received response ({len(content)} characters)")
        
        return content
        
    except requests.exceptions.Timeout:
        print(f"❌ Error: Perplexity API request timed out")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error querying Perplexity API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Status code: {e.response.status_code}")
            print(f"   Response: {e.response.text}")
        return None
        
    except (KeyError, IndexError) as e:
        print(f"❌ Error parsing Perplexity response: {e}")
        return None


# ============================================================================
# IMAGE GENERATION FUNCTIONS
# ============================================================================

def generate_crypto_image():
    """
    Generate a crypto-themed image using Pollinations.ai (free service).
    
    Returns:
        str: URL of the generated image
    """
    try:
        # Add date to make each day's image unique
        date_suffix = datetime.utcnow().strftime('%Y%m%d')
        prompt_with_date = f"{IMAGE_PROMPT}, seed {date_suffix}"
        
        # Encode prompt for URL
        encoded_prompt = requests.utils.quote(prompt_with_date)
        
        # Build image URL with parameters
        image_url = (
            f"{IMAGE_API_URL}{encoded_prompt}"
            f"?width={IMAGE_WIDTH}"
            f"&height={IMAGE_HEIGHT}"
            f"&nologo=true"
            f"&enhance=true"
        )
        
        print(f"🎨 Generated image URL")
        print(f"   Preview: {image_url[:80]}...")
        
        return image_url
        
    except Exception as e:
        print(f"❌ Error generating image: {e}")
        # Return a fallback placeholder image
        return "https://via.placeholder.com/1024x1024/1a1a2e/16c79a?text=Crypto+News"


# ============================================================================
# TELEGRAM FUNCTIONS
# ============================================================================

def send_telegram_photo_with_caption(photo_url, caption):
    """
    Send a photo with caption to Telegram chat with better error handling.
    
    Args:
        photo_url (str): URL of the photo to send
        caption (str): Caption text (max 1024 characters)
        
    Returns:
        bool: True if successful, False otherwise
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    
    # Ensure caption doesn't exceed Telegram's limit
    if len(caption) > TELEGRAM_MAX_CAPTION_LENGTH:
        print(f"⚠️ Warning: Caption too long ({len(caption)} chars), truncating...")
        caption = caption[:TELEGRAM_MAX_CAPTION_LENGTH] + "..."
    
    # First, verify the image URL is accessible
    try:
        print(f"🔍 Verifying image URL accessibility...")
        img_check = requests.head(photo_url, timeout=10)
        if img_check.status_code != 200:
            print(f"⚠️ Warning: Image URL returned status {img_check.status_code}")
    except Exception as e:
        print(f"⚠️ Warning: Could not verify image URL: {e}")
    
    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "photo": photo_url,
        "caption": caption,
        "parse_mode": "Markdown"
    }
    
    try:
        print(f"📤 Sending photo to Telegram...")
        print(f"   Image URL: {photo_url[:100]}...")
        response = requests.post(url, data=params, timeout=60)
        
        # Print response for debugging
        print(f"   Response status: {response.status_code}")
        
        response.raise_for_status()
        print("✅ Photo with caption sent successfully!")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending photo to Telegram: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Status code: {e.response.status_code}")
            print(f"   Response: {e.response.text[:500]}")
        
        # Fallback: Try sending as text only if photo fails
        print("⚠️ Photo failed, attempting to send as text only...")
        return send_telegram_message(caption)
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def send_telegram_message(text):
    """
    Fallback function to send text-only message to Telegram.
    
    Args:
        text (str): Message text to send
        
    Returns:
        bool: True if successful, False otherwise
    """
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
        print(f"❌ Error sending text message to Telegram: {e}")
        return False


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_environment():
    """
    Validate that all required environment variables are set.
    
    Returns:
        tuple: (bool, list) - (success status, list of missing variables)
    """
    required_vars = {
        'TELEGRAM_BOT_TOKEN': TELEGRAM_BOT_TOKEN,
        'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID,
        'PERPLEXITY_API_KEY': PERPLEXITY_API_KEY,
        'PERPLEXITY_QUERY': PERPLEXITY_QUERY,
        'IMAGE_PROMPT': IMAGE_PROMPT
    }
    
    missing_vars = [name for name, value in required_vars.items() if not value]
    
    return len(missing_vars) == 0, missing_vars


def print_config_status():
    """Print configuration status for debugging."""
    print("\n📋 Configuration Status:")
    print("=" * 70)
    
    configs = {
        'TELEGRAM_BOT_TOKEN': TELEGRAM_BOT_TOKEN,
        'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID,
        'PERPLEXITY_API_KEY': PERPLEXITY_API_KEY,
        'PERPLEXITY_QUERY': PERPLEXITY_QUERY,
        'IMAGE_PROMPT': IMAGE_PROMPT
    }
    
    for name, value in configs.items():
        if value:
            # Show first/last few chars for security
            if name in ['TELEGRAM_BOT_TOKEN', 'PERPLEXITY_API_KEY']:
                display = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else "***"
            elif name in ['PERPLEXITY_QUERY', 'IMAGE_PROMPT']:
                display = f"{value[:50]}..." if len(value) > 50 else value
            else:
                display = value
            print(f"   ✅ {name}: {display}")
        else:
            print(f"   ❌ {name}: NOT SET")
    
    print("=" * 70 + "\n")


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """
    Main function to orchestrate the crypto news bot workflow.
    
    Workflow:
    1. Validate environment variables
    2. Query Perplexity AI for crypto news
    3. Generate accompanying image
    4. Post to Telegram with image and caption
    """
    
    # Print header
    print("\n" + "=" * 70)
    print("🤖 CRYPTO NEWS TELEGRAM BOT")
    print("=" * 70)
    print(f"⏰ Execution Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"🐍 Python Version: {sys.version.split()[0]}")
    
    # Validate environment variables
    is_valid, missing_vars = validate_environment()
    
    if not is_valid:
        print("\n❌ ERROR: Missing required environment variables!")
        print_config_status()
        print("\nMissing variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Please set all required secrets in GitHub repository settings.")
        print("   Settings → Secrets and variables → Actions → New repository secret")
        print("\nRequired secrets:")
        print("   1. TELEGRAM_BOT_TOKEN - Your Telegram bot token from @BotFather")
        print("   2. TELEGRAM_CHAT_ID - Your Telegram chat/group ID")
        print("   3. PERPLEXITY_API_KEY - Your Perplexity API key")
        print("   4. PERPLEXITY_QUERY - Your custom crypto news query")
        print("   5. IMAGE_PROMPT - Your custom image generation prompt")
        
        # Try to send error notification if bot credentials exist
        if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
            error_msg = (
                f"⚠️ *Bot Configuration Error*\n\n"
                f"Missing environment variables:\n"
                f"{', '.join(missing_vars)}\n\n"
                f"Check GitHub Actions secrets configuration."
            )
            send_telegram_message(error_msg)
        
        sys.exit(1)
    
    print_config_status()
    
    # Step 1: Query Perplexity for crypto news
    print("=" * 70)
    print("STEP 1: Fetching Crypto News from Perplexity AI")
    print("=" * 70)
    
    content = query_perplexity(PERPLEXITY_QUERY)
    
    if not content:
        print("\n❌ FAILED: Could not get content from Perplexity API")
        
        # Send error notification
        error_msg = (
            f"⚠️ *Daily Report Failed*\n\n"
            f"Could not generate crypto news report.\n\n"
            f"Time: {datetime.utcnow().strftime('%H:%M UTC')}\n"
            f"Date: {datetime.utcnow().strftime('%Y-%m-%d')}\n\n"
            f"Please check GitHub Actions logs for details."
        )
        send_telegram_message(error_msg)
        sys.exit(1)
    
    # Step 2: Generate image
    print("\n" + "=" * 70)
    print("STEP 2: Generating Crypto-Themed Image")
    print("=" * 70)
    
    image_url = generate_crypto_image()
    
    # Step 3: Send to Telegram
    print("\n" + "=" * 70)
    print("STEP 3: Posting to Telegram")
    print("=" * 70)
    
    success = send_telegram_photo_with_caption(image_url, content)
    
    # Print final status
    print("\n" + "=" * 70)
    if success:
        print("✅ SUCCESS: Daily crypto report delivered successfully!")
        print(f"📊 Report length: {len(content)} characters")
        print(f"🖼️ Image URL: {image_url}")
        print(f"💬 Telegram Chat ID: {TELEGRAM_CHAT_ID}")
    else:
        print("❌ FAILED: Could not deliver report to Telegram")
        print("Check the error messages above for details")
    print("=" * 70 + "\n")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Process interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
        
