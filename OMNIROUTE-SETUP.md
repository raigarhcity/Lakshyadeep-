# OmniRoute setup (run on your own computer)

OmniRoute is a local AI gateway. Your coding tools send requests to it, and it routes them to
free or cheap providers, falls back when one fails, and compresses prompts (RTK + Caveman) to save tokens.

## 1. Install Node.js

You need Node.js **24** (or 22.22.2+). Download it from https://nodejs.org (pick "LTS").
Check it with: `node -v`

## 2. Install and start OmniRoute

```bash
npm install -g omniroute
omniroute
```

- Dashboard: http://localhost:20128
- API: http://localhost:20128/v1

Keep this terminal open while you use it. Your settings are saved in your home folder,
so they're still there the next time you run `omniroute`.

To check for problems: `omniroute doctor`

## 3. Connect providers (dashboard → Providers)

- **OpenCode Free**: no signup.
- **Kiro AI**: free Claude, about 50 credits/month.
- Optional: add free API keys (Groq, Gemini, OpenRouter, etc.) for more reliable fallbacks.

Copy your API key from **Dashboard → Endpoints**.

## 4. Use it with Claude Code

Easiest:

```bash
omniroute launch
```

Or set it up by hand (Mac/Linux):

```bash
export ANTHROPIC_BASE_URL=http://localhost:20128      # no /v1 at the end
export ANTHROPIC_AUTH_TOKEN=YOUR_OMNIROUTE_KEY
export ANTHROPIC_MODEL=auto
claude
```

On Windows PowerShell:

```powershell
$env:ANTHROPIC_BASE_URL="http://localhost:20128"
$env:ANTHROPIC_AUTH_TOKEN="YOUR_OMNIROUTE_KEY"
$env:ANTHROPIC_MODEL="auto"
claude
```

For Cursor, Cline and other OpenAI-compatible tools, use:
base URL `http://localhost:20128/v1`, your key, and model `auto`.

## 5. Check that it works

```bash
curl http://localhost:20128/v1/models -H "Authorization: Bearer YOUR_OMNIROUTE_KEY"
```

## Other ways to run it

- **Docker (runs in the background, restarts on its own):**
  ```bash
  docker run -d --name omniroute --restart unless-stopped \
    -e OMNIROUTE_MEMORY_MB=8192 --memory=10g \
    -p 127.0.0.1:20128:20128 -v omniroute-data:/app/data diegosouzapw/omniroute:latest
  ```
- **Android phone (Termux):** `pkg install nodejs && npx -y omniroute`

## Notes

- Free models are weaker and less reliable than real Claude. Use them for simple tasks, and
  keep hard tasks on a strong model.
- OmniRoute itself flags some free providers for possible terms-of-service problems. Check a
  provider's terms before you rely on it.
- Docs: https://github.com/diegosouzapw/OmniRoute
