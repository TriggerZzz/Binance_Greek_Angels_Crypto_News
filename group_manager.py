"""
Group Subscription Manager
Manages which Telegram groups are subscribed to daily reports
"""

import json
import os

GROUPS_FILE = "subscribed_groups.json"

def load_groups():
    """Load list of subscribed group IDs from file"""
    if not os.path.exists(GROUPS_FILE):
        return []
    
    try:
        with open(GROUPS_FILE, 'r') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception as e:
        print(f"Error loading groups: {e}")
        return []

def save_groups(groups):
    """Save list of subscribed group IDs to file"""
    try:
        with open(GROUPS_FILE, 'w') as f:
            json.dump(groups, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving groups: {e}")
        return False

def add_group(chat_id):
    """
    Add a new group to subscriptions
    Returns True if added, False if already exists
    """
    groups = load_groups()
    chat_id_str = str(chat_id)  # Ensure string for consistency
    
    if chat_id_str not in groups:
        groups.append(chat_id_str)
        save_groups(groups)
        print(f"✅ Added group {chat_id_str} to subscriptions")
        return True
    
    print(f"ℹ️ Group {chat_id_str} already subscribed")
    return False

def remove_group(chat_id):
    """
    Remove a group from subscriptions
    Returns True if removed, False if not found
    """
    groups = load_groups()
    chat_id_str = str(chat_id)
    
    if chat_id_str in groups:
        groups.remove(chat_id_str)
        save_groups(groups)
        print(f"✅ Removed group {chat_id_str} from subscriptions")
        return True
    
    print(f"ℹ️ Group {chat_id_str} not in subscriptions")
    return False

def get_all_groups():
    """Get all subscribed group IDs"""
    return load_groups()

def get_group_count():
    """Get count of subscribed groups"""
    return len(load_groups())

def is_subscribed(chat_id):
    """Check if a group is subscribed"""
    return str(chat_id) in load_groups()
