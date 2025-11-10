# 🤖 Binance Angel Devs Crypto News Telegram Bot

![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-blue?logo=github-actions)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)
![Perplexity](https://img.shields.io/badge/Perplexity-AI-purple)
![License](https://img.shields.io/badge/License-MIT-green)

**Automated daily cryptocurrency market reports delivered straight to your Telegram group with AI-generated images!**

This bot uses Perplexity AI to generate comprehensive crypto market summaries and automatically posts them with beautiful, cinematic images to your Telegram channel or group. Runs completely free on GitHub Actions (except Perplexity API costs).

---

## ✨ Features

- 📊 **Daily Crypto News**: AI-powered summaries of top global crypto market events
- 🎨 **Automatic Image Generation**: Unique AI-generated images for each report
- ⏰ **Scheduled Delivery**: Runs Monday-Friday at 17:00 UTC automatically
- 🔄 **Fully Automated**: Zero manual intervention required
- 💰 **Cost-Effective**: Runs on free GitHub Actions (only Perplexity API charges apply)
- 🎯 **Customizable**: Easy to modify query, schedule, and image style
- 🔒 **Secure**: All credentials stored as encrypted GitHub Secrets

---

## 📸 Example Output

Your Telegram will receive posts like this:

```
🖼️ [AI-Generated Crypto Image]

📊 Daily Report - November 10, 2025

Crypto Market Update: November 10, 2025

- 🚀 Bitcoin hovers near $100,500, recovering after a sharp dip...

- 📉 Major crypto stocks Coinbase (-2.29%) and MicroStrategy...

- 🔄 Innovations emerge as exchanges like BTCC launch...

- 🇺🇸 The recent U.S. government shutdown resolution sparked...

- ⚙️ Bitcoin Summer's Phase II upgrades promise enhanced...

#CryptoNews #MarketOverview

Generated at 17:00 UTC
```

---

## 🚀 Quick Start

### Prerequisites

- GitHub account (free)
- Telegram account
- Perplexity Pro subscription ([Sign up here](https://www.perplexity.ai/pro))

### Setup Time: ~15 minutes

---

## 📋 Step-by-Step Setup

### 1️⃣ Create Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow the prompts
3. Choose a name (e.g., "Crypto Daily News Bot")
4. Choose a username ending with "bot" (e.g., `crypto_daily_bot`)
5. **Save the bot token** BotFather provides

### 2️⃣ Get Your Telegram Chat ID

**For Groups/Channels:**
1. Add your bot to the group/channel
2. Make the bot an **admin**
3. Send a test message in the group
4. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
5. Find the `chat.id` value (negative number for groups)
6. **Save this ID**

**For Private Messages:**
- Chat ID will be a positive number
- Same process as above

### 3️⃣ Get Perplexity API Key

1. Go to [Perplexity API Settings](https://www.perplexity.ai/settings/api)
2. Create a new API Group
3. Generate an API Key
4. **Save the key** (starts with `pplx-`)

### 4️⃣ Fork or Clone This Repository

**Option A: Fork (Recommended)**
1. Click the **Fork** button at the top of this page
2. This creates your own copy

**Option B: Clone**
```bash
git clone https://github.com/yourusername/crypto-telegram-bot.git
cd crypto-telegram-bot
```

### 5️⃣ Configure GitHub Secrets

1. Go to your repository **Settings**
2. Navigate to **Secrets and variables** → **Actions**
3. Click **New repository secret** for each:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Your bot token from BotFather | `123456:ABC-DEF...` |
| `TELEGRAM_CHAT_ID` | Your chat/group ID | `-1001234567890` |
| `PERPLEXITY_API_KEY` | Your Perplexity API key | `pplx-abc123...` |
| `PERPLEXITY_QUERY` | Your custom news query | See below |
| `IMAGE_PROMPT` | Custom image style (optional) | See below |

### 6️⃣ Set Your Query

For `PERPLEXITY_QUERY` secret, use this template:

```
Summarize today's top global news about crypto market. Include major economic events, and highlight any breaking news about future events. Make an article no more than 750 characters (with spaces).

At the end of the article include these two hashtags "#CryptoNews #MarketOverview".

First enter a title with today's date and insert bullet points between paragraphs.
Use emojis and bullet points for each paragraph.

Do NOT mention anything about creating or posting an image. Just provide the news summary.
```

### 7️⃣ (Optional) Customize Image Style

For `IMAGE_PROMPT` secret, choose a style:

**Professional Financial:**
```
cryptocurrency trading floor with bitcoin and ethereum symbols, holographic financial charts, modern trading office, cinematic lighting, HDR, epic composition, hyper-realistic, professional photography, blue and gold theme
```

**Abstract/Futuristic:**
```
abstract cryptocurrency concept art, digital bitcoin network visualization, glowing blockchain connections, futuristic financial technology, cinematic scene, epic HDR composition, dramatic lighting, 8k quality
```

**Dynamic/Energetic:**
```
explosive crypto market action scene, bitcoin breaking through barriers, dynamic financial charts surging upward, electric energy atmosphere, cinematic fx, HDR lighting, epic composition, hyper-realistic photography
```

### 8️⃣ Test Your Bot

1. Go to **Actions** tab in your repository
2. Click on **Send Crypto News to Telegram** workflow
3. Click **Run workflow** → **Run workflow**
4. Wait ~45-60 seconds
5. Check your Telegram for the report with image! 🎉

---

## ⏰ Schedule Configuration

**Default:** Monday-Friday at 17:00 UTC

To change the schedule, edit `.github/workflows/send_perplexity_report.yml`:

```yaml
on:
  schedule:
    - cron: '0 17 * * 1-5'  # Mon-Fri at 17:00 UTC
```

### Common Schedule Examples

| Schedule | Cron Expression |
|----------|----------------|
| Every day at 09:00 UTC | `'0 9 * * *'` |
| Weekdays at 08:00 & 17:00 UTC | `'0 8,17 * * 1-5'` |
| Mon, Wed, Fri at 12:00 UTC | `'0 12 * * 1,3,5'` |
| Every 6 hours, weekdays only | `'0 */6 * * 1-5'` |

Use [crontab.guru](https://crontab.guru/) to create custom schedules.

---

## 📁 Repository Structure

```
crypto-telegram-bot/
├── .github/
│   └── workflows/
│       └── send_perplexity_report.yml    # GitHub Actions workflow
├── bot.py                                 # Main bot script
├── requirements.txt                       # Python dependencies
└── README.md                              # This file
```

---

## 🔧 Customization

### Change Article Length

In your `PERPLEXITY_QUERY`, modify:
```
Make an article no more than 750 characters (with spaces).
```

Change `750` to your desired length (Telegram caption limit: 1024 chars).

### Change Topic Focus

Modify your `PERPLEXITY_QUERY` to cover different topics:

**NFT Focus:**
```
Summarize today's top NFT market news including major sales, new launches, and trending collections...
```

**DeFi Focus:**
```
Summarize today's DeFi protocol updates, major yield changes, and new protocol launches...
```

**Bitcoin Only:**
```
Summarize today's Bitcoin-specific news including price action, network updates, and institutional adoption...
```

### Change Formatting Style

Adjust the query to change output style:
- Remove emojis: Delete "Use emojis" from query
- Change hashtags: Modify the hashtag line
- Adjust structure: Specify "Use numbered list" instead of bullet points

---

## 💰 Cost Breakdown

### Free Components:
- ✅ GitHub Actions: 2,000 minutes/month (free tier)
- ✅ Telegram Bot: Completely free
- ✅ Image Generation (Pollinations.ai): Free
- ✅ Bot Hosting: Free on GitHub

### Paid Components:
- 💵 Perplexity API: ~$0.50-2.00/month
  - Based on 22 reports/month (Mon-Fri)
  - ~1,500 tokens per report
  - Check current pricing at [Perplexity Pricing](https://docs.perplexity.ai/docs/pricing)

**Total Monthly Cost: $0.50-2.00** 🎉

---

## 🐛 Troubleshooting

### Bot doesn't run automatically
- ✅ Verify workflow file is on `main` branch
- ✅ Check repository hasn't been inactive for 60+ days
- ✅ GitHub Actions schedules can delay 3-15 minutes

### "Unauthorized" error from Perplexity
- ✅ Verify API key is correct and active
- ✅ Check key format: `pplx-...`
- ✅ Ensure API key hasn't been revoked

### Telegram message not received
- ✅ Verify bot token is correct
- ✅ Ensure you've sent `/start` to the bot
- ✅ For groups: Bot must be an admin
- ✅ Verify chat ID is correct (negative for groups)

### Image not showing
- ✅ Check GitHub Actions logs for errors
- ✅ Verify image URL is accessible
- ✅ Try manual test workflow run

### Workflow fails
1. Go to **Actions** tab
2. Click on the failed workflow run
3. Click on the job to see detailed logs
4. Check which step failed and review error message

---

## 📊 Monitoring

### View Workflow Runs
1. Go to **Actions** tab
2. See all past runs with status (✅ success / ❌ failed)
3. Click any run to view detailed logs

### Check Perplexity API Usage
1. Visit [Perplexity API Dashboard](https://www.perplexity.ai/settings/api)
2. Monitor your token usage and costs

### Telegram Message History
- All messages remain in your Telegram group
- Review past reports anytime

---

## 🔒 Security Best Practices

1. ✅ **Never commit secrets** to repository
2. ✅ **Use GitHub Secrets** for all sensitive data
3. ✅ **Make repository private** if containing sensitive logic
4. ✅ **Rotate API keys** every 90 days
5. ✅ **Monitor GitHub Actions logs** for unusual activity
6. ✅ **Revoke compromised keys immediately**

---

## 🚀 Advanced Features (Future Enhancements)

Want to add more features? Here are some ideas:

- 📈 **Price Alerts**: Monitor specific price thresholds
- 📊 **Custom Charts**: Generate price charts with data
- 🔔 **Breaking News Alerts**: Real-time notifications for major events
- 📧 **Email Delivery**: Also send reports via email
- 🌐 **Multi-Language**: Support multiple languages
- 💬 **Interactive Bot**: Respond to Telegram commands
- 📱 **Multiple Channels**: Post to different channels with different content
- 🤖 **Sentiment Analysis**: Include market sentiment scores

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Perplexity AI** - For the amazing AI search API
- **GitHub Actions** - For free workflow automation
- **Telegram** - For the bot platform
- **Pollinations.ai** - For free AI image generation

---

## 📞 Support

Having issues? Here's how to get help:

1. **Check the Troubleshooting section** above
2. **Review GitHub Actions logs** for error details
3. **Open an Issue** on this repository
4. **Check Perplexity API docs**: https://docs.perplexity.ai

---

## 📈 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/crypto-telegram-bot?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/crypto-telegram-bot?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/crypto-telegram-bot)

---

## 🎯 Roadmap

- [x] Basic crypto news automation
- [x] Image generation integration
- [x] Customizable scheduling
- [ ] Price alert notifications
- [ ] Multi-channel support
- [ ] Interactive command handling
- [ ] Sentiment analysis integration
- [ ] Custom chart generation

---

<div align="center">

**Made with ❤️ and powered by Binance Angel Devs**

⭐ Star this repo if you find it useful!

[Report Bug](https://github.com/yourusername/crypto-telegram-bot/issues) · [Request Feature](https://github.com/yourusername/crypto-telegram-bot/issues)

</div>
