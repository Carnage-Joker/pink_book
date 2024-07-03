from django.contrib.auth import get_user_model
import os
from datetime import date, datetime, timedelta
from uuid import uuid4

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        Group, Permission, PermissionsMixin)
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .utils.ai_utils import get_sentiment


def default_due_date():
    return datetime.now().date() + timedelta(days=1)


def current_timestamp():
    return datetime.now()


def profile_pic_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join('profile_pics', instance.sissy_name, filename)


class CustomUserManager(BaseUserManager):
    def create_user(self, sissy_name, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, sissy_name=sissy_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, sissy_name, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(sissy_name, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    bio = models.CharField(_('bio'), max_length=500, blank=True, null=True)
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    sissy_name = models.CharField(
        _('sissy name'),
        max_length=255,
        unique=True,
    )
    location = models.CharField(
        _('location'), max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(
        _('profile picture'),
        upload_to=profile_pic_upload_path,
        default='default.jpg'
    )

    PRONOUN_CHOICES = (
        ('he/him', _('he/him')),
        ('she/her', _('she/her')),
        ('they/them', _('they/them')),
        ('other', _('other')),
    )
    pronouns = models.CharField(
        _('pronouns'),
        max_length=20,
        choices=PRONOUN_CHOICES,
        blank=True,
        default=''
    )

    SISSY_TYPE_CHOICES = (
        ('sissy_maid', _('Maid')),
        ('sissy_bimbo', _('Bimbo')),
        ('sissy_schoolgirl', _('Schoolgirl')),
        ('sissy_slut', _('Slut')),
        ('bratty_sissy', _('Brat')),
    )
    sissy_type = models.CharField(
        _('sissy type'),
        max_length=100,
        choices=SISSY_TYPE_CHOICES,
        blank=True
    )

    CHASTITY_CHOICES = (
        ('yes', _('I always wear a chastity device')),
        ('no', _('I never wear a chastity device')),
        ('partly', _('I sometimes wear a chastity device')),
    )
    chastity_status = models.CharField(
        _('chastity status'),
        max_length=100,
        choices=CHASTITY_CHOICES,
        blank=True
    )

    OWNED_CHOICES = (
        ('yes', _('I have an owner')),
        ('no', _('I do not have an owner')),
    )
    owned_status = models.CharField(
        _('owned status'),
        max_length=100,
        choices=OWNED_CHOICES,
        blank=True
    )

    collective_insight = models.CharField(
        _('collective insight'), max_length=1000, null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'sissy_name'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'custom_user'

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',
    )
    points = models.IntegerField(default=0)
    # Using JSONField to store locked content
    locked_content = models.JSONField(default=dict)


    points = models.IntegerField(default=0)
    badges = models.JSONField(default=dict)
    level = models.IntegerField(default=1)

    def award_points(self, points):
        self.points += points
        self.check_level_up()
        self.save()

    def deduct_points(self, points):
        self.points = max(0, self.points - points)
        self.save()

    def add_badge(self, badge_name):
        badges = self.badges
        if badge_name not in badges:
            badges[badge_name] = datetime.now().strftime('%Y-%m-%d')
            self.badges = badges
            self.save()

    def check_level_up(self):
        # Example logic for leveling up
        required_points = self.level * 100  # Adjust as needed
        if self.points >= required_points:
            self.level += 1
            self.add_badge(f'Level {self.level} Achieved')

    def lock_content(self, content_name):
        self.locked_content[content_name] = True
        self.save()

    def __str__(self):
        return self.sissy_name

    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)


# Habit Trackers Models
# Assuming the models are in journal/models.py

REWARD_CHOICES = [
    ('sticker', 'Digital Sticker'),
    ('unlock_content', 'Unlock New Content'),
    # ... more rewards
]

PENALTY_CHOICES = [
    ('reminder', 'Reminder Message'),
    ('lock_content', 'Lock Content'),
    ('50_lines', 'Write 50 lines'),
    ('corner_time', '15 minutes Corner Time'),
    # ... more penalties
]


class Habit(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    reward = models.CharField(
        max_length=50, choices=REWARD_CHOICES, null=True, blank=True)
    penalty = models.CharField(
        max_length=50, choices=PENALTY_CHOICES, null=True, blank=True)
    timestamp = models.DateTimeField(default=datetime.now())
    reminder_frequency = models.CharField(max_length=10, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('none', 'None')
    ], default='daily')
    category = models.CharField(max_length=50, choices=[
        ('fashion_goals', 'Fashion Goals'),
        ('behavioral_goals', 'Behavioral Goals'),
        ('sissification_tasks', 'Sissification Tasks'),
        ('performance_tasks', 'Performance Tasks'),
        ('chastity_goals', 'Chastity Goals'),
        ('self_care', 'Self care'),
        ('domme_appreciation', 'Domme Appreciation'),
        ('orders', 'Orders')
    ], default='sissification_tasks')
    progress = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + relativedelta(months=1)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ToDo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    task = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    priority = models.IntegerField(default=1)
    category = models.CharField(max_length=50, choices=[
        ('Domme', 'Domme Task'),
        ('Sissy', 'Sissy Task'),
        ('Punishment', 'Punishment Task'),
        ('work', 'Work/Study Task'),
        ('self_care', 'Self Care Task'),
        ('chore', 'Chore Task'),
        ('personal', 'Personal Task')], default='personal')
    reward = models.CharField(
        max_length=50, choices=REWARD_CHOICES, null=True, blank=True)
    penalty = models.CharField(
        max_length=50, choices=PENALTY_CHOICES, null=True, blank=True)
    due_date = models.DateField(default=default_due_date, null=True)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=current_timestamp)
    processed = models.BooleanField(default=False)
    failed = models.BooleanField(default=False)
    penalty_issued = models.BooleanField(default=False)
    reward_issued = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('journal:todo_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.task


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Message(models.Model):
    sender = models.ForeignKey(
        CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.sissy_name} to {self.receiver.sissy_name}"


class RelatedModel(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)


class ActivityLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.sissy_name} - {self.action}"


class Billing(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.sissy_name}'s {self.subscription_type} subscription"
# Resource Models


class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    allow_comments = models.BooleanField(default=True)


class ResourceCategory(models.Model):
    name = models.CharField(max_length=100)
    resources = models.ManyToManyField(Resource, related_name='categories')


class ResourceComment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

# Contact Model (assuming you need one)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

# Moderator Model


class Moderator(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
# JournalEntry Model


class JournalEntry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='journal_entries', 
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    # Field to store the generated prompt
    prompt_text = models.TextField(blank=True, null=True)
    # Field to store the generated insight
    insight = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    audio = models.FileField(upload_to='audios/', blank=True, null=True)
    file = models.FileField(upload_to='files/', blank=True, null=True)
    polarity = models.FloatField(null=True, blank=True)
    subjectivity = models.FloatField(null=True, blank=True)
    sentiment = models.CharField(max_length=20, blank=True, null=True)

    @staticmethod
    def get_last_5_entries(user):
        return JournalEntry.objects.filter(user=user).order_by('-id')[:5]

    @staticmethod
    def calculate_average_sentiment(user):
        entries = JournalEntry.get_last_5_entries(user)
        if not entries:
            return "neutral"

        sentiment_scores = {'positive': 1, 'neutral': 0, 'negative': -1}
        total_score = sum(
            sentiment_scores[entry.sentiment] for entry in entries)
        average_score = total_score / len(entries)

        if average_score > 0:
            return "positive"
        elif average_score < 0:
            return "negative"
        else:
            return "neutral"

    @staticmethod
    def calculate_average_polarity(user):
        entries = JournalEntry.get_last_5_entries(user)
        if not entries:
            return 0.0

        total_polarity = sum(entry.polarity for entry in entries)
        return total_polarity / len(entries)

    @staticmethod
    def calculate_average_subjectivity(user):
        entries = JournalEntry.get_last_5_entries(user)
        if not entries:
            return 0.0

        total_subjectivity = sum(entry.subjectivity for entry in entries)
        return total_subjectivity / len(entries)

    def save(self, *args, **kwargs):
        self.sentiment, self.polarity, self.subjectivity = get_sentiment(
            self.content)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('journal:entry_detail', kwargs={'pk': self.pk})


class Report(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    reason = models.TextField()
    reported_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Quote(models.Model):
    content = models.TextField()
    author = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)


class Thread(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    PRIVACY_CHOICES = [
        ('public', 'Public Darling 💋'),
        ('friends', 'Just for Friends 🎀'),
        ('private', 'My Secret 🤫'),
    ]
    privacy_level = models.CharField(
        max_length=10, choices=PRIVACY_CHOICES, default='public')
    nsfw_blur = models.BooleanField(
        default=False, verbose_name="Blur NSFW Content 🙈")
    insight_opt = models.BooleanField(
        default=False, verbose_name="Ai Insight Opt In")

    def __str__(self):
        return f"{self.user.sissy_name}'s Settings"


class Comment(models.Model):
    entry = models.ForeignKey(
        JournalEntry, related_name='comments', on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # Choose either auto_now_add or default
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, )
    comments = GenericRelation(Comment, related_query_name='post_comments')

    def __str__(self):
        return f"Post by {self.author.sissy_name} in {self.category}"


class UserFeedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.content


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class UserTheme(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    layout = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.sissy_name}'s Theme"


class Streak(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name='streaks', on_delete=models.CASCADE)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + relativedelta(days=1)
        super(Streak, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.sissy_name
# Tag Model
