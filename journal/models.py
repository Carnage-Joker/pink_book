from pyexpat.errors import messages
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from .validators import validate_sissy_name
from django.conf import settings
from .ai_utils import  get_sentiment
from django.db.models import Avg
from django.contrib.auth import get_user_model

class CommunityPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('journal.CustomUser', on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Moderator(models.Model):
    user = models.OneToOneField('journal.CustomUser', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username




class RelatedModel(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

class CustomUserManager(BaseUserManager):
    def create_user(self, sissy_name, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, sissy_name=sissy_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, sissy_name, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(sissy_name, email, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
        date_of_birth = models.DateField(blank=True, null=True)
        sissy_name = models.CharField(max_length=100, unique=True, validators=[validate_sissy_name])
        bio = models.TextField(blank=True)
        location = models.CharField(max_length=100, blank=True)
        profile_picture = models.ImageField(upload_to='media/profile_pics', default='default.jpg')
        PRONOUN_CHOICES = (
        ('he/him', 'he/him'),
        ('she/her', 'she/her'),
        ('they/them', 'they/them'),
        ('other', 'other'),
    )
        pronouns = models.CharField(max_length=20, choices=PRONOUN_CHOICES, blank=True, default='')
        SISSY_TYPE_CHOICES = (
        ('sissy_maid', 'Maid'),
        ('sissy_bimbo', 'Bimbo'),
        ('sissy_schoolgirl', 'Schoolgirl'),
        ('sissy_slut', 'Slut'),
        ('bratty_sissy', 'Brat'),
    )
        sissy_type = models.CharField(max_length=100, choices=SISSY_TYPE_CHOICES, blank=True)
        CHASTITY_CHOICES = (
        ('yes', 'I always wear a chastity device'),
        ('no', 'I never wear a chastity device'),
        ('partly', 'I sometimes wear a chastity device'),
    )
        chastity_status = models.CharField(max_length=100, choices=CHASTITY_CHOICES, blank=True)
        OWNED_CHOICES = (
        ('yes', 'I have an owner'),
        ('no', 'I do not have an owner'),
    )
        owned_status = models.CharField(max_length=100, choices=OWNED_CHOICES, blank=True)
        class Meta:
            app_label = 'journal'

        objects = CustomUserManager()
        USERNAME_FIELD = 'sissy_name'
        REQUIRED_FIELDS = ['email']

        def __str__(self):
            return self.sissy_name

        def save(self, *args, **kwargs):
            super(CustomUser, self).save(*args, **kwargs)
            # Additional save logic if needed



class UserProfile(models.Model):
    user = models.OneToOneField('journal.CustomUser', on_delete=models.CASCADE)
    PRIVACY_CHOICES = [
        ('public', 'Public Darling 💋'),
        ('friends', 'Just for Friends 🎀'),
        ('private', 'My Secret 🤫'),
    ]
    privacy_level = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    nsfw_blur = models.BooleanField(default=False, verbose_name="Blur NSFW Content 🙈")

    def __str__(self):
        return f"{self.user.sissy_name}'s Settings"


    
#Journal Models
class EditTag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    
class JournalEntry(models.Model):
    user = models.ForeignKey('journal.CustomUser', on_delete=models.CASCADE, related_name='journal_entries')
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    audio = models.FileField(upload_to='audios/', blank=True, null=True)
    file = models.FileField(upload_to='files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    polarity = models.FloatField(null=True, blank=True)
    subjectivity = models.FloatField(null=True, blank=True)
    sentiment = models.CharField(max_length=20, blank=True, null=True)
    insight = models.TextField(null=True, blank=True)
    insight1 = models.TextField(null=True, blank=True)
    insight2 = models.TextField(null=True, blank=True)


    REQUIRED_FIELDS = ['title', 'content']
    def save(self, *args, **kwargs):
        self.sentiment = get_sentiment(self.content)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title



class JournalEntryTag(models.Model):
    journal_entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.journal_entry.title} - {self.tag.name}'
    
#Forum Models

class Category(models.Model):
    name = models.CharField(max_length=100, default="Default Category")

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField()
    author = models.ForeignKey('journal.CustomUser', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('journal.CustomUser', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    comments = GenericRelation(Comment)

#Reports
    # rest of your fields and methods
class Report(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    reason = models.TextField()
    reported_by = models.ForeignKey('journal.CustomUser', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

#Resources Models
class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    allow_comments = models.BooleanField(default=True)
    id = models.PositiveIntegerField(primary_key=True)

    def __str__(self):
        return self.title

class Article(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ResourceCategory(models.Model):
    name = models.CharField(max_length=100)
    resources = models.ManyToManyField(Resource, related_name='categories')
    articles = models.ManyToManyField(Article, related_name='categories')

    def __str__(self):
        return self.name

class ResourceComment(models.Model):
    content = models.TextField()
    author = models.ForeignKey('journal.CustomUser', on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
#Habit Trackers Models

class Habit(models.Model):
    user = models.ForeignKey('journal.CustomUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_date = models.DateField(default=date.today) 
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reminder_frequency = models.CharField(max_length=10, choices=[('daily', 'Daily'), ('weekly', 'Weekly')])

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + relativedelta(months=1)
        super(Habit, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class ToDo(models.Model):
    user = models.ForeignKey('journal.CustomUser', on_delete=models.CASCADE)
    task = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task

class UserFeedback(models.Model):
    user = models.ForeignKey('journal.CustomUser', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class Theme:
    def __init__(self, color='default_color', layout='default_layout'):
        self.color = color
        self.layout = layout

class UserTheme(models.Model):
    user = models.OneToOneField('journal.CustomUser', on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    layout = models.CharField(max_length=50)
    