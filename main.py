import requests
import time
from discord_webhook import DiscordWebhook

# Mock Twitch–Discord Integration
# The idea: notify a Discord channel instantly when a Twitch streamer goes live

TWITCH_CLIENT_ID = "your_twitch_client_id"
TWITCH_ACCESS_TOKEN = "your_twitch_access_token"
STREAMER_USER_ID = "12345678"  # Replace with actual Twitch user ID
DISCORD_WEBHOOK_URL = "your_discord_webhook_url"

def get_stream_status():
    """Check if a Twitch streamer is live."""
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {TWITCH_ACCESS_TOKEN}"
    }
    url = f"https://api.twitch.tv/helix/streams?user_id={STREAMER_USER_ID}"
    response = requests.get(url, headers=headers)
    data = response.json().get("data", [])
    return bool(data)  # True if live, False otherwise

def notify_discord(stream_title):
    """Send a notification to Discord."""
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=f"🎮 {stream_title} is now live on Twitch!")
    webhook.execute()

def monitor_stream(interval=15):
    """Continuously check stream status with low-latency polling."""
    was_live = False
    while True:
        try:
            is_live = get_stream_status()
            if is_live and not was_live:
                notify_discord("StreamerName")  # Replace with dynamic name if desired
                print("Notification sent: Streamer is live!")
            was_live = is_live
            time.sleep(interval)
        except Exception as e:
            print(f"[Error] {e}")
            time.sleep(interval)

if __name__ == "__main__":
    print("Starting Twitch–Discord integration monitor...")
    monitor_stream()

