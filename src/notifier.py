import smtplib
from email.message import EmailMessage
from src.config import Config

class EmailNotifier:
    def send_bulk_alert(self, deals):
        if not deals:
            return

        msg = EmailMessage()
        msg['Subject'] = f"Uçuş Fırsatları Bülteni ({len(deals)} Yeni Düşüş)"
        msg['From'] = Config.EMAIL_ADDRESS
        msg['To'] = Config.EMAIL_ADDRESS

        body = "Aşağıdaki uçuşlarda fiyat düşüşü saptandı:\n\n"
        for deal in deals:
            old_p = deal['old'] if deal['old'] else "İlk Kayıt"
            body += f"{deal['origin']} -> AMS\n"
            body += f"Tarih: {deal['date']}\n"
            body += f"Yeni Fiyat: {deal['new']} TRY (Eski: {old_p} TRY)\n"
            body += "-" * 30 + "\n"

        body += "\nBu bülten flight-tracking sistemi tarafından otomatik oluşturulmuştur."
        msg.set_content(body)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(Config.EMAIL_ADDRESS, Config.EMAIL_PASSWORD)
                smtp.send_message(msg)
            print(f"Özet mail {len(deals)} fırsat ile gönderildi.")
        except Exception as e:
            print(f"Mail hatası: {e}")