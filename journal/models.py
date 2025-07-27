
from datetime import timedelta
import logging
import os
import uuid
from datetime import date
from typing import Optional
from uuid import uuid4
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        Group, Permission, PermissionsMixin)
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.db.models import F
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.encrypted import EncryptedTextField

# Placeholder for AI analysis function
from .generate import check_content_topic_with_openai
from .utils.ai_utils import get_sentiment  # AI module for insights


LEVEL_UP_THRESHOLD = 100


def default_due_date():
    return timezone.now().date() + timedelta(days=1)


# Removed duplicate current_timestamp function definition.


def profile_pic_upload_path(instance, filename):
    if not hasattr(instance, '_profile_pic_uuid'):
        instance._profile_pic_uuid = uuid4()
    ext = filename.split('.')[-1]
    new_filename = f"{instance._profile_pic_uuid}.{ext}"
    sissy_name = instance.sissy_name if instance.sissy_name else 'default_sissy_name'
    return os.path.join('profile_pics', sissy_name, new_filename)


def current_timestamp():
    return timezone.now()


class CustomUserManager(BaseUserManager):

    def create_user(self, email: str, password: Optional[str] = None, **extra_fields):
        """
        Create and return a regular user with an email and password.

        Args:
            email (str): The email address of the user.
            password (Optional[str]): The password for the user.
            **extra_fields: Additional fields for the user.

        Returns:
            CustomUser: The created user instance.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        if 'sissy_name' not in extra_fields or not extra_fields['sissy_name']:
            raise ValueError('The Sissy Name field must be set')
        user = self.model(email=email, sissy_name=extra_fields.pop('sissy_name'), **extra_fields)
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
    date_joined = models.DateTimeField(
        default=current_timestamp, editable=False)
    activate_account_token = models.CharField(
        max_length=64, blank=True, null=True)
    location = models.CharField(
        _('location'), max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(
        _('profile picture'), upload_to=profile_pic_upload_path, default='default-profile-pic.jpg')

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

    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(default=True)
    is_moderator = models.BooleanField(default=False)

    SUB_TIERS = (
        ('free', _('Free')),
        ('basic', _('Basic')),
        ('premium', _('Premium')),
        ('moderator', _('Moderator')),
        ('admin', _('Admin')),
    )
    subscription_tier = models.CharField(
        max_length=50, default='free', choices=SUB_TIERS)

    groups = models.ManyToManyField(Group, related_name='customuser_set_groups')
    user_permissions = models.ManyToManyField(
        Permission, related_name='customuser_set_permissions')
    locked_content = models.JSONField(default=dict)
    points = models.IntegerField(default=0)
    badges = models.JSONField(default=dict)
    level = models.IntegerField(default=1)

    objects = CustomUserManager()

    avatar = models.OneToOneField(
        'dressup.Avatar',
        on_delete=models.CASCADE,
        related_name='user_avatar',
        null=True,
        blank=True,
    )
    favorites = models.ManyToManyField(
        'dressup.PurchasedItem',
        related_name='favorite_items',
        blank=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['sissy_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'custom_user'

    def profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        else:
            return "/static/journal/media/default-profile-pic.jpg"

    def award_points(self, points):
        self.points += points
        self.check_level_up()
        self.save()

    def deduct_points(self, points):
        self.points = max(0, self.points - points)
        self.save()

    def check_level_up(self):
        while self.points >= self.level * LEVEL_UP_THRESHOLD:
            self.level += 1
            self.award_badge(f'Level {self.level} Achiever')

    def award_badge(self, badge_name):
        """Award a badge to the user."""
        self.badges[badge_name] = timezone.now().strftime(
            '%Y-%m-%d')  # Stores the date badge was earned
        self.save()

    def is_premium(self) -> bool:
        return self.subscription_tier in ['premium', 'moderator', 'admin']

    def is_basic_subscriber(self) -> bool:
        return self.subscription_tier == 'basic'

    def is_moderator_or_admin(self) -> bool:
        return self.is_moderator or self.is_staff or self.is_superuser

    def __str__(self):
        return self.sissy_name
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


logger = logging.getLogger(__name__)

User = get_user_model()

CATEGORY_CHOICES = [
    ('sissification_tasks', 'Sissification Tasks'),
    ('domme_tasks', 'Domme Tasks'),
    ('punishment_tasks', 'Punishment Tasks'),
    ('work_tasks', 'Work/Study Tasks'),
    ('self_care_tasks', 'Self Care Tasks'),
    ('chore_tasks', 'Chore Tasks'),
    ('personal_tasks', 'Personal Tasks')
]

FREQUENCY_CHOICES = [
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
    ('yearly', 'Yearly')
]

DIFFICULTY_CHOICES = [
    ('easy', 'Easy Peasy 💖'),
    ('moderate', 'Glamorous Effort ✨'),
    ('hard', 'Ultimate Sissy Challenge 💪')
]


class Habit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default='sissification_tasks')

    difficulty = models.CharField(
        max_length=20, choices=DIFFICULTY_CHOICES, default='moderate')
    start_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField(blank=True, null=True)
    frequency = models.CharField(
        max_length=10, choices=FREQUENCY_CHOICES, default='daily')

    target_count = models.PositiveIntegerField(default=8)  # Default target
    increment_counter = models.PositiveIntegerField(default=0)
    last_reset_date = models.DateField(blank=True, null=True)

    longest_streak_days = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.name} ({self.get_difficulty_display()})"

    def is_completed(self):
        """Check if the habit has reached its target count for the current period."""
        return self.increment_counter >= self.target_count

    def reset_counter(self):
        """Reset the counter based on the habit's frequency."""
        self.increment_counter = 0
        self.last_reset_date = timezone.now().date()
        self.save(update_fields=['increment_counter', 'last_reset_date'])

    def check_reset_needed(self):
        """Determine if the habit counter needs to reset."""
        if self.last_reset_date is None:
            return True
        today = timezone.now().date()

        reset_conditions = {
            'daily': self.last_reset_date < today,
            'weekly': self.last_reset_date < today - timedelta(days=7),
            'monthly': self.last_reset_date.month != today.month,
            'yearly': self.last_reset_date.year != today.year
        }
        return reset_conditions.get(self.frequency, False)

    @transaction.atomic
    def increment_count(self):
        """Increment the habit counter, ensuring streaks are updated."""
        try:
            if self.check_reset_needed():
                self.reset_counter()

            Habit.objects.filter(pk=self.pk).update(
                increment_counter=F('increment_counter') + 1,
                last_reset_date=timezone.now().date()
            )
            self.refresh_from_db(fields=['increment_counter', 'last_reset_date'])

            self.update_streaks()
        except Exception as e:
            logger.error(f"Error incrementing habit: {e}")
            raise

    def update_streaks(self):
        """Track the longest streak and maintain current streak count."""
        current_streak = self.get_current_streak()
        if current_streak > self.longest_streak_days:
            self.longest_streak_days = current_streak
            self.save(update_fields=['longest_streak_days'])

    def get_current_streak(self):
        """Calculate the current streak based on consecutive completions."""
        return self.increment_counter  # Could expand to track actual date-based streaks

    def get_longest_streak(self):
        return self.longest_streak_days

    def get_insights(self):
        """Provide AI-driven habit insights and motivation."""
        if self.increment_counter == 0:
            return "You haven't started this habit yet. Time to get fabulous!"

        # Dynamic encouragement
        encouragements = {
            'easy': "Nice start! Keep up the easy wins, babe! 💖",
            'moderate': "You're building momentum! Stay consistent! ✨",
            'hard': "You're slaying this challenge! Absolute queen behavior! 👑"
        }
        encouragement = encouragements.get(
            self.difficulty, "Keep going, you're amazing!")

        # Streak-based motivation
        if self.increment_counter >= self.target_count:
            return f"OMG, you completed **{self.name}** for this period! 🎉 {encouragement}"
        elif self.increment_counter > 10:
            return f"Great job! You've hit **{self.increment_counter}** times in **{self.name}**! Keep it up! 💃"
        else:
            return "You're making progress, but there's room to improve. Try to be more consistent. 💕"

    def analyze_journal_correlation(self):
        """Analyze user's journal entries for patterns related to this habit."""

        journal_entries = JournalEntry.objects.filter(
            user=self.user).order_by('-timestamp')[:10]
        if not journal_entries.exists():
            return "Not enough journal entries to analyze habit impact."

        sentiment_analysis = [get_sentiment(
            entry.content) for entry in journal_entries]
        avg_polarity = sum(
            score[1] for score in sentiment_analysis) / len(sentiment_analysis)
        avg_subjectivity = sum(
            score[2] for score in sentiment_analysis) / len(sentiment_analysis)

        if avg_polarity > 0.5:
            return "Your journal entries suggest **habit success** is making you **happier**! Keep it up! 😊"
        elif avg_polarity < -0.3:
            return "Your journaling shows some struggle with this habit. Maybe try a different approach? 💭"
        else:
            return "Your habit and journaling are neutral. Maybe reflect on your progress more deeply? ✍️"

    def get_milestone_rewards(self):
        """Encourage user with milestone-based rewards."""
        if self.increment_counter == 5:
            return "Woohoo! 5 streaks reached! You've earned a treat! 🎀"
        elif self.increment_counter == 10:
            return "Double digits! You should reward yourself with a new sissy accessory! 👗"
        elif self.increment_counter == 20:
            return "20 streaks?! You’re unstoppable! Maybe a **special challenge** is in order! 🎯"
        return None


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
    """
    A generic model to relate any object via a GenericForeignKey.
    Stores the content type, object ID, and timestamp for tracking relationships.
    
    Stores the content type, object ID, and timestamp for tracking relationships.
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True)
    related_models = GenericRelation(RelatedModel)


class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    # needs to make sure that only a user that is grouped as a professional can answer
    professional = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True)
    related_models = GenericRelation(RelatedModel)


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100, default='Sissy Sparkles')
    timestamp = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    comments = GenericRelation('Comment', related_query_name='blog_comments')
    

class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)


class ResourceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    resources = models.ManyToManyField(Resource, related_name='categories')

    def __str__(self):
        return self.name

    def get_featured_resource(self):
        """Returns the latest featured resource for the category."""
        return self.resources.filter(featured=True).order_by('-timestamp').first()


class ResourceComment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.timestamp:%Y-%m-%d})"

    class Meta:
        ordering = ['-timestamp']
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
    task_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    
    def __str__(self):
        description_preview = self.description[:50] if self.description else "No description"
        return f"Task for {self.user.sissy_name}: {description_preview}"
# Configuring logger for the module
logger = logging.getLogger(__name__)
User = get_user_model()


def current_timestamp():
    return timezone.now()


class JournalEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="entries",
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = EncryptedTextField()
    prompt_text = EncryptedTextField(blank=True, null=True)
    insight = EncryptedTextField(blank=True, null=True)
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
    points = models.IntegerField(default=0)
    is_on_topic = models.BooleanField(default=False)  # NEW

    @staticmethod
    def get_last_5_entries(user):
        return JournalEntry.objects.filter(user=user).order_by('-id')[:5]

    def calculate_points(self):
        # Points logic (kept from original)
        points = 0
        if self.is_sissy():
            points += 10
        if self.is_good_length():
            points += 5
        if self.sentiment == 'positive':
            points += 10
        elif self.sentiment == 'negative':
            points -= 10
        if self.polarity is not None:
            points += 5 if self.polarity > 0.5 else -5
        if self.subjectivity is not None:
            points += 5 if self.subjectivity > 0.5 else -5
        # Bonus for on-topic entries
        if self.is_on_topic:
            points += 10
        return points

    def is_sissy(self):
        # (Long keyword list omitted for brevity)
        keywords = ['sissy', 'feminine', 'dress', 'heels', 'makeup', 'lingerie', 'panties',
                    'skirt', 'stockings', 'bra', 'feminization', 'femme', 'girly', 'sissify',
                    'femboy', 'femboi', 'femdom', 'mistress', 'dominatrix', 'chastity',
                    'submission', 'submissive', 'slave', 'pet', 'sissy']
        content_lower = self.content.lower()
        return sum(kw in content_lower for kw in keywords) >= 5

    def is_good_length(self):
        return len(self.content.split()) >= 100

    def analyze_content(self):
        """
        Uses OpenAI to determine if the entry is on-topic.
        """
        if not self.prompt_text:
            return False
        try:
            return check_content_topic_with_openai(self.content, self.prompt_text)
        except Exception as e:
            logger.error(f"Error during content analysis: {e}")
            return False

    def save(self, *args, **kwargs):
        # Analyse sentiment
        sentiment, polarity, subjectivity = get_sentiment(self.content)
        self.sentiment = sentiment
        self.polarity = polarity
        self.subjectivity = subjectivity
        # Determine on-topic status
        self.is_on_topic = self.analyze_content()
        # Save once to get ID
        super().save(*args, **kwargs)
        # Calculate points
        self.points = self.calculate_points()
        super().save(update_fields=['points'])

    def __str__(self):
        return f"{self.user} - {self.title}"


class JournalAnalyzer:
    @staticmethod
    def calculate_average_sentiment(user: 'CustomUser'):
        entries = JournalEntry.get_last_5_entries(user)
        if not entries:
            return "neutral"

        sentiment_scores = {'positive': 1, 'neutral': 0, 'negative': -1}
        total_score = sum(
            sentiment_scores[entry.sentiment] for entry in entries if entry.sentiment is not None)
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

        total_polarity = sum(
            entry.polarity for entry in entries if entry.polarity is not None)
        return total_polarity / len(entries)

    @staticmethod
    def calculate_average_subjectivity(user):
        entries = JournalEntry.get_last_5_entries(user)
        if not entries:
            return 0.0

        total_subjectivity = sum(
            entry.subjectivity for entry in entries if entry.subjectivity is not None)
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
    id = models.AutoField(primary_key=True)
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
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class UserTheme(models.Model):
    """
    Stores user-specific theme preferences such as color and layout.
    """
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
    # free, basic, premium, moderator, admin
    subscription_tier = models.CharField(max_length=50, default='free')
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"{self.user.sissy_name}'s {self.subscription_tier} subscription"
        )

            billing.is_active = False
            billing.is_active = False
            billing.user.subscription_tier = 'free'
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
