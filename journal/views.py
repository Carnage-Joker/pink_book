import logging

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)

from .forms import (CustomUserCreationForm, CustomUserLoginForm,
                    CustomUserUpdateForm, JournalEntryForm,
                    ProfileSettingsForm, ResendActivationForm, ThemeForm,
                    ToDoForm)
from .generate import generate_insight, generate_prompt
from .models import (ActivityLog, Answer, Billing, Comment, CustomUser, Guide,
                     Habit, JournalEntry, Message, Post, Question, Quote,
                     Resource, ResourceCategory, Thread, ToDo)
from .utils.ai_utils import (extract_keywords, get_average_sentiment,
                             get_average_word_count, get_current_streak,
                             get_most_common_emotions, get_most_common_tags,
                             get_peak_journaling_time)
from .utils.utils import generate_task

User = get_user_model()


class ActivateAccountView(TemplateView):
    template_name = "activate_account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uidb64 = self.kwargs.get('uidb64')
        token = self.kwargs.get('token')

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            context['valid_link'] = True
        else:
            context['valid_link'] = False

        return context



class ResendActivationView(FormView):
    template_name = "resend_activation.html"
    form_class = ResendActivationForm
    success_url = reverse_lazy('journal:resend_activation_done')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                current_site = get_current_site(self.request)
                mail_subject = 'Activate your Sissy Diary account.'
                message = render_to_string('activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                send_mail(mail_subject, message,
                          'noreply@sissydiary.com', [user.email])
                messages.success(
                    self.request, 'A new activation link has been sent to your email.')
            else:
                messages.warning(
                    self.request, 'This account is already active.')
        except User.DoesNotExist:
            messages.error(
                self.request, 'No account found with this email address.')
        return super().form_valid(form)


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('journal:resend_activation')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)
        user.is_active = False  # Deactivate account until it is confirmed
        user.save()
        self.send_activation_email(user)
        return response

    def send_activation_email(self, user):
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your Sissy Diary account.'
        message = render_to_string('activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        send_mail(mail_subject, message, 'noreply@sissydiary.com', [user.email])



class AboutView(TemplateView):
    template_name = "about.html"


logger = logging.getLogger(__name__)


class CustomLoginView(AuthLoginView):
    template_name = "welcome.html"
    authentication_form = CustomUserLoginForm

    def form_valid(self, form):
        logger.info(
            f"User {form.get_user().sissy_name} logged in successfully.")
        messages.success(self.request, "You have successfully logged in.")
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning(f"Failed login attempt: {form.errors}")
        messages.error(
            self.request, "Login failed. Please check your sissy name and password.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('journal:dashboard')

class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy("journal:welcome")
#  Ensure this is correctly imported


class PasswordResetView(auth_views.PasswordResetView):
    template_name = "password_reset.html"
    email_template_name = "password_reset_email.html"
    subject_template_name = "password_reset_subject.txt"
    success_url = reverse_lazy("journal:password_reset_done")

    def form_valid(self, form):
        messages.success(
            self.request, "Password reset email sent successfully.")
        return super().form_valid(form)


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "password_reset_done.html"


@csrf_exempt
def fail_task_view(request):
    if request.method == 'POST':
        user = request.user
        # "LOCK_CONTENT" or "DEDUCT_POINTS"
        penalty_type = request.POST.get('penaltyType')
        points_to_deduct = int(request.POST.get('pointsToDeduct', 0))
        content_name = request.POST.get('contentName', '')

        if penalty_type == 'LOCK_CONTENT' and content_name:
            user.lock_content(content_name)
            message = f"{user.username} has failed the task. Content '{
                content_name}' is now locked."
        elif penalty_type == 'DEDUCT_POINTS':
            user.deduct_points(points_to_deduct)
            message = f"{user.username} has failed the task. {
                points_to_deduct} points have been deducted."
        else:
            message = "Invalid penalty type."

        return JsonResponse({'message': message})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


# In journal/views.py


def generate_task_view(request):
    task = generate_task()
    return JsonResponse({'task': task})
# In your journal/views.py


@csrf_exempt
def complete_todo_view(request, pk):
    if request.method == 'POST':
        try:
            todo = ToDo.objects.get(pk=pk, user=request.user)
            todo.completed = True
            todo.save()
            return JsonResponse({'success': True})
        except ToDo.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Todo item does not exist.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def complete_task_view(request):
    user_profile = request.user.userprofile
    user_profile.points += 10  # Award 10 points for completing a task
    user_profile.save()
    return JsonResponse({'message': 'Task completed! You earned 10 points.', 'points': user_profile.points})


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'profile.html'

    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'profile_update.html'
    success_url = reverse_lazy('journal:dashboard')

    def get_object(self, ):
        return self.request.user


class ProfileCustomizeView(LoginRequiredMixin, UpdateView):
    form_class = ThemeForm
    template_name = 'profile_customize.html'
    model = CustomUser
    success_url = reverse_lazy('journal:dashboard')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "OMG I love your new look!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Bad Sissy! Try again! ")
        return super().form_invalid(form)


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ResourceCategory.objects.all()
        return context


class ProfileSettingsView(LoginRequiredMixin, TemplateView):
    form_class = ProfileSettingsForm
    template_name = "profile_settings.html"
    model = CustomUser


class PostListView(ListView):
    model = Post
    template_name = "post_list.html"


class ForumPostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"


class ForumThreadListView(ListView):
    model = Thread
    template_name = "categories.html"


class ForumCreateView(CreateView):
    model = Post
    template_name = "create_post.html"
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ForumDeleteView(DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("journal:categories")


class ModeratorListView(LoginRequiredMixin, ListView):
    model = Thread
    template_name = "moderators.html"


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ["content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Habit Views


class HabitListView(LoginRequiredMixin, ListView):
    model = Habit
    template_name = "habit_list.html"
    paginate_by = 10  # Adjust the number of items per page as needed

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitCreateView(LoginRequiredMixin, CreateView):
    model = Habit
    template_name = 'habit_form.html'
    fields = ['name', 'description', 'start_date', 'end_date',
              'reward', 'penalty', 'reminder_frequency', 'category', 'progress']
    # Redirect to the habit list view after creation
    success_url = reverse_lazy('journal:dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class HabitUpdateView(LoginRequiredMixin, UpdateView):
    model = Habit
    template_name = "habit_form.html"
    fields = ["name", "description", "start_date", "end_date"]


class HabitDetailView(LoginRequiredMixin, DetailView):
    model = Habit
    template_name = "habit_detail.html"


class ToDoCreateView(LoginRequiredMixin, CreateView):
    model = ToDo
    form_class = ToDoForm
    template_name = 'create_todo.html'
    success_url = reverse_lazy('journal:todo_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ToDoDetailView(LoginRequiredMixin, DetailView):
    model = ToDo
    template_name = "todo_detail.html"


class ToDoUpdateView(LoginRequiredMixin, UpdateView):
    model = ToDo
    form_class = ToDoForm
    template_name = "todo_update.html"
    success_url = reverse_lazy('journal:todo_list')


class ToDoListView(LoginRequiredMixin, ListView):
    model = ToDo
    template_name = "todo_list.html"

    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_quote_of_the_day(self):
        quotes_count = Quote.objects.count()
        if quotes_count == 0:
            return None
        today = now().date()
        index = today.timetuple().tm_yday % quotes_count
        return Quote.objects.all()[index]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        recent_entries = JournalEntry.objects.filter(
            user=user).order_by('-timestamp')[:3]
        entries = JournalEntry.objects.filter(user=user).order_by('-timestamp')
        todos = ToDo.objects.filter(user=user).order_by('-timestamp')[:5]
        habits = Habit.objects.filter(user=user).order_by('-timestamp')[:5]
        for todo in todos:
            if todo.due_date and now().date() > todo.due_date and not todo.completed:
                todo.processed = True
                todo.save()
        sentiment_data = get_average_sentiment(entries)

        context.update({
            'user': user,
            'quote_of_the_day': self.get_quote_of_the_day(),
            'todos': todos,
            'habits': habits,
            'recent_entries': recent_entries,
            'entries': entries,
            'frequent_keywords': extract_keywords(entries),
            'common_tags': get_most_common_tags(entries),
            'most_common_emotions': get_most_common_emotions(entries),
            'average_word_count': get_average_word_count(entries),
            'current_streak_length': get_current_streak(entries),
            'most_active_hour': get_peak_journaling_time(entries),
            'entries_with_insights': [entry for entry in entries if entry.insight],
            'sentiment_data': sentiment_data,
            'polarity': sentiment_data['avg_polarity'],
            'subjectivity': sentiment_data['avg_subjectivity'],
        })

        return context


class JournalEntryCreateView(LoginRequiredMixin, CreateView):
    model = JournalEntry
    template_name = 'new_entry.html'
    form_class = JournalEntryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Generate a new prompt when the user accesses the new entry page
        context['generated_prompt'] = generate_prompt()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.prompt_text = self.get_context_data(
        )['generated_prompt']  # Save the generated prompt

        # Save the form but don't commit to the database yet
        journal_entry = form.save(commit=False)

        # Generate the insight for the journal entry content
        try:
            insight_text = generate_insight(journal_entry.content)
            journal_entry.insight = insight_text
        except Exception as e:
            messages.error(self.request, f"Error generating insight: {str(e)}")
            journal_entry.insight = "Insight generation failed."

        journal_entry.save()
        self.object = journal_entry

        messages.success(
            self.request, "Journal entry created successfully with insights.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('journal:entry_detail', kwargs={'pk': self.object.pk})


class JournalEntryDetailView(LoginRequiredMixin, DetailView):
    model = JournalEntry
    template_name = "entry_detail.html"
    context_object_name = 'entry'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entry = context['entry']
        # Pass the prompt to the context
        context['prompt_text'] = entry.prompt_text
        context['insight'] = entry.insight  # Pass the insight to the context
        context['comments'] = entry.comments.all()
        return context


class JournalEntryListView(LoginRequiredMixin, ListView):
    model = JournalEntry
    template_name = "entry_list.html"
    context_object_name = 'recent_entries'

    def get_queryset(self):
        user = self.request.user
        return JournalEntry.objects.filter(user=user)


class JournalEntryUpdateView(LoginRequiredMixin, UpdateView):
    model = JournalEntry
    template_name = 'new_entry.html'
    fields = ['title', 'content', 'tags', 'image', 'video', 'audio', 'file']


class JournalEntryDeleteView(LoginRequiredMixin, DeleteView):
    model = JournalEntry
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('journal:entry_list')


logger = logging.getLogger(__name__)


def guide_list(request):
    guides = Guide.objects.all()
    return render(request, 'guides/guide_list.html', {'guides': guides})


def guide_detail(request, pk):
    guide = get_object_or_404(Guide, pk=pk)
    return render(request, 'guides/guide_detail.html', {'guide': guide})


class ResourceListView(ListView):
    model = ResourceCategory
    template_name = "resources.html"


class ResourceCategoryView(DetailView):
    model = ResourceCategory
    template_name = "resource_category_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["journal_categories"] = ResourceCategory.objects.all()
        return context


class ResourceDetailView(DetailView):
    model = Resource
    template_name = "resource_detail.html"


# views.py
def qna_list(request):
    questions = Question.objects.all()
    return render(request, 'qna/qna_list.html', {'questions': questions})


def qna_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = Answer.objects.filter(question=question)
    return render(request, 'qna/qna_detail.html', {'question': question, 'answers': answers})


class ContactView(TemplateView):
    template_name = "contact_form.html"
    fields = ["name", "email", "subject", "message"]

# class NotificationListView(LoginRequiredMixin, ListView):
#    model = Notification
#    template_name = "notifications.html"


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "messages.html"


class ActivityLogListView(LoginRequiredMixin, ListView):
    model = ActivityLog
    template_name = "activity_log.html"


class BillingView(LoginRequiredMixin, ListView):
    model = Billing
    template_name = "billing.html"
