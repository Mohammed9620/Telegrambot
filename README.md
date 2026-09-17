# Telegram Job Bot

A Telethon-based bot that listens to a set of Telegram job groups, uses the
Gemini API to detect whether a posting is a genuine tech job, and forwards
matching messages to your own Saved Messages.

## How it works

1. `main.py` connects to your Telegram account (via Telethon) and listens
   only to the groups listed in `groups.json`.
2. Every new message from those groups is sent to `classifier.py`, which
   asks Gemini a yes/no question: is this a real tech job?
3. If yes, the message is forwarded as-is to your Saved Messages chat.
4. If no, it's silently ignored.

Runs in real time (event-driven, not polling) and is meant to stay online
24/7 on a server.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in:
   - `API_ID` / `API_HASH` — from [my.telegram.org](https://my.telegram.org)
     (API development tools)
   - `GEMINI_API_KEY` — from [Google AI Studio](https://aistudio.google.com)
3. (Optional) Find the numeric IDs of groups you're in:
   ```
   python list_groups.py
   ```
   Copy the IDs you want into `groups.json`.
4. Run it:
   ```
   python main.py
   ```
   First run asks for your phone number and the login code sent to your
   Telegram app. After that, a local session file keeps you logged in.

## Files

| File | Purpose |
|---|---|
| `main.py` | Telethon client + message handler |
| `classifier.py` | Gemini-based yes/no tech-job classifier |
| `groups.json` | List of group IDs to monitor |
| `list_groups.py` | Helper to list all your groups with their IDs |
| `jobbot.service` | systemd unit for running the bot as a background service on a Linux server |
| `requirements.txt` | Python dependencies |

## Deployment

Meant to run continuously on a small server (e.g. an Oracle Cloud Always
Free VM) via `jobbot.service`, so it doesn't depend on your own machine
being on.

## Notes

- `.env` and `*.session` files are gitignored — they contain your
  credentials and must never be committed or shared.
- The classifier prompt in `classifier.py` can be tuned to be stricter or
  looser about what counts as a "tech job."
