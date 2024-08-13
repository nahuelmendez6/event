"""
Event managment: Event, Category, EventPhoto, EventSponsor, Tag,
EventTag, AttendeeEvent, Subscription
"""
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app.auth.models import Users


class Event(db.Model):
    """
        Represents an event in the system.

        Attributes:
            id_event (int): The unique identifier for the event.
            event_title (str): The title of the event.
            description (str): A description of the event.
            start_date (datetime): The start date and time of the event.
            finish_date (datetime): The end date and time of the event.
            id_category (int): The identifier of the category the event belongs to.
            id_organizer (int): The identifier of the user who organized the event.
            latitude (float): The latitude of the event location.
            longitude (float): The longitude of the event location.
            location_name (str): The name of the event location.
            adress (str): The address of the event location.
            created_at (datetime): The timestamp when the event was created.
            updated_at (datetime): The timestamp when the event was last updated.

        Relationships:
            category (Categories): The category of the event.
            organizer (Users): The user who organized the event.
            photos (EventPhoto): The photos associated with the event.
            sponsors (EventSponsor): The sponsors of the event.
            tags (EventTag): The tags associated with the event.
            attendees (AttendeeEvent): The attendees of the event.
        """
    __tablename__ = 'events'

    id_event = db.Column(db.Integer, primary_key=True, nullable=False)
    event_title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    finish_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    id_category = db.Column(db.Integer, db.ForeignKey('categories.id_category'), nullable=False)
    id_organizer = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    location_name = db.Column(db.String(255), nullable=True)
    adress = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    # Relationships
    category = db.relationship('Categories', backref='events', lazy=True)
    organizer = db.relationship('Users', backref='organized_events', lazy=True)
    photos = db.relationship('EventPhoto', backref='event', lazy=True)
    sponsors = db.relationship('EventSponsor', backref='event', lazy=True)
    tags = db.relationship('EventTag', backref='event', lazy=True)
    attendees = db.relationship('AttendeeEvent', backref='event', lazy=True)


class Categories(db.Model):
    """
        Represents a category for events.

        Attributes:
            id_category (int): The unique identifier for the category.
            category_name (str): The name of the category.

        Relationships:
            subscriptions (Subscription): The subscriptions associated with the category.
        """

    __tablename__ = 'categories'

    id_category = db.Column(db.Integer, primary_key=True, nullable=False)
    category_name = db.Column(db.String(100), nullable=False)

    # Relationships
    subscriptions = db.relationship('Subscription', backref='category', lazy=True)

class EventPhoto(db.Model):
    """
        Represents a photo associated with an event.

        Attributes:
            id_event_photo (int): The unique identifier for the event photo.
            id_event (int): The identifier of the event the photo is associated with.
            photo_url (str): The URL of the photo.
            uploaded_at (datetime): The timestamp when the photo was uploaded.
            updated_at (datetime): The timestamp when the photo was last updated.

        Relationships:
            event (Event): The event associated with the photo.
        """

    __tablename__ = 'event_photos'

    id_event_photo = db.Column(db.Integer, primary_key=True, nullable=False)
    id_event = db.Column(db.Integer, db.ForeignKey('events.id_event'), nullable=False)
    photo_url = db.Column(db.String(255), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    event = db.relationship('Event', backref='photos', lazy=True)

class EventSponsor(db.Model):
    """
       Represents a sponsor of an event.

       Attributes:
           id_sponsor (int): The unique identifier for the event sponsor.
           id_event (int): The identifier of the event the sponsor supports.
           sponsor_name (str): The name of the sponsor.
           sponsor_logo (str): The URL of the sponsor's logo.

       Relationships:
           event (Event): The event associated with the sponsor.
       """

    __tablename__ = 'event_sponsors'

    id_sponsor = db.Column(db.Integer, primary_key=True, nullable=False)
    id_event = db.Column(db.Integer, db.ForeignKey('events.id_event'), nullable=False)
    sponsor_name = db.Column(db.String(255), nullable=True)
    sponsor_logo = db.Column(db.String(255), nullable=True)

    # Relationships
    event = db.relationship('Event', backref='sponsors', lazy=True)


class Tag(db.Model):
    """
        Represents a tag that can be associated with events.

        Attributes:
            id_tag (int): The unique identifier for the tag.
            tag_name (str): The name of the tag.

        Relationships:
            event (EventTag): The events associated with the tag.
        """

    __tablename__ = 'tags'

    id_tag = db.Column(db.Integer, primary_key=True, nullable=False)
    tag_name = db.Column(db.Varchar(100), nullable=False)

    # Relationships
    event = db.relationship('EventTag', backref='sponsors', lazy=True)


class EventTag(db.Model):
    """
        Represents the association between an event and a tag.

        Attributes:
            id_event (int): The identifier of the event.
            id_tag (int): The identifier of the tag.

        Relationships:
            event (Event): The event associated with the tag.
            tag (Tag): The tag associated with the event.
        """

    __tablename__ = 'event_tags'

    id_event = db.Column(db.Integer, db.ForeignKey('events.id_event'), primary_key=True, nullable=False)
    id_tag = db.Column(db.Integer, db.ForeignKey('tags.id_tag'), primary_key=True, nullable=False)

    # Relationship
    event = db.relationship('Event', backref='event_tags', lazy=True)
    tag = db.relationship('Tag', backref='event_tags', lazy=True)

class AttendeeEvent(db.Model):

    """
    Represents the attendance of a user at an event.

    Attributes:
        id_attendee (int): The unique identifier for the attendee record.
        id_event (int): The identifier of the event.
        id_user (int): The identifier of the user.
        registration_date (datetime): The date and time when the user registered for the event.

    Relationships:
        event (Event): The event the user is attending.
        user (Users): The user attending the event.
    """

    __tablename__ = 'attendees_events'

    id_attendee = db.Column(db.Integer, primary_key=True, nullable=False)
    id_event = db.Column(db.Integer,db.ForeignKey('events.id_event'), nullable=True)
    id_user = db.Column(db.Integer,db.ForeignKey('users.id_user'), nullable=True)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    event = db.relationship('Event', backref='attendees', lazy=True)
    user = db.relationship('Users', backref='attended_events', lazy=True)


class Subscription(db.Model):
    """
        Represents a user's subscription to a category.

        Attributes:
            id_subscription (int): The unique identifier for the subscription.
            id_user (int): The identifier of the user.
            id_category (int): The identifier of the category.
            subscription_date (datetime): The date and time when the subscription was created.

        Relationships:
            user (Users): The user who subscribed.
            category (Categories): The category the user subscribed to.
        """

    __tablename__ = 'subscription'

    id_subscription = db.Column(db.Integer, primary_key=True, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=True)
    id_category = db.Column(db.Integer, db.ForeignKey('categories.id_cagegory'), nullable=True)
    subscription_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('Users', backref='subscriptions', lazy=True)
    category = db.relationship('Categories', backref='subscriptions', lazy=True)
