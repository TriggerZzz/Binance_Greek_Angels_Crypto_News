"""
Simple file-based storage for managing multiple Telegram groups
"""
import json
import os

GROUPS_FILE = "subscribed_groups.json"

def load_groups():
    """Load list of subscribed group IDs"""
    if not os.path.exists(GROUPS_FILE):
        return []
    
    try:
        with open(GROUPS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_groups(groups):
    """Save list of subscribed group IDs"""
    with open(GROUPS_FILE, 'w') as f:
        json.dump(groups, f, indent=2)

def add_group(chat_id):
    """Add a new group to subscriptions"""
    groups = load_groups()
    if chat_id not in groups:
        groups.append(chat_id)
        save_groups(groups)
        return True
    return False

def remove_group(chat_id):
    """Remove a group from subscriptions"""
    groups = load_groups()
    if chat_id in groups:
        groups.remove(chat_id)
        save_groups(groups)
        return True
    return False

def get_all_groups():
    """Get all subscribed groups"""
    return load_groups()
