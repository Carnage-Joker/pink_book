# Generated by Django 5.2 on 2025-05-04 09:02

import datetime
import django.db.models.deletion
import django.utils.timezone
import journal.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("dressup", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogPost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("content", models.TextField()),
                ("author", models.CharField(default="Sissy Sparkles", max_length=100)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("published", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150)),
                ("email", models.EmailField(max_length=254)),
                ("subject", models.CharField(max_length=200)),
                ("message", models.TextField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-timestamp"],
            },
        ),
        migrations.CreateModel(
            name="Faq",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question", models.CharField(blank=True, max_length=200, null=True)),
                ("answer", models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Guide",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("content", models.TextField()),
                ("author", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Quote",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("author", models.CharField(max_length=100)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Resource",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("link", models.URLField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("featured", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Thread",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("content", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "bio",
                    models.CharField(
                        blank=True, max_length=500, null=True, verbose_name="bio"
                    ),
                ),
                (
                    "date_of_birth",
                    models.DateField(
                        blank=True, null=True, verbose_name="date of birth"
                    ),
                ),
                ("sissy_name", models.CharField(max_length=100, unique=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=journal.models.current_timestamp, editable=False
                    ),
                ),
                (
                    "activate_account_token",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "location",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="location"
                    ),
                ),
                (
                    "profile_picture",
                    models.ImageField(
                        default="default-profile-pic.jpg",
                        upload_to=journal.models.profile_pic_upload_path,
                        verbose_name="profile picture",
                    ),
                ),
                (
                    "pronouns",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("he/him", "he/him"),
                            ("she/her", "she/her"),
                            ("they/them", "they/them"),
                            ("other", "other"),
                        ],
                        default="",
                        max_length=20,
                        verbose_name="pronouns",
                    ),
                ),
                (
                    "sissy_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("sissy_maid", "Maid"),
                            ("sissy_bimbo", "Bimbo"),
                            ("sissy_schoolgirl", "Schoolgirl"),
                            ("sissy_slut", "Slut"),
                            ("bratty_sissy", "Brat"),
                        ],
                        max_length=100,
                        verbose_name="sissy type",
                    ),
                ),
                (
                    "chastity_status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("yes", "I always wear a chastity device"),
                            ("no", "I never wear a chastity device"),
                            ("partly", "I sometimes wear a chastity device"),
                        ],
                        max_length=100,
                        verbose_name="chastity status",
                    ),
                ),
                (
                    "owned_status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("yes", "I have an owner"),
                            ("no", "I do not have an owner"),
                        ],
                        max_length=100,
                        verbose_name="owned status",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(default=False, verbose_name="staff status"),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_moderator", models.BooleanField(default=False)),
                (
                    "subscription_tier",
                    models.CharField(
                        choices=[
                            ("free", "Free"),
                            ("basic", "Basic"),
                            ("premium", "Premium"),
                            ("moderator", "Moderator"),
                            ("admin", "Admin"),
                        ],
                        default="free",
                        max_length=50,
                    ),
                ),
                ("locked_content", models.JSONField(default=dict)),
                ("points", models.IntegerField(default=0)),
                ("badges", models.JSONField(default=dict)),
                ("level", models.IntegerField(default=1)),
                (
                    "avatar",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_avatar",
                        to="dressup.avatar",
                    ),
                ),
                (
                    "favorites",
                    models.ManyToManyField(
                        blank=True,
                        related_name="favorite_items",
                        to="dressup.purchaseditem",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        related_name="customuser_groups", to="auth.group"
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        related_name="customuser_permissions", to="auth.permission"
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "db_table": "custom_user",
            },
        ),
        migrations.CreateModel(
            name="ActivityLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("action", models.CharField(max_length=200)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Billing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("subscription_tier", models.CharField(default="free", max_length=50)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("is_active", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("object_id", models.PositiveIntegerField()),
                ("content", models.TextField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Habit",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("sissification_tasks", "Sissification Tasks"),
                            ("domme_tasks", "Domme Tasks"),
                            ("punishment_tasks", "Punishment Tasks"),
                            ("work_tasks", "Work/Study Tasks"),
                            ("self_care_tasks", "Self Care Tasks"),
                            ("chore_tasks", "Chore Tasks"),
                            ("personal_tasks", "Personal Tasks"),
                        ],
                        default="sissification_tasks",
                        max_length=50,
                    ),
                ),
                (
                    "difficulty",
                    models.CharField(
                        choices=[
                            ("easy", "Easy Peasy 💖"),
                            ("moderate", "Glamorous Effort ✨"),
                            ("hard", "Ultimate Sissy Challenge 💪"),
                        ],
                        default="moderate",
                        max_length=20,
                    ),
                ),
                (
                    "start_date",
                    models.DateField(default=django.utils.timezone.localdate),
                ),
                ("end_date", models.DateField(blank=True, null=True)),
                (
                    "frequency",
                    models.CharField(
                        choices=[
                            ("daily", "Daily"),
                            ("weekly", "Weekly"),
                            ("monthly", "Monthly"),
                            ("yearly", "Yearly"),
                        ],
                        default="daily",
                        max_length=10,
                    ),
                ),
                ("target_count", models.PositiveIntegerField(default=8)),
                ("increment_counter", models.PositiveIntegerField(default=0)),
                ("last_reset_date", models.DateField(blank=True, null=True)),
                ("longest_streak_days", models.PositiveIntegerField(default=0)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-timestamp"],
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "receiver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="received_messages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_messages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Moderator",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("content", models.TextField()),
                ("is_read", models.BooleanField(default=False)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("tags", models.ManyToManyField(blank=True, to="journal.tag")),
            ],
        ),
        migrations.CreateModel(
            name="RelatedModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("object_id", models.PositiveIntegerField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Report",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("object_id", models.PositiveIntegerField()),
                ("reason", models.TextField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "reported_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ResourceCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                (
                    "resources",
                    models.ManyToManyField(
                        related_name="categories", to="journal.resource"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ResourceComment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "resource",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="journal.resource",
                    ),
                ),
            ],
            options={
                "ordering": ["-timestamp"],
            },
        ),
        migrations.CreateModel(
            name="Streak",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date", models.DateField(default=datetime.date.today)),
                ("end_date", models.DateField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="streaks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="JournalEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("content", models.TextField()),
                ("prompt_text", models.TextField(blank=True, null=True)),
                ("insight", models.TextField(blank=True, null=True)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="images/"),
                ),
                ("video", models.FileField(blank=True, null=True, upload_to="videos/")),
                ("audio", models.FileField(blank=True, null=True, upload_to="audios/")),
                ("file", models.FileField(blank=True, null=True, upload_to="files/")),
                ("polarity", models.FloatField(blank=True, null=True)),
                ("subjectivity", models.FloatField(blank=True, null=True)),
                ("sentiment", models.CharField(blank=True, max_length=20, null=True)),
                ("task", models.TextField(blank=True, null=True)),
                ("points", models.IntegerField(default=0)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entries",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("tags", models.ManyToManyField(blank=True, to="journal.tag")),
            ],
        ),
        migrations.CreateModel(
            name="Answer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("answer", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "professional",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "question",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="journal.question",
                    ),
                ),
                ("tags", models.ManyToManyField(blank=True, to="journal.tag")),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                ("description", models.TextField(blank=True, null=True)),
                ("points_awarded", models.IntegerField(default=10)),
                ("points_penalty", models.IntegerField(default=20)),
                ("completed", models.BooleanField(default=False)),
                (
                    "task_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TaskCompletion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("completed_at", models.DateTimeField(auto_now_add=True)),
                (
                    "journal_entry",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="journal.journalentry",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="journal.task"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=200)),
                ("content", models.TextField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "thread",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="journal.thread"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ToDo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("task", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                ("priority", models.IntegerField(default=1)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("Domme", "Domme Task"),
                            ("Sissy", "Sissy Task"),
                            ("Punishment", "Punishment Task"),
                            ("work", "Work/Study Task"),
                            ("self_care", "Self Care Task"),
                            ("chore", "Chore Task"),
                            ("personal", "Personal Task"),
                        ],
                        default="personal",
                        max_length=50,
                    ),
                ),
                (
                    "reward",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("praise", "Praise"),
                            ("points", "Points"),
                            ("gift", "Gift"),
                            ("privilege", "Privilege"),
                            ("none", "None"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "penalty",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("ignore", "Ignore"),
                            ("punishment", "Punishment"),
                            ("task", "Task"),
                            ("points_loss", "Lose Points"),
                            ("none", "None"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "due_date",
                    models.DateField(
                        default=journal.models.default_due_date, null=True
                    ),
                ),
                ("completed", models.BooleanField(default=False)),
                (
                    "timestamp",
                    models.DateTimeField(default=journal.models.current_timestamp),
                ),
                ("processed", models.BooleanField(default=False)),
                ("failed", models.BooleanField(default=False)),
                ("penalty_issued", models.BooleanField(default=False)),
                ("reward_issued", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserFeedback",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "privacy_level",
                    models.CharField(
                        choices=[
                            ("public", "Public Darling 💋"),
                            ("friends", "Just for Friends 🎀"),
                            ("private", "My Secret 🤫"),
                        ],
                        default="public",
                        max_length=10,
                    ),
                ),
                (
                    "nsfw_blur",
                    models.BooleanField(
                        default=False, verbose_name="Blur NSFW Content 🙈"
                    ),
                ),
                (
                    "insight_opt",
                    models.BooleanField(
                        default=False, verbose_name="Ai Insight Opt In"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserTheme",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("color", models.CharField(max_length=50)),
                ("layout", models.CharField(max_length=50)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
