"""
Authentication models: Users, RolePermissions, UserProfile,
Session, AuditLog
"""

from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class Users(UserMixin, db.Model):
    """
    Represents a user in the system.

    Attributes:
        id_user (int): The unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password_hash (str): The hashed password of the user.
        google_id (str): The Google ID of the user (for OAuth).
        registered_via (str): Indicates how the user registered (e.g., 'local', 'google').
        role (str): The role of the user (e.g., 'attendee').
        created_at (datetime): The timestamp when the user was created.

    Relationships:
        role_permissions (RolePermissions): The user's role permissions.
        profile (UserProfile): The user's profile information.
        sessions (Session): The user's active sessions.
        audit_logs (AuditLog): The logs related to the user's activities.
    """

    __tablename__ = 'users'

    id_user = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    google_id = db.Column(db.String(50), nullable=True)
    registered_via = db.Column(db.String(50), default='local', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship with RolePermissions
    #role_permissions = db.relationship('RolePermissions', backref='users', lazy=True)

    # Relationship with UserProfile
    profile = db.relationship('UserProfile', backref='users', uselist=False)

    # Relationship with Sessions
   # sessions = db.relationship('Session', backref='users', lazy=True)

    # Relationship with AuditLog
   # audit_logs = db.relationship('AuditLog', backref='users', lazy=True)

    def set_password(self, password):
        """
        Set the user's password by hashing it.
        :param password:
            password (str): The password to be hashed and set
        :return:
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Chek if the provided password matches the hashed password
        :param password:
            password (str): The password to check
        :return:
            bool: True if the password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)

    def reset_password(self, current_password, new_password):
        """
        Reset the user's password if the current password is correct.

        Args:
            current_password (str): The current password.
            new_password (str): The new password to set.

        Returns:
            bool: True if the password was successfully reset.

        Raises:
            ValueError: If the current password is incorrect.
        """
        if not self.check_password(self, current_password):
            raise ValueError('La contraseña actual es incorrecta')

        self.set_password(new_password)

        return True

    @classmethod
    def find_by_email(cls, email):
        """
                Find a user by their email address.

                Args:
                    email (str): The email address of the user.

                Returns:
                    Users: The user with the specified email, or None if not found.
                """
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_username(cls, username):
        """
                Find a user by their username.

                Args:
                    username (str): The username of the user.

                Returns:
                    Users: The user with the specified username, or None if not found.
                """
        return cls.query.filter_by(username=username).first()

    def __repr__(self):
        """
                Return a string representation of the user.

                Returns:
                    str: A string representation of the user, showing the username.
                """
        return f'<User {self.username}>'

class UserProfile(db.Model):
    """
        Represents a user's profile information.

        Attributes:
            id_user_profile (int): The unique identifier for the user profile.
            id_user (int): The identifier of the user.
            profile_picture_url (str): The URL of the user's profile picture.
            bio (str): A short biography of the user.
            website_url (str): The URL of the user's personal website.
            social_media_links (str): Links to the user's social media profiles.
            created_at (datetime): The timestamp when the profile was created.
            updated_at (datetime): The timestamp when the profile was last updated.

        Relationships:
            user (Users): The user associated with this profile.
        """


    __tablename__ = 'user_profiles'

    id_user_profile = db.Column(db.Integer, primary_key=True, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    profile_picture_url = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    website_url = db.Column(db.String(255), nullable=True)
    social_media_links = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)