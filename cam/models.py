from django.db import models
# from camus import models
from slugify import slugify
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Create your models here.
class Room(models.Model):
    # __tablename__ = 'rooms'
    # id = models.(models.Integer, primary_key=True)
    name = models.CharField(unique=True, max_length=100, blank=True)
    slug = models.SlugField(editable=False, blank=True)
    password_hash = models.CharField(max_length=10000, blank=True)
    guest_limit = models.IntegerField(default=100)
    is_public = models.BooleanField(default=False)
    created = models.DateTimeField(default=datetime.utcnow)
    active = models.DateTimeField(default=datetime.utcnow)

    # clients = models.ManyToManyField('Client', backref='room')

    def __repr__(self):
        return '<Room {}>'.format(self.name)

    def set_name(self, name):
        self.name = name
        self.slug = slugify(name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    
    def is_full(self):
        """Check whether the room's guest limit has been reached.

        Returns True if the guest limit has been reached, False otherwise.
        """
        return self.guest_limit and len(self.clients) >= self.guest_limit

    def active_ago(self):
        """The number of minutes ago that the room was last active."""
        now = datetime.utcnow().timestamp()
        return int((now - self.active.timestamp()) / 60)


class Client(models.Model):
    # __tablename__ = 'clients'
    # id = models.Column(models.Integer, primary_key=True)
    name = models.CharField(max_length=100)
    # uuid = models.UUIDField(unique=True, default=uuid.uuid4().hex)
    seen = models.DateTimeField(default=datetime.utcnow)

    room_id = models.ForeignKey(Room, on_delete=models.DO_NOTHING)

    def __repr__(self):
        return '<Client {}>'.format(self.uuid)
