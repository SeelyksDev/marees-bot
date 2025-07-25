import os
import requests
from email.message import EmailMessage
from dotenv import load_dotenv
import smtplib
import json

# Charger les variables d'environnement depuis le .env
load_dotenv()

with open('marees.json', 'r') as f:
    data = json.load(f)

print("Lieu :", data["location"]["name"])
print("Date :", data["date"])
print("Horaires de marées :")


# 6. Charger les variables sensibles
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
TOKEN = os.getenv("TOKEN")

if not all([EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_RECEIVER]):
    raise ValueError("Une ou plusieurs variables d'environnement sont manquantes.")

# # 7. Préparer et envoyer l'e-mail
# msg = EmailMessage()
# msg.set_content(texte)
# msg["Subject"] = subject
# msg["From"] = f"Maree Bot 🌊 <{EMAIL_ADDRESS}>"
# msg["To"] = EMAIL_RECEIVER

# with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    # smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    # smtp.send_message(msg)