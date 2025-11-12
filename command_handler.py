"""
Telegram Command Handler Bot
Handles interactive commands for the Crypto Market Daily bot
"""

import os
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import group_manager

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    chat_type = update.effective_chat.type
    chat_id = update.effective_chat.id
    
    if chat_type == "private":
        # Private chat - show instructions
        await update.message.reply_text(
            "📊 *Welcome to Crypto Market Daily!*\n\n"
            "🚀 *How to Get Started:*\n"
            "1. Add me to your Telegram group\n"
            "2. Make me an admin (required for posting)\n"
            "3. Send /subscribe in the group\n"
            "4. Receive daily reports Mon-Fri at 17:00 UTC!\n\n"
            "📋 Use /help to see all commands\n"
            "ℹ️ Use /about to learn more",
            parse_mode='Markdown'
        )
    else:
        # Group chat - auto-subscribe
        chat_name = update.effective_chat.title
        
        if group_manager.add_group(chat_id):
            await update.message.reply_text(
                f"✅ *Subscribed Successfully!*\n\n"
                f"'{chat_name}' will now receive daily crypto market reports!\n\n"
                f"📅 Schedule: Monday-Friday\n"
                f"🕐 Time: 17:00 UTC\n"
                f"📊 Content: Market analysis + AI images\n\n"
                f"Use /unsubscribe to stop reports\n"
                f"Use /help for more commands",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                "✅ *Already Subscribed!*\n\n"
                "This group is receiving daily reports.\n\n"
                "Use /help to see available commands",
                parse_mode='Markdown'
            )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        "❓ *Available Commands:*\n\n"
        "*Group Management:*\n"
        "/subscribe - Subscribe this group to daily reports\n"
        "/unsubscribe - Unsubscribe from daily reports\n"
        "/status - Check subscription status\n\n"
        "*Information:*\n"
        "/help - Show this help message\n"
        "/about - About this bot\n"
        "/schedule - View delivery schedule\n"
        "/privacy - Privacy policy\n\n"
        "*Support:*\n"
        "/feedback - Send feedback or report issues\n\n"
        "📊 Reports delivered Mon-Fri at 17:00 UTC",
        parse_mode='Markdown'
    )

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /subscribe command"""
    chat_type = update.effective_chat.type
    
    if chat_type == "private":
        await update.message.reply_text(
            "⚠️ *Group Command Only*\n\n"
            "This command only works in groups.\n\n"
            "To subscribe:\n"
            "1. Add me to your group\n"
            "2. Use /subscribe there",
            parse_mode='Markdown'
        )
        return
    
    chat_id = update.effective_chat.id
    chat_name = update.effective_chat.title
    
    if group_manager.add_group(chat_id):
        await update.message.reply_text(
            f"✅ *Subscribed!*\n\n"
            f"'{chat_name}' will receive daily crypto reports.\n\n"
            f"📅 Monday-Friday at 17:00 UTC\n"
            f"📊 Market analysis with AI-generated images\n\n"
            f"Total subscribers: {group_manager.get_group_count()}",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            "ℹ️ *Already Subscribed*\n\n"
            "This group is already receiving daily reports!",
            parse_mode='Markdown'
        )

async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /unsubscribe command"""
    chat_type = update.effective_chat.type
    
    if chat_type == "private":
        await update.message.reply_text(
            "⚠️ This command only works in groups."
        )
        return
    
    chat_id = update.effective_chat.id
    chat_name = update.effective_chat.title
    
    if group_manager.remove_group(chat_id):
        await update.message.reply_text(
            f"✅ *Unsubscribed*\n\n"
            f"'{chat_name}' will no longer receive daily reports.\n\n"
            f"Use /subscribe to re-enable anytime.",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            "ℹ️ This group wasn't subscribed to daily reports.",
            parse_mode='Markdown'
        )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    chat_type = update.effective_chat.type
    
    if chat_type == "private":
        total_groups = group_manager.get_group_count()
        await update.message.reply_text(
            f"🔄 *Bot Status*\n\n"
            f"✅ Online and operational\n"
            f"📊 Total subscribed groups: {total_groups}\n"
            f"⏰ Next report: Next weekday at 17:00 UTC\n"
            f"🤖 Powered by Perplexity AI\n\n"
            f"Add me to a group to subscribe!",
            parse_mode='Markdown'
        )
    else:
        chat_id = update.effective_chat.id
        is_sub = group_manager.is_subscribed(chat_id)
        status_emoji = "✅" if is_sub else "❌"
        status_text = "Subscribed" if is_sub else "Not Subscribed"
        
        await update.message.reply_text(
            f"🔄 *Group Status*\n\n"
            f"{status_emoji} Status: {status_text}\n"
            f"📅 Schedule: Mon-Fri, 17:00 UTC\n"
            f"🤖 Bot: Online\n\n"
            f"{'Use /unsubscribe to stop reports' if is_sub else 'Use /subscribe to get daily reports'}",
            parse_mode='Markdown'
        )

async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /schedule command"""
    await update.message.reply_text(
        "⏰ *Delivery Schedule*\n\n"
        "📅 *Days:* Monday - Friday\n"
        "🕐 *Time:* 17:00 UTC\n"
        "🌍 *Your Time:* Calculate your local timezone\n\n"
        "*No reports on weekends.*\n\n"
        "Each report includes:\n"
        "• Real-time market data\n"
        "• Technical analysis\n"
        "• Institutional sentiment\n"
        "• AI-generated images\n\n"
        "🔔 Reports are delivered automatically!",
        parse_mode='Markdown'
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /about command"""
    await update.message.reply_text(
        "ℹ️ *About Crypto Market Daily*\n\n"
        "🤖 AI-powered crypto market news bot\n\n"
        "*Technology Stack:*\n"
        "🧠 AI: Perplexity API\n"
        "🎨 Images: Pollinations.ai\n"
        "⚙️ Automation: GitHub Actions\n"
        "📱 Platform: Telegram Bot API\n\n"
        "*Features:*\n"
        "• Daily market analysis\n"
        "• Real-time data & percentages\n"
        "• Macroeconomic insights\n"
        "• Institutional sentiment\n"
        "• AI-generated visuals\n\n"
        "🌐 *Open Source:*\n"
        "github.com/TriggerZzz/Binance_Greek_Angels_Crypto_News\n\n"
        "⭐ Star us on GitHub!",
        parse_mode='Markdown'
    )

async def privacy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /privacy command"""
    await update.message.reply_text(
        "🔒 *Privacy Policy*\n\n"
        "*Data Collection:*\n"
        "✅ We store: Group/Chat IDs (for delivery)\n"
        "❌ We DON'T store: Messages, user data, personal info\n\n"
        "*Data Usage:*\n"
        "• Chat IDs used ONLY for report delivery\n"
        "• No data shared with third parties\n"
        "• No analytics or tracking\n\n"
        "*Third-Party Services:*\n"
        "• Perplexity AI (news generation)\n"
        "• Pollinations.ai (image generation)\n"
        "• GitHub (hosting & automation)\n\n"
        "*Your Rights:*\n"
        "• Unsubscribe anytime: /unsubscribe\n"
        "• Data deleted immediately on unsubscribe\n\n"
        "*Open Source & Transparent:*\n"
        "Review our code on GitHub\n\n"
        "⚠️ *Disclaimer:* Informational only, not financial advice.",
        parse_mode='Markdown'
    )

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /feedback command"""
    await update.message.reply_text(
        "💬 *Feedback & Support*\n\n"
        "We'd love to hear from you!\n\n"
        "🐛 *Report Bugs:*\n"
        "github.com/TriggerZzz/Binance_Greek_Angels_Crypto_News/issues\n\n"
        "⭐ *Like This Bot?*\n"
        "Star us on GitHub!\n\n"
        "💡 *Feature Requests:*\n"
        "Open an issue on GitHub with your idea\n\n"
        "📧 *Contact:*\n"
        "Create a GitHub issue for fastest response\n\n"
        "Thank you for using Crypto Market Daily! 🚀",
        parse_mode='Markdown'
    )

def main():
    """Main function to run the command handler bot"""
    
    # Validate bot token
    if not TELEGRAM_BOT_TOKEN:
        print("❌ ERROR: TELEGRAM_BOT_TOKEN environment variable not set!")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🤖 CRYPTO MARKET DAILY - COMMAND HANDLER")
    print("=" * 60)
    print(f"Token: {TELEGRAM_BOT_TOKEN[:8]}...{TELEGRAM_BOT_TOKEN[-4:]}")
    print(f"Subscribed groups: {group_manager.get_group_count()}")
    print("=" * 60 + "\n")
    
    # Create application
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("schedule", schedule))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("privacy", privacy))
    app.add_handler(CommandHandler("feedback", feedback))
    
    # Start bot
    print("✅ Command handler bot is running...")
    print("📝 Listening for commands from users...\n")
    
    try:
        app.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        print("\n⚠️ Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
