<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# 🤖 Crypto News Telegram Bot

**Fully automated bot that delivers daily crypto market news with AI-generated images to your Telegram group. Powered by Perplexity AI and GitHub Actions.**

***

## ✨ Features

- **AI-powered Crypto News:** Get concise, pro-level summaries of global crypto events and key economic news.
- **AI-Generated Images:** Every post includes an AI-generated, cinematic image themed by your own prompt.
- **Runs on Schedule:** Sends news Monday-Friday at your chosen UTC time (default: 17:00 UTC).
- **Zero Hosting Required:** Runs free on GitHub Actions.
- **Secure:** All secrets managed in GitHub Actions; no credentials in your code.
- **Customizable:** Edit the query and image prompt via GitHub Secrets – no code changes required!

***

## 🚀 Quick Start

### Prerequisites

- [ ] GitHub account
- [ ] Telegram account
- [ ] Perplexity PRO subscription ([Get Perplexity PRO](https://www.perplexity.ai/pro))

***

### ⚡️ Step-by-Step Setup

#### 1. **Create Your Telegram Bot**

- In Telegram, search for `@BotFather`
- Send `/newbot` and follow instructions
- Copy your bot token (format: `12345678:ABC...`)


#### 2. **Get Your Chat ID**

- Add your bot to your group/channel and make it an admin
- Send a text message in the group/channel
- Open: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
- Find and note your `chat.id` (starts with `-100...` for groups)


#### 3. **Get Your Perplexity API Key**

- Go to [Perplexity API Settings](https://www.perplexity.ai/settings/api)
- Create an API group and generate a key (format: `pplx-...`)
- Copy and save it – you’ll use this in GitHub Secrets


#### 4. **Fork or Clone This Repository**

- Fork this repo, or
- Clone to your machine:
`git clone https://github.com/yourusername/crypto-telegram-bot.git`


#### 5. **Set Up GitHub Secrets**

Go to: **GitHub repo → Settings → Secrets and variables → Actions**

Add each as a “New repository secret”:


| Secret Name | Value | Example Value/Notes |
| :-- | :-- | :-- |
| `TELEGRAM_BOT_TOKEN` | Bot token | From BotFather, like `12345678:AA...` |
| `TELEGRAM_CHAT_ID` | Chat ID | E.g., `-1001234567890` |
| `PERPLEXITY_API_KEY` | API key | From Perplexity, like `pplx-xxx...` |
| `PERPLEXITY_QUERY` | News query | See below for example |
| `IMAGE_PROMPT` | Image style | See below for example |


***

## 🔑 Example Secrets

### `PERPLEXITY_QUERY` (example)

```
Summarize today's top global news about crypto market. Include major economic events and highlight any breaking news about future events. Make an article no more than 750 characters (with spaces).
At the end of the article include these two hashtags "#CryptoNews #MarketOverview".
First enter a title with today's date and insert bullet points between paragraphs.
Use emojis and bullet points for each paragraph.
Do NOT mention anything about creating or posting an image. Just provide the news summary.
```


### `IMAGE_PROMPT` (example)

```
cinematic scene, fx, HDR, epic composition, cinematic photo, hyper-realistic, hyper-detailed, cinematic lighting, cryptocurrency trading floor, bitcoin ethereum symbols, financial charts, modern digital finance
```


***

## 🛠️ Customizing the Bot

- **Change time of daily post:**
Edit `.github/workflows/send_perplexity_report.yml` cron line
(default: `'0 17 * * 1-5'` for 17:00 UTC Mon-Fri)
- **Change news or image style:**
Update the secrets `PERPLEXITY_QUERY` and/or `IMAGE_PROMPT` any time.
- **Use for other news/tokens:**
Change your prompt to focus on NFTs, DeFi, a specific token, or anything else.

***

## 💡 How It Works

- At the scheduled time, GitHub Actions runs `bot.py`:

1. Uses Perplexity API to generate crypto market news from your query.
2. Generates an AI image using your prompt via Pollinations.
3. Posts both (as a photo with the headline in the caption) to your Telegram group/channel.

***

## 🏁 Manual Test

To try it any time:

- Go to your GitHub repo → **Actions**
- Select workflow → **Run workflow**
- Wait ~1 minute
- Check Telegram!

***

## 🐛 Troubleshooting

- **No news/image?**
Check workflow logs for missing or misconfigured secrets.
- **Bot doesn’t send?**
Ensure it’s an admin in the group/channel, and that all secrets are correct.
- **Message too long?**
The bot will auto-truncate captions past 1,020 characters.
- **API error?**
Bot sends you an error message in Telegram if possible.

***

## 🔐 Security Tips

- Do NOT commit secrets in code or files; **only use GitHub Secrets**.
- Rotate Perplexity API keys and Telegram bot tokens periodically.
- Make your repo public only after checking secrets aren’t in code or logs.

***

## 📝 File Overview

```
.
├── .github/
│   └── workflows/
│       └── send_perplexity_report.yml
├── bot.py                # Main script, secrets loaded from env
├── requirements.txt      # Python dependencies (requests)
└── README.md             # This file
```


***

## 📈 Cost

- GitHub Actions: Free tier (up to 2,000 minutes/month)
- Telegram Bot: Free
- Image Generation (Pollinations): Free
- Perplexity API: ~\$0.50–2/month (22 reports @ 750–1500 tokens each)

***

## 🛣️ Roadmap

- [x] Basic crypto news automation
- [x] AI-generated image support
- [x] Secrets-only config, no inline credentials
- [ ] Price alert add-on
- [ ] Custom chart support
- [ ] Interactive Telegram command mode
- [ ] Multi-language reports

***

## 🤝 Contributing

PRs are very welcome! Please open issues/requests for bugs or improvements.

***

## 🙏 Acknowledgments

- [Perplexity AI](https://perplexity.ai) – For the AI news engine
- [Pollinations AI](https://pollinations.ai) – Free AI image generation
- [GitHub Actions](https://github.com/features/actions) – No-cost automation
- [Telegram](https://core.telegram.org/bots) – Messaging platform

***

## 📮 Questions? Get Help!

- Open a GitHub Issue on this repo if you get stuck.
- Check Perplexity API docs: https://docs.perplexity.ai
- Review workflow/action logs for errors.

***

**Made with ❤️ and powered by AI**
Star this repo if you find it useful!

