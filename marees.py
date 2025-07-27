import os
import requests
from email.message import EmailMessage
from dotenv import load_dotenv
import smtplib
import datetime
import locale

# Charger les variables d'environnement depuis le .env
load_dotenv()

# 6. Charger les variables sensibles
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
TOKEN = os.getenv("TOKEN")

if not all([EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_RECEIVER]):
    raise ValueError("Une ou plusieurs variables d'environnement sont manquantes.")

url = "https://api.marea.ooo/v1/tides?latitude=46.49440932953166&longitude=-1.785200331355088&days=1"
headers = {
    "x-marea-api-token": TOKEN
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    marees = data["extremes"]
    maree_list = []
else:
    print("Erreur lors de l'appel API :", response.status_code)

for maree in marees:
    maree_timestamp = maree['timestamp']
    hour = datetime.datetime.fromtimestamp(maree_timestamp)
    seaState = maree['state']

    if seaState == "LOW TIDE":
        seaState = "MAREE BASSE"
    elif seaState == "HIGH TIDE":
        seaState = "MAREE HAUTE"
    else:
        print("erreur : il n'y a pas d'info sur la direction de la marée")

    maree_list.append((seaState, hour.strftime("%H:%M")))

locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
date = datetime.datetime.now()
mois = date.strftime("%B").capitalize()
subject = f"Marées du {date.day} {mois} {date.year} aux Sables-d'Olonne 🌊"

lignes = [f"{etat} à {heure}" for etat, heure in maree_list]
content = "\n".join(lignes)

# 7. Préparer et envoyer l'e-mail
msg = EmailMessage()
msg.set_content(content)
msg["Subject"] = subject
msg["From"] = f"Maree Bot 🌊 <{EMAIL_ADDRESS}>"
msg["To"] = EMAIL_RECEIVER

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)