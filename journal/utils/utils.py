# In journal/utils.py or a similar utilities file
import random


def generate_task():
    tasks = [
        "Write a positive affirmation about yourself. Then stick it to your Dashboard.",
        "Plan a cute outfit for the day and share it in your journal. Extra points for pics(use the Task tag if you wanna collect points!)",
        "Complete a short mindfulness or meditation exercise.Then write about how it made you feel, where you found it and whether or not you'll do it again(use the Task tag if you wanna collect points!)",
        "Give a compliment to someone and write about the experience. Either in your journal or in a forum post.(use the Task tag if you wanna collect points!)",
        "Learn a new makeup technique or hairstyle and document the process. Share your results in your journal(use the Task tag if you wanna collect points!)",
        "Do a sissy-themed workout or yoga session.Then write about how it made you feel, where you found it and whether or not you'll do it again(use the Task tag if you wanna collect points!)",
        "Pamper yourself with a self-care routine and share your experience in the forum(use the Task tag if you wanna collect points!)",
        "Write a short story or poem about your sissy journey. Don't use your real name or any identifying information. Lets be original girls! write in your journaL with the task tag to collect your points",
        "Comment on three other users' forum posts make sure your kind and use the Task tag.",
        "Write a journal entry on why Pink is such a great colour. Don't forget the Task tag",
        "Find 5 hot pics of guys and explain why each of them is so attractive to you. Upload their pics to your journal with the Task tag",
        "Write a journal entry about your favourite sissy outfit, extra points if you upload a pic of it! More points if you post a pic in our forum of you wearing it(use the Task tag if you wanna collect points!)",
        "Practise your sissy walk and write about how it makes you feel Extra points for video evidence(use the Task tag if you wanna collect points!)",
        "Promote the Pink Book on social media and write about the experience(you don't have to use your personal account but remember to tag us!)",
        
    ]
    task_id = random.randint(1, 100)
    if task_id % 2 == 0:
        tasks.append("Write a journal entry about your favourite sissy outfit")
    else:
        tasks.append("Practise your sissy walk and write about how it makes you feel")
    return random.choice(tasks)
