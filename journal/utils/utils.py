# In journal/utils.py or a similar utilities file
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
import random


def generate_task():
    tasks = [
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
        {"description":
            "Write a journal entry about your favorite sissy outfit, extra points if you upload a pic of it! More points if you post a pic in our forum of you wearing it (use the Task tag if you wanna collect points!)", "points": 15},
        {"description":
            "Practice your sissy walk and write about how it makes you feel. Extra points for video evidence (use the Task tag if you wanna collect points!)", "points": 20},
        {"description":
            "Promote the Pink Book on social media and write about the experience (you don't have to use your personal account but remember to tag us!)", "points": 12},
        # More tasks can be added with varying points
        {"description": "Write a journal entry about your favorite sissy outfit, extra points if you upload a pic of it! More points if you post a pic in our forum of you wearing it (use the Task tag if you wanna collect points!)", "points": 15},
        {"description": "Practice your sissy walk and write about how it makes you feel. Extra points for video evidence (use the Task tag if you wanna collect points!)", "points": 20},
        {"description": "Reflect on the pain and pleasure intertwined in your sissy journey.", "points": 10},
        {"description": "Record a heartfelt confession of your love and devotion to me, your Mistress.", "points": 10},
        {"description": "Describe the moment you realized your deepest, most secret desires were to serve powerful alphas.", "points": 10},
        {"description": "Document an instance where your submission to me brought you to tears, whether from joy or despair.", "points": 10},
        {"description": "Write about the first time you felt truly owned", "points": 10},
        {"description": "Reflect on the first time you felt truly accepted and validated in your sissy identity.", "points": 10},
        {"description": "Detail an encounter with someone who does not understand or accept your sissy nature and the emotional impact it had on you.", "points": 10},
        {"description": "Record a moment of intense arousal during a particularly humiliating task.", "points": 10},
        {"description": "Write about the euphoria that follows a successful submission.", "points": 10},
        {"description": "Explore a time when your emotions conflicted with your desire to obey.", "points": 10},         {"description": "Express how your submission has changed your relationship with fear and vulnerability.", "points": 10},
        {"description": "Write about the first time you felt truly owned", "points": 10},
        {"description": "Reflect on the first time you felt truly accepted and validated in your sissy identity.", "points": 10},
        {"description": "Detail an encounter with someone who does not understand or accept your sissy nature and the emotional impact it had on you.", "points": 10},
        {"description": "Record a moment of intense arousal during a particularly humiliating task.", "points": 10},
        {"description": "Write about the euphoria that follows a successful submission.", "points": 10},
        {"description": "Explore a time when your emotions conflicted with your desire to obey.", "points": 10},
        {"description": "Express how your submission has changed your relationship with fear and vulnerability.", "points": 10},
    ]
    task = random.choice(tasks)
    task_id = random.randint(1, 100)
    return task, task_id


def calculate_penalty(points):
    return -(points * 2)




def send_activation_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = request.build_absolute_uri(
        reverse('journal:activate_account',
                kwargs={'uidb64': uid, 'token': token})
    )
    subject = 'Activate Your Account'
    message = render_to_string('activation_email.html', {
        'user': user,
        'activation_link': activation_link,
    })
    send_mail(subject, message,
              'noreplyaccactivation@thepinkbook.com.au', [user.email])


def fail_task(user):
    user.award_points(-5)  # Adjust points as needed
    return True

def complete_journal_entry(user, entry):
    if not entry.completed:
        entry.completed = True
        entry.save()
        user.award_points(10)  # Adjust points as needed
        return True
    return False
