import smtplib
from email.message import EmailMessage
from src.config import Config
from collections import defaultdict

class EmailNotifier:
    def send_bulk_alert(self, deals):
        if not deals:
            return

        grouped_deals = defaultdict(list)
        for deal in deals:
            grouped_deals[deal['date']].append(deal)

        msg = EmailMessage()
        msg['Subject'] = f"Uçuş Bülteni: {len(deals)} Fırsat Yakalandı!"
        msg['From'] = Config.EMAIL_ADDRESS
        msg['To'] = Config.EMAIL_ADDRESS

        body = "Amsterdam (AMS) rotasında fiyat düşüşleri tespit edildi!\n\n"
        
        sorted_dates = sorted(grouped_deals.keys())
        
        for date in sorted_dates:
            body += f"TARİH: {date}\n"
            body += "=" * 35 + "\n"
            
            for deal in grouped_deals[date]:
                old_p = f"{deal['old']} TRY" if deal['old'] else "İlk Kayıt"
                body += f"{deal['origin']} -> AMS\n"
                body += f"Yeni Fiyat: {deal['new']} TRY\n"
                body += f"Önceki: {old_p}\n"
                body += "-" * 20 + "\n"
            
            body += "\n"

        body += "\nBu bülten Amsterdam uçuş planın için otomatik olarak oluşturulmuştur."
        msg.set_content(body)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(Config.EMAIL_ADDRESS, Config.EMAIL_PASSWORD)
                smtp.send_message(msg)
            print(f"Özet mail {len(deals)} fırsat ile tarihlere göre gruplanarak gönderildi.")
        except Exception as e:
            print(f"Mail hatası: {e}")