
from django.contrib.auth import get_user_model
from math import e
import os
import uuid
from datetime import date, datetime, timedelta
from uuid import uuid4

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        Group, Permission, PermissionsMixin)
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .utils.ai_utils import get_sentiment

LEVEL_UP_THRESHOLD = 100


def default_due_date():
    return timezone.now().date() + timedelta(days=1)


def current_timestamp():
    return timezone.now()


def profile_pic_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join('profile_pics', instance.sissy_name, filename)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    bio = models.CharField(_('bio'), max_length=500, blank=True, null=True)
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    sissy_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=current_timestamp, editable=False)
    activate_account_token = models.CharField(
        max_length=64, blank=True, null=True)
    location = models.CharField(
        _('location'), max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(
        _('profile picture'), upload_to='profile_pics', default='default.jpg')

    PRONOUN_CHOICES = (
        ('he/him', _('he/him')),
        ('she/her', _('she/her')),
        ('they/them', _('they/them')),
        ('other', _('other')),
    )
    pronouns = models.CharField(
        _('pronouns'), max_length=20, choices=PRONOUN_CHOICES, blank=True, default='')

    SISSY_TYPE_CHOICES = (
        ('sissy_maid', _('Maid')),
        ('sissy_bimbo', _('Bimbo')),
        ('sissy_schoolgirl', _('Schoolgirl')),
        ('sissy_slut', _('Slut')),
        ('bratty_sissy', _('Brat')),
    )
    sissy_type = models.CharField(
        _('sissy type'), max_length=100, choices=SISSY_TYPE_CHOICES, blank=True)

    CHASTITY_CHOICES = (
        ('yes', _('I always wear a chastity device')),
        ('no', _('I never wear a chastity device')),
        ('partly', _('I sometimes wear a chastity device')),
    )
    chastity_status = models.CharField(
        _('chastity status'), max_length=100, choices=CHASTITY_CHOICES, blank=True)

    OWNED_CHOICES = (
        ('yes', _('I have an owner')),
        ('no', _('I do not have an owner')),
    )
    owned_status = models.CharField(
        _('owned status'), max_length=100, choices=OWNED_CHOICES, blank=True)

    collective_insight = models.CharField(
        _('collective insight'), max_length=1000, null=True, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    SUB_TIERS = (
        ('free', _('Free')),
        ('basic', _('Basic')),
        ('premium', _('Premium')),
        ('moderator', _('Moderator')),
        ('admin', _('Admin')),
    )
    subscription_tier = models.CharField(max_length=50, default='free', choices=SUB_TIERS)  # free, basic, premium, moderator, admin
    is_subscriber = models.BooleanField(default=False)
    avatar_body = models.CharField(
        max_length=255, default="/static/virtual_try_on/avatars/body/light/hourglass.png")
    avatar_hair = models.CharField(
        max_length=255, default="/static/virtual_try_on/avatars/hair/long_straight/blonde.png")
    avatar_top = models.CharField(
        max_length=255, default="/static/virtual_try_on/garmets/tops/1.png")
    avatar_bottom = models.CharField(
        max_length=255, default="/static/virtual_try_on/garmets/skirts/1.png")
    avatar_shoes = models.CharField(
        max_length=255, default="/static/virtual_try_on/garmets/shoes/1.png")
    groups = models.ManyToManyField(Group, related_name='customuser_groups')
    user_permissions = models.ManyToManyField(
        Permission, related_name='customuser_permissions')
    locked_content = models.JSONField(default=dict)
    points = models.IntegerField(default=0)
    badges = models.JSONField(default=dict)
    level = models.IntegerField(default=1)

    objects = CustomUserManager()

    USERNAME_FIELD = 'sissy_name'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'custom_user'

    def award_points(self, points):
        self.points += points
        self.check_level_up()
        self.save()

    def deduct_points(self, points):
        self.points = max(0, self.points - points)
        self.save()

    def check_level_up(self):
        """Check if the user qualifies for a level up and handle it."""
        while self.points >= self.level * LEVEL_UP_THRESHOLD:
            self.level += 1
            self.award_badge(f'Level {self.level} Achiever')
            # Optionally: Notify the user of their level up

    def award_badge(self, badge_name):
        """Award a badge to the user if they don't already have it."""
        if badge_name not in self.badges:
            self.badges[badge_name] = now().strftime(
                '%Y-%m-%d')  # Stores the date badge was earned
            self.save()

    def has_badge(self, badge_name):
        """Check if the user has a specific badge."""
        return badge_name in self.badges

    def lock_content(self, content_name):
        self.locked_content[content_name] = True
        self.save()

    def is_premium(self):
        return self.subscription_tier in ['premium', 'moderator', 'admin']

    def is_basic_subscriber(self):
        return self.subscription_tier == 'basic'

    def is_moderator_or_admin(self):
        return self.is_moderator or self.is_staff or self.is_superuser
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.sissy_name

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)

# Habit Trackers Models
# Assuming the models are in journal/models.py


REWARD_CHOICES = [
    ('praise', 'Praise'),
    ('points', 'Points'),
    ('gift', 'Gift'),
    ('privilege', 'Privilege'),
    ('none', 'None')
]

PENALTY_CHOICES = [
    ('ignore', 'Ignore'),
    ('punishment', 'Punishment'),
    ('task', 'Task'),
    ('points_loss', 'Lose Points'),
    ('none', 'None')
]


class Habit(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    start_date = models.DateField(default=timezone.now)
    date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    increment_counter = models.IntegerField(default=0)
    reward = models.CharField(
        max_length=50, choices=REWARD_CHOICES, null=True, blank=True)
    penalty = models.CharField(
        max_length=50, choices=PENALTY_CHOICES, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    reminder_frequency = models.CharField(
        max_length=10,
        choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly',
                                                            'Monthly'), ('yearly', 'Yearly'), ('none', 'None')],
        default='daily'
    )
    category = models.CharField(
        max_length=50,
        choices=[('fashion_goals', 'Fashion Goals'), ('behavioral_goals', 'Behavioral Goals'), ('sissification_tasks', 'Sissification Tasks'),
                 ('performance_tasks', 'Performance Tasks'), ('chastity_goals',
                                                              'Chastity Goals'), ('self_care', 'Self care'),
                 ('domme_appreciation', 'Domme Appreciation'), ('orders', 'Orders')],
        default='sissification_tasks'
    )
    last_reset_date = models.DateField(
        blank=True, null=True, default=timezone.now)  # Use timezone.now
    longest_streak_days = models.IntegerField(
        default=0)  # To store the longest streak

    def check_reset_needed(self):
        today = timezone.now().date()  # Ensure 'today' is a date object
        if self.last_reset_date is None or self.last_reset_date.date() < today:
            self.reset_count()

    def reset_count(self):
        self.increment_counter = 0
        self.last_reset_date = timezone.now().date()  # Make sure it's stored as a date
        self.save()                 
    
    def get_current_streak(self):
        today = timezone.now().date()

        if not self.last_reset_date:
            return 0

        if self.last_reset_date == today:
            streak_days = (today - self.start_date).days
        else:
            streak_days = 0  # Streak is broken if not tracked today

        return streak_days

    def get_longest_streak(self):
        # Assume the longest streak is stored in `longest_streak_days` field.
        # If not, you could also calculate it similarly to `get_current_streak`.
        return self.longest_streak_days

    def update_streaks(self):
        # Call this method whenever a habit is tracked to update the streaks.
        current_streak = self.get_current_streak()

        if current_streak > self.longest_streak_days:
            self.longest_streak_days = current_streak

        self.save()

    def increment_count(self):
        self.increment_counter += 1
        self.update_streaks()  # Call this to update streaks whenever the count is incremented
        self.save()
    
    def get_insights(self):
        if self.increment_counter == 0:
            return "You haven't started this habit yet."
        elif self.increment_counter > 10:
            return f"Great job! You've hit {self.increment_counter} in {self.name}. Keep it up!"
        else:
            return "You're making progress, but there’s room to improve. Try to be more consistent."

    def save(self, *args, **kwargs):
        self.check_reset_needed()
        super().save(*args, **kwargs)


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


class Guide(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class RelatedModel(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)
    """_summary_

    Returns:
        _type_: _description_
    """


class Question(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True)
    related_models = GenericRelation(RelatedModel)


class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    professional = models.ForeignKey(CustomUser, on_delete=models.CASCADE) ## needs to make sure that only a user that is grouped as a professional can answer
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True)
    related_models = GenericRelation(RelatedModel)


class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    allow_comments = models.BooleanField(default=True)
    category = models.CharField(max_length=50, choices=[  # Add more categories as needed
        ('fashion', 'Fashion'),
        ('beauty', 'Beauty'),
        ('health', 'Health'),
        ('fitness', 'Fitness'),
        ('lifestyle', 'Lifestyle'),
        ('other', 'Other')
    ], default='other')


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100, default='Sissy Sparkles')
    timestamp = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    comments = GenericRelation('Comment', related_query_name='blog_comments')


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


class Task(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    points_awarded = models.IntegerField(default=10)
    points_penalty = models.IntegerField(default=20)
    completed = models.BooleanField(default=False)
    task_id = models.IntegerField(null=True, unique=True)

    def __str__(self):
        return f"Task for {self.user.sissy_name}: {self.description[:50]}"


class JournalEntry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='entries',
        on_delete=models.CASCADE)
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
    task = models.TextField(blank=True, null=True)

    @staticmethod
    def get_last_5_entries(user):
        return JournalEntry.objects.filter(user=user).order_by('-id')[:5]

    def save(self, *args, **kwargs):
        sentiment, polarity, subjectivity = get_sentiment(self.content)
        self.sentiment = sentiment
        self.polarity = polarity
        self.subjectivity = subjectivity
        super().save(*args, **kwargs)

        
class JournalAnalyzer:
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


class TaskCompletion(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    journal_entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} completed {self.task}"
    
    
class Report(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    reason = models.TextField()
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Quote(models.Model):
    content = models.TextField()
    author = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)


class Thread(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='profile')
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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.content_object}'


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    comments = GenericRelation(Comment, related_query_name='post_comments')

    def __str__(self):
        return f"Post by {self.author.sissy_name} in {self.thread}"

    def get_absolute_url(self):
        # Replace 'journal:post_detail' with the actual name of your post detail URL pattern
        return reverse('journal:post_detail', args=[self.id])


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


class Billing(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subscription_tier = models.CharField(max_length=50, default='free')  # free, basic, premium, moderator, admin
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.sissy_name}'s {self.subscription_tier} subscription"

    def check_subscription_status():
        for billing in Billing.objects.filter(is_active=True):
            if billing.end_date < timezone.now().date():
                billing.is_active = False
                billing.user.subscription_tier = 'free'
                billing.user.is_subscriber = False
                billing.save()
                billing.user.save()


class Message(models.Model):
    sender = models.ForeignKey(
        CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.sissy_name} to {self.receiver.sissy_name}"


class ActivityLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.sissy_name} - {self.action}"


class Faq(models.Model):
    question = models.CharField(max_length=200, blank=True, null=True)
    answer = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.question
    