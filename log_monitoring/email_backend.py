# log_monitoring/email_backend.py
import ssl
import smtplib
from django.core.mail.backends.smtp import EmailBackend

class DevSMTPEmailBackend(EmailBackend):
    def open(self):
        if self.connection:
            return False

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE   # 🔥 THIS FIXES IT

        self.connection = smtplib.SMTP(self.host, self.port, timeout=self.timeout)
        self.connection.ehlo()
        self.connection.starttls(context=context)
        self.connection.ehlo()
        self.connection.login(self.username, self.password)
        return True