from builder import db


class SendEmailsInactives(db.Model):
    __tablename__ = "send_emails_inactives"

    id = db.Column(db.Integer, primary_key=True)
    email_send = db.Column(db.String(), nullable=False)
    send_date = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "email_send": self.email_send,
            "send_date": self.send_date,
        }

    def __repr__(self) -> str:
        return f"<id: {self.id}, send_email;{self.email_send}, send_date: {self.send_date}"
