from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
import random
from journal.models import Task

TASKS = [
        {"description": "Write a positive affirmation about yourself. Then stick it to your Dashboard.", "points": 5},
        {"description":
            "Plan a cute outfit for the day and share it in your journal. Extra points for pics (use the Task tag if you wanna collect points!)", "points": 10},
        {"description":
            "Complete a short mindfulness or meditation exercise. Then write about how it made you feel, where you found it, and whether or not you'll do it again (use the Task tag if you wanna collect points!)", "points": 8},
        {"description":
            "Give a compliment to someone and write about the experience. Either in your journal or in a forum post (use the Task tag if you wanna collect points!)", "points": 7},
        {"description":
            "Learn a new makeup technique or hairstyle and document the process. Share your results in your journal (use the Task tag if you wanna collect points!)", "points": 12},
        {"description":
            "Do a sissy-themed workout or yoga session. Then write about how it made you feel, where you found it, and whether or not you'll do it again (use the Task tag if you wanna collect points!)", "points": 15},
        {"description":
            "Pamper yourself with a self-care routine and share your experience in the forum (use the Task tag if you wanna collect points!)", "points": 10},
        {"description": "Write a short story or poem about your sissy journey. Don't use your real name or any identifying information. Be original! Write in your journal with the Task tag to collect your points.", "points": 12},
        {"description": "Comment on three other users' forum posts. Make sure you're kind and use the Task tag.", "points": 6},
        {"description": "Write a journal entry on why Pink is such a great color. Don't forget the Task tag.", "points": 5},
        {"description": "Find 5 hot pics of guys and explain why each of them is so attractive to you. Upload their pics to your journal with the Task tag.", "points": 8},
        # Duplicate task removed
        {"description":
            "Practice your sissy walk and write about how it makes you feel. Extra points for video evidence (use the Task tag if you wanna collect points!)", "points": 20},
        {"description":
            "Promote the Pink Book on social media and write about the experience (you don't have to use your personal account but remember to tag us!)", "points": 12},
        # More tasks can be added with varying points
        {"description":
            "Write a journal entry about your favorite sissy outfit, extra points if you upload a pic of it! More points if you post a pic in our forum of you wearing it (use the Task tag if you wanna collect points!)", "points": 15},
        {"description":
            "Practice your sissy walk and write about how it makes you feel. Extra points for video evidence (use the Task tag if you wanna collect points!)", "points": 20},
        {"description": "Reflect on the pain and pleasure intertwined in your sissy journey.", "points": 10},
        {"description": "Record a heartfelt confession of your love and devotion to me, your Mistress.", "points": 10},
        {"description": "Describe the moment you realized your deepest, most secret desires were to serve powerful alphas.", "points": 10},
        {"description": "Document an instance where your submission to me brought you to tears, whether from joy or despair.", "points": 10},
        {"description": "Write about the first time you felt truly owned and how it changed you.", "points": 10},
        {"description": "Detail an encounter with someone who does not understand or accept your sissy nature and the emotional impact it had on you.", "points": 10},
        {"description": "Write about the euphoria that follows a successful submission.", "points": 10},
        {"description": "Express how your submission has changed your relationship with fear and vulnerability.", "points": 10},
        {"description": "Reflect on the first time you felt truly accepted and validated in your sissy identity.", "points": 10},
        {"description": "Detail an encounter with someone who does not understand or accept your sissy nature and the emotional impact it had on you.", "points": 10},
        {"description": "Record a moment of intense arousal during a particularly humiliating task.", "points": 10},
        {"description": "Write about the euphoria that follows a successful submission.", "points": 10},
        {"description": "Explore a time when your emotions conflicted with your desire to obey.", "points": 10},
        {"description": "Express how your submission has changed your relationship with fear and vulnerability.", "points": 10},
    ]


TRUTH_TASKS = [
        {"description":
            "Confess your most embarrassing secret as a sissy. Write about how it felt to admit it (use the Task tag to collect points!).", "points": 15},
        {"description":
            "Write a journal entry about the moment you felt the most vulnerable in your sissy journey. Share why it impacted you so deeply (Task tag required).", "points": 12},
        {"description": "Reflect on a time when you struggled to accept yourself. What helped you overcome it? Write your story in your journal.", "points": 10},
        {"description": "Describe your ultimate dream of sissy life. Be as detailed and imaginative as possible. Don’t hold back!", "points": 20},
        {"description": "Admit to a time when you hesitated or faltered in your submission. Why did it happen, and what did you learn?", "points": 10},
        {"description": "Write about a moment when you felt the most proud of your sissy progress. What made it so special?", "points": 8},
        {"description":
            "Share a confession about something you’ve been too shy to admit, even to yourself. Write it in your journal (use the Task tag!).", "points": 18},
        {"description": "Reveal the most daring thought or fantasy you've ever had about your sissy identity. Be brave and write it down.", "points": 15},
        {"description": "What’s your biggest fear about being a sissy? Write a journal entry exploring this fear and how you might overcome it.", "points": 12},
        {"description": "Detail the most fulfilling moment you've experienced as a sissy. Why did it mean so much to you?", "points": 10},
        {"description": "Write about a time when you felt judged for your sissy nature. How did you cope, and what would you do differently now?", "points": 12},
        {"description": "Confess your deepest desire for self-improvement as a sissy. What steps will you take to achieve it?", "points": 10},
        {"description": "Be brutally honest: What’s one aspect of sissyhood that you still struggle with? Reflect on why and how you can grow.", "points": 15},
        {"description": "Describe your happiest memory related to your sissy identity. What made it so joyous, and how can you recreate it?", "points": 10},
        {"description": "Admit something you’ve never told anyone about your sissy journey. Write it down and reflect on how it feels to share.", "points": 20},
        {"description": "Reveal a moment when you felt conflicted about your desires. What caused the conflict, and how did you resolve it?", "points": 12},
        {"description": "Write a letter to your younger self about your sissy journey. What would you say to comfort or encourage them?", "points": 15},
        {"description": "Confess your guilty pleasure as a sissy. Why does it make you feel guilty, and how can you embrace it instead?", "points": 8},
        {"description": "Be honest about a time when you felt jealous of another sissy. What triggered it, and how can you use that to inspire growth?", "points": 10},
        {"description": "Reflect on the first time you felt like a true sissy. What were you doing, and how did it change your perspective?", "points": 15},
        {"description": "Share your most empowering moment as a sissy. How did it impact your confidence and outlook?", "points": 12},
        {"description": "Write about a time when your sissy identity helped you connect with someone in a meaningful way. How did it feel?", "points": 10},
        {"description": "Confess the wildest sissy goal you’ve ever considered. What’s holding you back from pursuing it?", "points": 18},
        {"description":
            "Be honest about what makes you feel the most beautiful as a sissy. Share your thoughts in a journal entry (use the Task tag!).", "points": 8},
        {"description": "Reveal the most vulnerable thing you’ve ever done as a sissy. How did it shape your journey?", "points": 15},
        {"description": "Reflect on a compliment you've received about your sissy journey. What was said, and why did it stand out to you?", "points": 8},
        {"description": "Admit a time when you felt conflicted about sharing your sissy side. How did you navigate the situation?", "points": 12},
        {"description": "Write about your ultimate sissy role model. What about them inspires you, and how can you embody those traits?", "points": 10},
        {"description": "Confess a secret desire related to your sissy identity. Be bold and put it into words!", "points": 20},
    ]


def generate_task(user):
    """Generate a random task for a user."""
    task_data = random.choice(TASKS)
    return Task.objects.create(
        user=user,
        description=task_data["description"],
        points_awarded=task_data["points"],
        points_penalty=calculate_penalty(task_data["points"]),
    )


def generate_truth_task(user):
    """Generate a random truth task for a user."""
    task_data = random.choice(TRUTH_TASKS)
    return Task.objects.create(
        user=user,
        description=task_data["description"],
        points_awarded=task_data["points"],
        points_penalty=calculate_penalty(task_data["points"]),
    )


def calculate_penalty(points):
    """Calculate the penalty for a task."""
    return -(points * 2)


def send_activation_email(user, request):
    """Send account activation email to a user."""
    current_site = request.get_host()
    subject = 'Activate Your Account'
    message = render_to_string('activation_email.html', {
        'user': user,
        'domain': current_site,
        'protocol': 'https' if request.is_secure() else 'http',
        'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


def fail_task(user):
    """Handle task failure for a user."""
    user.award_points(-5)
    return True


def complete_journal_entry(user, entry):
    """Mark a journal entry as completed and award points."""
    if not entry.completed:
        entry.completed = True
        entry.save()
        user.award_points(10)
        return True
    else:
        penalty = calculate_penalty(25)
        user.award_points(penalty)
    return False
