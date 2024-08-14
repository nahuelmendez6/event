"""
Comunication: Message, Notification, UserNotification
"""

from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app.auth.models import Users


class Message(db.Model):
    """
       Represents a message sent between users.

       Attributes:
           id_message (int): The unique identifier for the message.
           id_sender (int): The identifier of the user who sent the message.
           id_receiver (int): The identifier of the user who received the message.
           id_event (int): The identifier of the event related to the message.
           message_content (str): The content of the message.
           sent_at (datetime): The timestamp when the message was sent.

       Relationships:
           sender (Users): The user who sent the message.
           receiver (Users): The user who received the message.
           event (Event): The event associated with the message.
       """

    __tablename__ = 'messages'

    id_message = db.Column(db.Integer, primary_key=True, nullable=False)
    id_sender = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=True)
    id_receiver = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=True)
    id_event = db.Column(db.Integer, db.ForeignKey('events.id_event'), nullable=False)
    message_content = db.Column(db.Text, nullable=True)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    sender = db.relationship('Users', foreign_keys=[id_sender] ,backref='sent_message', lazy=True)
    receiver = db.relationship('Users', foreign_keys=[id_receiver] ,backref='received_message', lazy=True)
    event = db.relationship('Events', backref='event', lazy=True)


class Notification(db.Model):

    """
    Represents a notification in the system.

    Attributes:
        id_notification (int): The unique identifier for the notification.
        notification_text (str): The text of the notification.
        created_at (datetime): The timestamp when the notification was created.

    Relationships:
        user_notifications (UserNotification): The notifications associated with users.
    """

    __tablename__ = 'notifications'

    id_notification = db.Column(db.Integer, primary_key=True, nullable=False)
    notification_text = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user_notifications = db.relationship('UserNotification', backref='notificacion', lazy=True)

class UserNotification(db.Model):
    """
       Represents the association between a user and a notification.

       Attributes:
           id_user_notification (int): The unique identifier for the user notification record.
           id_user (int): The identifier of the user who received the notification.
           id_notification (int): The identifier of the notification.
           seen (bool): Indicates whether the notification has been seen by the user.

       Relationships:
           user (Users): The user who received the notification.
           notification (Notification): The notification associated with the user.
       """


    __tablename__ = 'user_notification'

    id_user_notification = db.Column(db.Integer, primary_key=True, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=True)
    id_notification = db.Column(db.Integer, db.ForeignKey('notifications.id_notification'), nullable=True)
    seen = db.Column(db.Tinyint, default=0 ,nullable=True)

    # Relationships
    user = db.relationship('Users', backref='user_notifications', lazy=True)
    notification = db.relationship('Notification', backref='user_notification', lazy=True)