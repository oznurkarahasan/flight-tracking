import smtplib
from email.message import EmailMessage
from src.config import Config

class EmailNotifier:
    def send_alert(self, origin, dest, date, new_price, old_price):
        msg = EmailMessage()
        subject = f"Fiyat Düştü! {origin} -> {dest}"
        body = (f"Uçuş Tarihi: {date}\n"
                f"Yeni Fiyat: {new_price} TRY\n"
                f"Eski Fiyat: {old_price if old_price else 'Bilinmiyor'} TRY\n"
                f"Acele etsen iyi olur!")
        
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = Config.EMAIL_ADDRESS
        msg['To'] = Config.EMAIL_ADDRESS

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(Config.EMAIL_ADDRESS, Config.EMAIL_PASSWORD)
                smtp.send_message(msg)
            print(f"Mail başarıyla gönderildi: {origin} -> {dest}")
        except Exception as e:
            print(f"Mail gönderme hatası: {e}")