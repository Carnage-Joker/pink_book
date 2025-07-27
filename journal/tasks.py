from celery import shared_task
from django.utils import timezone
from openai import OpenAIError

from .models import JournalEntry
from .generate import generate_insight, check_content_topic_with_openai

MAX_RETRIES = 3
RETRY_DELAY = 60  # seconds


@shared_task(bind=True, max_retries=MAX_RETRIES, default_retry_delay=RETRY_DELAY)
def generate_insight_task(self, entry_id):
    try:
        entry = JournalEntry.objects.get(pk=entry_id)
        insight = generate_insight(entry.content)
        entry.insight = insight
        entry.insight_generated_at = timezone.now()
        entry.save(update_fields=['insight', 'insight_generated_at'])
    except OpenAIError as exc:
        raise self.retry(exc=exc)
    except Exception as exc:
        entry = JournalEntry.objects.get(pk=entry_id)
        entry.ai_generation_error = str(exc)
        entry.insight_generated_at = timezone.now()
        entry.save(update_fields=[
                   'ai_generation_error', 'insight_generated_at'])


@shared_task(bind=True, max_retries=MAX_RETRIES, default_retry_delay=RETRY_DELAY)
def check_topic_task(self, entry_id):
    try:
        entry = JournalEntry.objects.get(pk=entry_id)
        passed = check_content_topic_with_openai(
            entry.content, entry.prompt_text or '')
        entry.topic_check_passed = passed
        entry.topic_check_at = timezone.now()
        entry.save(update_fields=['topic_check_passed', 'topic_check_at'])
    except OpenAIError as exc:
        raise self.retry(exc=exc)
    except Exception as exc:
        entry = JournalEntry.objects.get(pk=entry_id)
        entry.ai_generation_error = str(exc)
        entry.topic_check_at = timezone.now()
        entry.save(update_fields=['ai_generation_error', 'topic_check_at'])
