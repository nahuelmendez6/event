"""
Comments: Comment, Feedback
"""
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class Comment(db.Model):
    """
        Represents a comment made by a user on an event.

        Attributes:
            id_comment (int): The unique identifier for the comment.
            content (str): The text content of the comment.
            rating (int): An optional rating associated with the comment.
            created_at (datetime): The timestamp when the comment was created.
            id_user (int): The identifier of the user who made the comment.
            id_event (int): The identifier of the event associated with the comment.

        Relationships:
            user (Users): The user who made the comment.
            event (Event): The event associated with the comment.
        """

    __tablename__ = 'comments'

    id_comment = db.Column(db.Integer, primary_key=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=True)
    id_event = db.Column(db.Integer, db.ForeignKey('events.id_event'), nullable=True)

    # Relationships
    user = db.relationship('Users', backref='comments', lazy=True)
    event = db.relationship('Event', backref='comments', lazy=True)


class FeedBack(db.Model):
    """
        Represents feedback provided by a user on an event.

        Attributes:
            id_feedback (int): The unique identifier for the feedback.
            feedback_text (str): The text content of the feedback.
            id_user (int): The identifier of the user who provided the feedback.
            id_event (int): The identifier of the event associated with the feedback.
            created_at (datetime): The timestamp when the feedback was created.

        Relationships:
            user (Users): The user who provided the feedback.
            event (Event): The event associated with the feedback.
        """

    __tablename__ = 'feedback'

    id_feedback = db.Column(db.Integer, primary_key=True, nullable=False)
    feedback_text = db.Column(db.Text, nullable=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=True)
    id_event = db.Column(db.Integer, db.ForeignKey('events.id_event'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('Users', backref='feedbacks', lazy=True)
    event = db.relationship('Event', backref='feedbacks', lazy=True)