#!/usr/bin/env python3
"""Публикация запланированных постов в Telegram-канал."""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
import urllib.request
import urllib.error

BASE_DIR = Path(__file__).parent
POSTS_FILE = BASE_DIR / "scheduled_posts.json"
STATE_FILE = BASE_DIR / "state.json"
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID")

def load_json(path, default):
    if not path.exists():
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def send_telegram_message(text):
    if not BOT_TOKEN or not CHANNEL_ID:
        raise RuntimeError("Не заданы TELEGRAM_BOT_TOKEN / TELEGRAM_CHANNEL_ID")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "HTML"}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if not result.get("ok"):
                raise RuntimeError(f"Telegram API: {result}")
            return result
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        raise RuntimeError(f"HTTP {e.code}: {body}") from e

def main():
    posts = load_json(POSTS_FILE, [])
    state = load_json(STATE_FILE, {"published_ids": []})
    published_ids = set(state.get("published_ids", []))
    now = datetime.now(timezone.utc)
    for post in posts:
        post_id = post.get("id")
        publish_at_str = post.get("publish_at")
        text = post.get("text", "")
        if not post_id or not publish_at_str or not text or post_id in published_ids:
            continue
        try:
            publish_at = datetime.fromisoformat(publish_at_str.replace("Z", "+00:00"))
        except ValueError:
            continue
        if publish_at <= now:
            send_telegram_message(text)
            published_ids.add(post_id)
    state["published_ids"] = sorted(published_ids)
    save_json(STATE_FILE, state)

if __name__ == "__main__":
    main()
