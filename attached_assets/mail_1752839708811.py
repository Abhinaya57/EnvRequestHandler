import requests
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

# Config
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")

def fetch_niche_tech_news():
    keywords = "XR OR AR OR VR OR metaverse OR gaming OR '3D artist' OR Unreal OR Unity OR Blender"
    url = f"https://newsapi.org/v2/everything?q={keywords}&language=en&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"
    
    response = requests.get(url)
    if response.status_code != 200:
        return f"⚠️ Failed to fetch news: {response.status_code}"

    articles = response.json().get("articles", [])

    if not articles:
        return "🛑 No niche tech news found today."

    news_content = "🧠 *Today's XR / Gaming / 3D Artist News*\n\n"
    for i, article in enumerate(articles, 1):
        title = article.get("title", "No Title")
        url = article.get("url", "")
        news_content += f"{i}. {title}\n{url}\n\n"

    return news_content

def send_email(news_body):
    recipients = EMAIL_TO.split(",")

    msg = EmailMessage()
    msg['Subject'] = "🎮 XR, Gaming & 3D Artist News - Daily Update"
    msg['From'] = EMAIL_USER
    msg['To'] = ", ".join(recipients)
    msg.set_content(news_body)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def job():
    news = fetch_niche_tech_news()
    send_email(news)

job()  # Call once when scheduled
