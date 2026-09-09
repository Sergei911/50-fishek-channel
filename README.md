# 50-fishek-channel

Автоматизация публикаций в Telegram-канал [@salon_psychology](https://t.me/salon_psychology).

## Как работает

1. Посты добавляются в `scheduled_posts.json`.
2. GitHub Actions каждый час проверяет время публикации.
3. Бот отправляет готовые посты в канал.
4. Статус сохраняется в `state.json`.

## Формат поста

```json
{
  "id": "2026-09-15-post-01",
  "publish_at": "2026-09-15T09:00:00Z",
  "text": "Текст поста (HTML поддерживается)"
}
```

## Секреты

Settings → Secrets and variables → Actions:
- `TELEGRAM_BOT_TOKEN` — токен от @BotFather
- `TELEGRAM_CHANNEL_ID` — @username канала

## Запуск

Actions → Publish scheduled posts → Run workflow вручную.
