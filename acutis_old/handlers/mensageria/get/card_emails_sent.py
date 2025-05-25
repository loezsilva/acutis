from typing import List
from flask_sqlalchemy import SQLAlchemy
from models.mensageria import Mensageria

class CardEmailsSent:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__conn = database

    def execute(self):
        emails_not_sent = self.__query_card_emails_sent()
        emails_delivered = self.__query_card_emails_delivered()
        emails_opened = self.__query_card_emails_opened()
        emails_reported_spam = self.__query_card_emails_reported_spam()
        emails_clicks = self.__query_card_emails_clicks()
        return self.__format_response(emails_not_sent, emails_delivered, emails_opened, emails_reported_spam, emails_clicks)
    
    def __query_card_emails_sent(self) -> int:
        emails = self.__conn.session.query(Mensageria).filter(
            Mensageria.status.in_(["blocked", "deferred", "bounce"])
        ).count()
        return emails
    
    def __query_card_emails_delivered(self) -> int:
        emails = self.__conn.session.query(Mensageria).filter(
            Mensageria.status == "delivered"
        ).count()
        return emails
    
    def __query_card_emails_opened(self) -> int:
        emails = self.__conn.session.query(Mensageria).filter(
            Mensageria.status == "open"
        ).count()
        return emails
    
    def __query_card_emails_reported_spam(self) -> int:
        emails = self.__conn.session.query(Mensageria).filter(
            Mensageria.status.in_(["Unsubscribe", "spamreport", "group_unsubscribe"])
        ).count()
        return emails
    
    def __query_card_emails_clicks(self) -> int:
        emails = self.__conn.session.query(Mensageria).filter(
            Mensageria.status == "click"
        ).count()
        return emails
    
    def __format_response(self, emails_not_sent: int, emails_delivered: int, emails_opened: int, emails_reported_spam: int, emails_clicks: int) -> dict:
        return {
            "total_sents": emails_not_sent,
            "total_delivered": emails_delivered,
            "total_opened": emails_opened,
            "total_reported_spam": emails_reported_spam,
            "total_clicks": emails_clicks
        }
