"""
Crypto News Telegram Bot with AI Image Generation - FIXED
REAL-TIME DATA + UNIQUE IMAGES EVERY DAY

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
import hashlib

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
PERPLEXITY_MODEL = "sonar"
PERPLEXITY_MAX_TOKENS = 2000
PERPLEXITY_TEMPERATURE = 0.2

# Image Generation Configuration
IMAGE_API_URL = "https://image.pollinations.ai/prompt/"
IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 1024

# Telegram Configuration
TELEGRAM_MAX_CAPTION_LENGTH = 1020


# ============================================================================
# PERPLEXITY AI FUNCTIONS - REAL-TIME DATA FETCHING
# ============================================================================

def query_perplexity(prompt, max_retries=3):
    """
    Query Perplexity AI API for REAL-TIME crypto market news.
    Uses 'sonar' model which searches the web for current data.
    """
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    current_date = datetime.utcnow().strftime('%B %d, %Y')
    current_time = datetime.utcnow().strftime('%H:%M UTC')
    
    payload = {
        "model": PERPLEXITY_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a professional crypto market analyst. "
                    "MANDATORY: Use REAL current market data from today. "
                    "Search the web for the LATEST Bitcoin, Ethereum, and altcoin prices RIGHT NOW. "
                    "Include TODAY'S actual prices, percentage changes, and real market events. "
                    "Do NOT generate or guess data. Only use real data from today. "
                    "Format exactly as requested. No images, no guidance, only facts and numbers."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Today's date: {current_date}\n"
                    f"Current time: {current_time} UTC\n\n"
                    f"IMPORTANT: Fetch REAL-TIME data from TODAY ONLY.\n\n"
                    f"{prompt}"
                )
            }
        ],
        "max_tokens": PERPLEXITY_MAX_TOKENS,
        "temperature": PERPLEXITY_TEMPERATURE,
        "top_p": 0.9
    }
    
    for attempt in range(1, max_retries + 1):
        try:
            print(f"📡 Querying Perplexity API for REAL-TIME data (attempt {attempt}/{max_retries})...")
            response = requests.post(
                PERPLEXITY_API_URL, 
                headers=headers, 
                json=payload, 
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            
            content = data['choices'][0]['message']['content']
            print(f"✅ Received REAL-TIME response ({len(content)} characters)")
            
            return content
            
        except requests.exceptions.Timeout:
            print(f"❌ Attempt {attempt}: Timeout (Perplexity is searching the web...)")
            if attempt < max_retries:
                wait_time = attempt * 10
                print(f"⏳ Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if hasattr(e, 'response') else None
            print(f"❌ Attempt {attempt}: HTTP Error {status_code}")
            
            if status_code and 500 <= status_code < 600:
                if attempt < max_retries:
                    wait_time = attempt * 15
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
                time.sleep(attempt * 10)
                
        except (KeyError, IndexError) as e:
            print(f"❌ Attempt {attempt}: Parse error: {e}")
            return None
    
    print(f"❌ All {max_retries} attempts failed - could not fetch real-time data")
    return None


# ============================================================================
# IMAGE GENERATION FUNCTIONS - UNIQUE IMAGES EVERY DAY
# ============================================================================

def generate_unique_image_prompt():
    """
    Generate a truly unique prompt variation for each day.
    Uses multiple randomization techniques to ensure different images.
    """
    
    # Get current date and time for maximum uniqueness
    now = datetime.utcnow()
    date_str = now.strftime('%Y%m%d')
    hour_str = now.strftime('%H')
    
    # Create a hash-based seed for even more randomness
    hash_seed = hashlib.md5(f"{date_str}{hour_str}".encode()).hexdigest()[:8]
    
    # Different image style variations for each day
    style_variations = [
        "cinematic epic composition",  # Day 1, 5, 9...
        "dramatic HDR photography",     # Day 2, 6, 10...
        "ultra-detailed 8K render",     # Day 3, 7, 11...
        "hyper-realistic professional", # Day 4, 8, 12...
        "sleek modern digital art",     # Day 5, 9...
    ]
    
    # Different angle/perspective variations
    angle_variations = [
        "wide sweeping vista",
        "close-up detail focus",
        "top-down perspective",
        "dynamic diagonal composition",
        "centered balanced view",
    ]
    
    # Different lighting variations
    lighting_variations = [
        "neon blue and gold lighting",
        "dramatic volumetric lighting",
        "cinematic rim lighting",
        "electric neon glow",
        "high-contrast theatrical lighting",
    ]
    
    # Get day of month to cycle through variations
    day_of_month = now.day
    month_value = now.month
    
    style = style_variations[day_of_month % len(style_variations)]
    angle = angle_variations[month_value % len(angle_variations)]
    lighting = lighting_variations[(day_of_month + month_value) % len(lighting_variations)]
    
    # Build the unique prompt with today's variations
    unique_prompt = (
        f"{IMAGE_PROMPT}, {style}, {angle}, {lighting}, "
        f"seed variation {date_str}{hash_seed}, "
        f"unique daily composition"
    )
    
    return unique_prompt


def generate_crypto_image():
    """Generate truly unique crypto-themed image with daily variations"""
    try:
        # Generate unique prompt for today
        unique_prompt = generate_unique_image_prompt()
        
        # Encode prompt for URL
        encoded_prompt = requests.utils.quote(unique_prompt)
        
        # Add random parameters to force cache bypass
        now = datetime.utcnow()
        timestamp = now.strftime('%Y%m%d%H%M%S')
        random_param = hashlib.md5(timestamp.encode()).hexdigest()[:8]
        
        # Build image URL with multiple unique parameters
        image_url = (
            f"{IMAGE_API_URL}{encoded_prompt}"
            f"?width={IMAGE_WIDTH}"
            f"&height={IMAGE_HEIGHT}"
            f"&nologo=true"
            f"&enhance=true"
            f"&version={random_param}"  # Force unique version each time
            f"&timestamp={timestamp}"    # Prevent caching
        )
        
        print(f"🎨 Generated UNIQUE image URL")
        print(f"   Date variant: {now.strftime('%Y-%m-%d')}")
        print(f"   Style variation applied")
        print(f"   Preview: {image_url[:100]}...")
        
        return image_url
        
    except Exception as e:
        print(f"❌ Error generating image: {e}")
        return "https://via.placeholder.com/1024x1024/1a1a2e/16c79a?text=Crypto+News"


# ============================================================================
# TELEGRAM FUNCTIONS
# ============================================================================

def send_telegram_photo_downloaded(photo_url, caption):
    """
    Download image first, then send to Telegram as file.
    This method is more reliable than sending by URL.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    
    if len(caption) > TELEGRAM_MAX_CAPTION_LENGTH:
        print(f"⚠️ Warning: Caption too long ({len(caption)} chars), truncating...")
        caption = caption[:TELEGRAM_MAX_CAPTION_LENGTH] + "..."
    
    try:
        print(f"⬇️ Downloading image...")
        img_response = requests.get(photo_url, timeout=60)
        img_response.raise_for_status()
        
        image_size = len(img_response.content)
        print(f"✅ Downloaded ({image_size:,} bytes)")
        
        print(f"📤 Sending photo to Telegram...")
        files = {
            'photo': ('crypto_news.png', BytesIO(img_response.content), 'image/png')
        }
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'caption': caption,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, files=files, data=data, timeout=60)
        response.raise_for_status()
        
        print("✅ Photo with caption sent successfully!")
        return True
        
    except requests.exceptions.Timeout:
        print(f"❌ Timeout while downloading or sending image")
        print("⚠️ Falling back to text-only message...")
        return send_telegram_message(caption)
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Status: {e.response.status_code}")
            print(f"   Response: {e.response.text[:500]}")
        print("⚠️ Falling back to text-only message...")
        return send_telegram_message(caption)
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("⚠️ Falling back to text-only message...")
        return send_telegram_message(caption)


def send_telegram_message(text):
    """Fallback: send text-only message to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    
    try:
        print(f"📤 Sending text-only message to Telegram...")
        response = requests.post(url, data=params, timeout=10)
        response.raise_for_status()
        print("✅ Text message sent successfully!")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return False


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_environment():
    """Validate that all required environment variables are set"""
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
            print(f"   ❌ {name}: NOT SET")
    
    print("=" * 70 + "\n")


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Main execution function"""
    
    print("\n" + "=" * 70)
    print("🤖 CRYPTO NEWS TELEGRAM BOT - REAL-TIME DATA + UNIQUE IMAGES")
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
        sys.exit(1)
    
    print_config_status()
    
    # Step 1: Get REAL-TIME crypto news
    print("=" * 70)
    print("STEP 1: Fetching REAL-TIME Crypto News from Perplexity AI")
    print("=" * 70)
    
    content = query_perplexity(PERPLEXITY_QUERY)
    
    if not content:
        print("\n❌ Failed to get REAL-TIME content from Perplexity")
        error_msg = (
            f"⚠️ *Daily Report Failed*\n\n"
            f"Could not fetch real-time crypto data.\n"
            f"Time: {datetime.utcnow().strftime('%H:%M UTC')}\n"
            f"Date: {datetime.utcnow().strftime('%Y-%m-%d')}\n\n"
            f"Check GitHub Actions logs for details."
        )
        send_telegram_message(error_msg)
        sys.exit(1)
    
    # Step 2: Generate UNIQUE image
    print("\n" + "=" * 70)
    print("STEP 2: Generating UNIQUE Crypto Image")
    print("=" * 70)
    
    image_url = generate_crypto_image()
    
    # Step 3: Send to Telegram
    print("\n" + "=" * 70)
    print("STEP 3: Sending to Telegram")
    print("=" * 70)
    
    success = send_telegram_photo_downloaded(image_url, content)
    
    # Final status
    print("\n" + "=" * 70)
    if success:
        print("✅ SUCCESS: REAL-TIME report with UNIQUE image delivered!")
        print(f"📊 Content: {len(content)} chars")
        print(f"🎨 Image: Unique daily variation")
    else:
        print("❌ FAILED: Could not deliver report")
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
