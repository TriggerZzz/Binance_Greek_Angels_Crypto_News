"""
Crypto News Telegram Bot with AI Image Generation
Multi-group support enabled

Author: TriggerZzz
License: MIT
Repository: https://github.com/TriggerZzz/Binance_Greek_Angels_Crypto_News
"""

import requests
import json
import os
from datetime import datetime
import sys
import time
from io import BytesIO
import group_manager

# ============================================================================
# CONFIGURATION - All sensitive data loaded from environment variables
# ============================================================================

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')  # Fallback for single-group mode
PERPLEXITY_API_KEY = os.environ.get('PERPLEXITY_API_KEY')
PERPLEXITY_QUERY = os.environ.get('PERPLEXITY_QUERY')
IMAGE_PROMPT = os.environ.get('IMAGE_PROMPT')

# API Configuration
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
PERPLEXITY_MODEL = "sonar"
PERPLEXITY_MAX_TOKENS = 2000
PERPLEXITY_TEMPERATURE = 0.3

# Image Generation Configuration
IMAGE_API_URL = "https://image.pollinations.ai/prompt/"
IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 1024

# Telegram Configuration
TELEGRAM_MAX_CAPTION_LENGTH = 1020


# ============================================================================
# PERPLEXITY AI FUNCTIONS
# ============================================================================

def query_perplexity(prompt, max_retries=3):
    """Query Perplexity AI API with retry logic"""
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
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
    
    for attempt in range(1, max_retries + 1):
        try:
            print(f"📡 Querying Perplexity API (attempt {attempt}/{max_retries})...")
            response = requests.post(
                PERPLEXITY_API_URL, 
                headers=headers, 
                json=payload, 
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            content = data['choices'][0]['message']['content']
            print(f"✅ Received response ({len(content)} characters)")
            
            return content
            
        except requests.exceptions.Timeout:
            print(f"❌ Attempt {attempt}: Timeout")
            if attempt < max_retries:
                wait_time = attempt * 5
                print(f"⏳ Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if hasattr(e, 'response') else None
            print(f"❌ Attempt {attempt}: HTTP Error {status_code}")
            
            if status_code and 500 <= status_code < 600:
                if attempt < max_retries:
                    wait_time = attempt * 10
                    print(f"⏳ Server error. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    if hasattr(e, 'response'):
                        print(f"   Response: {e.response.text[:500]}...")
            else:
                if hasattr(e, 'response'):
                    print(f"   Response: {e.response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Attempt {attempt}: {e}")
            if attempt < max_retries:
                time.sleep(attempt * 5)
                
        except (KeyError, IndexError) as e:
            print(f"❌ Attempt {attempt}: Parse error: {e}")
            return None
    
    print(f"❌ All {max_retries} attempts failed")
    return None


# ============================================================================
# IMAGE GENERATION FUNCTIONS
# ============================================================================

def generate_crypto_image():
    """Generate crypto image URL using Pollinations.ai"""
    try:
        date_suffix = datetime.utcnow().strftime('%Y%m%d')
        prompt_with_date = f"{IMAGE_PROMPT}, seed {date_suffix}"
        
        encoded_prompt = requests.utils.quote(prompt_with_date)
        
        image_url = (
            f"{IMAGE_API_URL}{encoded_prompt}"
            f"?width={IMAGE_WIDTH}"
            f"&height={IMAGE_HEIGHT}"
            f"&nologo=true"
            f"&enhance=true"
        )
        
        print(f"🎨 Generated image URL")
        print(f"   Preview: {image_url[:100]}...")
        
        return image_url
        
    except Exception as e:
        print(f"❌ Error generating image: {e}")
        return "https://via.placeholder.com/1024x1024/1a1a2e/16c79a?text=Crypto+News"


# ============================================================================
# TELEGRAM FUNCTIONS
# ============================================================================

def send_telegram_photo_to_chat(chat_id, photo_url, caption):
    """Send photo to specific chat"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    
    if len(caption) > TELEGRAM_MAX_CAPTION_LENGTH:
        caption = caption[:TELEGRAM_MAX_CAPTION_LENGTH] + "..."
    
    try:
        print(f"⬇️ Downloading image for chat {chat_id}...")
        img_response = requests.get(photo_url, timeout=60)
        img_response.raise_for_status()
        
        image_size = len(img_response.content)
        print(f"✅ Downloaded ({image_size:,} bytes)")
        
        print(f"📤 Sending to chat {chat_id}...")
        files = {
            'photo': ('crypto_news.png', BytesIO(img_response.content), 'image/png')
        }
        data = {
            'chat_id': chat_id,
            'caption': caption,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, files=files, data=data, timeout=60)
        response.raise_for_status()
        
        print(f"  ✅ Sent successfully to {chat_id}")
        return True
        
    except Exception as e:
        print(f"  ❌ Failed for {chat_id}: {e}")
        # Fallback to text only
        return send_telegram_message_to_chat(chat_id, caption)


def send_telegram_message_to_chat(chat_id, text):
    """Send text-only message to specific chat"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    params = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    
    try:
        response = requests.post(url, data=params, timeout=10)
        response.raise_for_status()
        print(f"  ✅ Text sent to {chat_id}")
        return True
    except Exception as e:
        print(f"  ❌ Text failed for {chat_id}: {e}")
        return False


def send_to_all_groups(image_url, content):
    """Send report to all subscribed groups"""
    groups = group_manager.get_all_groups()
    
    # Fallback: if no groups subscribed, use TELEGRAM_CHAT_ID
    if not groups:
        if TELEGRAM_CHAT_ID:
            print("ℹ️ No subscribed groups, using default TELEGRAM_CHAT_ID")
            groups = [TELEGRAM_CHAT_ID]
        else:
            print("❌ No groups subscribed and no default TELEGRAM_CHAT_ID!")
            return False
    
    print(f"📤 Sending to {len(groups)} group(s)...")
    
    success_count = 0
    failed_groups = []
    
    for chat_id in groups:
        success = send_telegram_photo_to_chat(chat_id, image_url, content)
        if success:
            success_count += 1
        else:
            failed_groups.append(chat_id)
        
        # Delay to avoid rate limits
        time.sleep(2)
    
    print(f"\n📊 Delivery Summary:")
    print(f"  ✅ Successful: {success_count}/{len(groups)}")
    if failed_groups:
        print(f"  ❌ Failed: {failed_groups}")
    
    return success_count > 0


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_environment():
    """Validate required environment variables"""
    required_vars = {
        'TELEGRAM_BOT_TOKEN': TELEGRAM_BOT_TOKEN,
        'PERPLEXITY_API_KEY': PERPLEXITY_API_KEY,
        'PERPLEXITY_QUERY': PERPLEXITY_QUERY,
        'IMAGE_PROMPT': IMAGE_PROMPT
    }
    
    missing_vars = [name for name, value in required_vars.items() if not value]
    
    return len(missing_vars) == 0, missing_vars


def print_config_status():
    """Print configuration status"""
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
            if name in ['TELEGRAM_BOT_TOKEN', 'PERPLEXITY_API_KEY']:
                display = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else "***"
            elif name in ['PERPLEXITY_QUERY', 'IMAGE_PROMPT']:
                display = f"{value[:50]}..." if len(value) > 50 else value
            else:
                display = value
            print(f"   ✅ {name}: {display}")
        else:
            print(f"   ⚠️ {name}: NOT SET")
    
    print(f"\n📊 Subscribed Groups: {group_manager.get_group_count()}")
    print("=" * 70 + "\n")


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Main execution function"""
    
    print("\n" + "=" * 70)
    print("🤖 CRYPTO NEWS TELEGRAM BOT - MULTI-GROUP")
    print("=" * 70)
    print(f"⏰ Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"🐍 Python: {sys.version.split()[0]}")
    
    # Validate environment
    is_valid, missing_vars = validate_environment()
    
    if not is_valid:
        print("\n❌ ERROR: Missing required variables!")
        print_config_status()
        print("\nMissing:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Set these in GitHub Secrets")
        sys.exit(1)
    
    print_config_status()
    
    # Step 1: Get crypto news
    print("=" * 70)
    print("STEP 1: Fetching Crypto News")
    print("=" * 70)
    
    content = query_perplexity(PERPLEXITY_QUERY)
    
    if not content:
        print("\n❌ Failed to get content from Perplexity")
        sys.exit(1)
    
    # Step 2: Generate image
    print("\n" + "=" * 70)
    print("STEP 2: Generating Image")
    print("=" * 70)
    
    image_url = generate_crypto_image()
    
    # Step 3: Send to all groups
    print("\n" + "=" * 70)
    print("STEP 3: Sending to Subscribed Groups")
    print("=" * 70)
    
    success = send_to_all_groups(image_url, content)
    
    # Final status
    print("\n" + "=" * 70)
    if success:
        print("✅ SUCCESS: Reports delivered!")
        print(f"📊 Content: {len(content)} chars")
        print(f"📱 Groups: {group_manager.get_group_count()}")
    else:
        print("❌ FAILED: Could not deliver reports")
    print("=" * 70 + "\n")
    
    sys.exit(0 if success else 1)


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
