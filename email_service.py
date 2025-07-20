import os
import smtplib
import logging
from email.message import EmailMessage
from news_service import NewsService

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.email_user = os.getenv("EMAIL_USER")
        self.email_pass = os.getenv("EMAIL_PASS")
        self.email_to = os.getenv("EMAIL_TO")
        self.news_service = NewsService()
        
    def validate_config(self):
        """Validate email configuration"""
        if not self.email_user:
            raise Exception("EMAIL_USER not configured")
        if not self.email_pass:
            raise Exception("EMAIL_PASS not configured")
        if not self.email_to:
            raise Exception("EMAIL_TO not configured")
    
    def send_news_email(self, articles, subject_prefix=""):
        """Send news email with articles"""
        self.validate_config()
        
        # Format email content
        news_content = self.news_service.format_articles_for_email(articles)
        
        # Prepare recipients
        recipients = [email.strip() for email in self.email_to.split(",")]
        
        # Create email message
        msg = EmailMessage()
        subject = "🎮 Daily XR Technology News - Multiple Sources (48 Hours)"
        if subject_prefix:
            subject = f"{subject_prefix} - {subject}"
        
        msg['Subject'] = subject
        msg['From'] = self.email_user
        msg['To'] = ", ".join(recipients)
        msg.set_content(news_content)
        
        try:
            logger.info(f"Sending email to {len(recipients)} recipients")
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.email_user, self.email_pass)
                server.send_message(msg)
            logger.info("Email sent successfully")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP authentication failed: {e}")
            raise Exception("Email authentication failed. Please check your email credentials.")
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {e}")
            raise Exception(f"Email sending failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error sending email: {e}")
            raise Exception(f"Email sending failed: {str(e)}")
    
    def test_email_connection(self):
        """Test email server connection"""
        self.validate_config()
        
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.email_user, self.email_pass)
            return True
        except Exception as e:
            logger.error(f"Email connection test failed: {e}")
            raise
