"""
Simple command handler for Telegram bot
This is optional - only if you want interactive commands
"""

import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 *Welcome to Crypto Market Daily!*\n\n"
        "Receive professional crypto market reports every weekday at 17:00 UTC.\n\n"
        "🚀 Features:\n"
        "• AI-powered market analysis\n"
        "• Real-time data & percentages\n"
        "• Institutional sentiment insights\n"
        "• Key market highlights\n\n"
        "Use /help to see available commands.",
        parse_mode='Markdown'
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❓ *Available Commands:*\n\n"
        "/start - Welcome message\n"
        "/help - This help message\n"
        "/status - Bot status\n"
        "/schedule - Delivery schedule\n"
        "/about - About this bot\n"
        "/privacy - Privacy policy\n"
        "/feedback - Send feedback\n\n"
        "📊 Reports are delivered automatically Mon-Fri at 17:00 UTC.",
        parse_mode='Markdown'
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔄 *Bot Status*\n\n"
        "✅ Online and operational\n"
        "📅 Next report: Tomorrow at 17:00 UTC\n"
        "🤖 Powered by Perplexity AI\n"
        "⏰ Schedule: Monday-Friday",
        parse_mode='Markdown'
    )

async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⏰ *Delivery Schedule*\n\n"
        "📅 Days: Monday - Friday\n"
        "🕐 Time: 17:00 UTC\n"
        "🌍 Your timezone: Calculate your local time\n\n"
        "No reports on weekends.\n"
        "All reports include market data, analysis, and AI-generated images.",
        parse_mode='Markdown'
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ *About Crypto Market Daily*\n\n"
        "🤖 AI-powered crypto news bot\n"
        "📊 Data sources: Multiple crypto APIs\n"
        "🧠 Powered by: Perplexity AI\n"
        "🎨 Images: Pollinations.ai\n"
        "⚙️ Automation: GitHub Actions\n\n"
        "🌐 Open Source:\n"
        "github.com/TriggerZzz/Binance_Greek_Angels_Crypto_News",
        parse_mode='Markdown'
    )

async def privacy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔒 *Privacy Policy*\n\n"
        "✅ No personal data collected\n"
        "✅ No message history stored\n"
        "✅ Only chat ID for delivery\n"
        "✅ Open source & transparent\n\n"
        "Full policy:\n"
        "github.com/TriggerZzz/Binance_Greek_Angels_Crypto_News#privacy",
        parse_mode='Markdown'
    )

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💬 *Feedback & Support*\n\n"
        "We'd love to hear from you!\n\n"
        "🐛 Report issues on GitHub:\n"
        "github.com/TriggerZzz/Binance_Greek_Angels_Crypto_News/issues\n\n"
        "⭐ Like this bot? Star us on GitHub!\n\n"
        "📧 Contact: [Your preferred contact method]",
        parse_mode='Markdown'
    )

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("schedule", schedule))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("privacy", privacy))
    app.add_handler(CommandHandler("feedback", feedback))
    
    print("🤖 Command handler bot running...")
    app.run_polling()

if __name__ == '__main__':
    main()
