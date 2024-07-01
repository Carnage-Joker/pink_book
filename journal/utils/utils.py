# In journal/utils.py or a similar utilities file
import random


def generate_task():
    tasks = [
        "Write a positive affirmation about yourself.",
        "Plan a cute outfit for the day and share it in your journal.",
        "Complete a short mindfulness or meditation exercise.",
        "Give a compliment to someone and write about the experience.",
        "Learn a new makeup technique or hairstyle and document the process.",
        "Do a sissy-themed workout or yoga session.",
        "Pamper yourself with a self-care routine and share your experience.",
        "Write a short story or poem about your sissy journey.",
        "Comment on three other users' journal entries."
    ]
    return random.choice(tasks)
