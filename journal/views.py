from .utils import (
    get_average_sentiment, extract_keywords, get_most_common_tags,
    get_most_common_emotions, get_average_word_count, get_current_streak,
    get_peak_journaling_time
)
from .models import CustomUser, JournalEntry, ToDo, Habit, Quote
from django.views.generic import TemplateView
from .models import ResourceCategory, Guide
from django.views.generic import DetailView
from django.core.paginator import Paginator
import json
import logging
import random
from datetime import date

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView as AuthLoginView
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.timezone import now
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)

from .forms import (CommentForm, CustomUserCreationForm, CustomUserLoginForm,
                    CustomUserUpdateForm, HabitForm, JournalEntryForm,
                    ProfileSettingsForm, ResendActivationForm, ThemeForm,
                    ToDoForm)
from .generate import generate_insight, generate_prompt
from .models import (ActivityLog, Answer, Billing, BlogPost, Comment,
                     CustomUser, Faq, Guide, Habit, JournalEntry, Message,
                     Post, Question, Quote, Resource, ResourceCategory, Task,
                     TaskCompletion, Thread, ToDo)
from .utils.ai_utils import (extract_keywords, get_average_sentiment,
                             get_average_word_count, get_current_streak,
                             get_most_common_emotions, get_most_common_tags,
                             get_peak_journaling_time)
from .utils.utils import generate_task, send_activation_email

logger = logging.getLogger(__name__)


User = get_user_model()


class SafeMixin:
    """Mixin to add error handling and logging."""

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__}: {str(e)}")
            messages.error(
                request, "An unexpected error occurred. Please try again later.")
            return redirect('journal:dashboard')


class RegisterView(View):
    model = CustomUser
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('journal:login')
    # redirect_authenticated_user = True
    # extra_context = {'title': 'Register'}
    # success_message = "Your account was created successfully. Please check your email to activate your account."
    # failure_message = "There was an error creating your account. Please try again."

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_activation_email(user, request)
            return redirect('journal:activation_sent')
        return render(request, 'register.html', {'form': form})


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('journal:registration_success')
        else:
            return render(
                request, 
                'activation_invalid.html'
            )


class ResendActivationView(FormView):
    template_name = 'resend_activation.html'
    form_class = ResendActivationForm
    success_url = reverse_lazy('journal:activation_sent')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = CustomUser.objects.filter(email=email, is_active=False).first()
        if user:
            send_activation_email(user, self.request)
        return super().form_valid(form)


def activation_sent(request):
    return render(request, 'activation_sent.html')


class RegistrationSuccessView(TemplateView):
    template_name = 'registration_success.html'

    def send_welcome_email(self, user):
        subject = "Welcome to the Sissy Journal!"
        message = f"Hi {CustomUser.sissy_name},\n\n" \
                  "Welcome to The Pink Book! We're so excited to have you join our community. " \
                  "You're one step closer to becoming the best sissy you can be.\n\n" \
                  "If you have any questions or need help getting started, feel free to reach out to us. " \
                  "We're here to support you on your journey.\n\n" \
                  "Best wishes,\n" \
                  "The Pink Team"
        user.email_user(subject, message)

    def get(self, request):
        messages.success(request, "Your account was activated successfully. Welcome to the community sis.")
        return redirect('journal:login')


class AboutView(TemplateView):
    template_name = "about.html"


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = "blog_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_posts'] = BlogPost.objects.filter(
            published=True).exclude(id=self.object.id).order_by('-timestamp')[:5]
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.content_object = self.object
            comment.user = request.user
            comment.save()
            return self.render_to_response(context=context)
        context['comment_form'] = comment_form
        return self.render_to_response(context=context)


class BlogListView(ListView):
    template_name = "blog_list.html"
    model = BlogPost
    context_object_name = "blog_posts"
    paginate_by = 5

    def get_queryset(self):
        return BlogPost.objects.filter(published=True).order_by("-timestamp")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_posts'] = BlogPost.objects.filter(
            published=True).order_by('-timestamp')[:5]
        return context


def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog.html', {'post': post})


class CustomLoginView(AuthLoginView, SafeMixin):
    template_name = "welcome.html"
    authentication_form = CustomUserLoginForm
    success_url = reverse_lazy("journal:dashboard")

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        logger.info(f"User {CustomUser.sissy_name} (ID: {CustomUser.email}) logged in successfully.")
        messages.success(self.request, "You have successfully logged in.")
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning(f"Failed login attempt with errors: {form.errors}")
        messages.error(
            self.request, "Login failed. Please check your sissy name and password.")
        return super().form_invalid(form)
# Set up the logger


logger = logging.getLogger(__name__)


class CustomLogoutView(auth_views.LogoutView):
    model = CustomUser
    template_name = "logout.html"
    next_page = reverse_lazy("journal:welcome")
    redirect_field_name = "next"

    def get_next_page(self):
        next_page = super().get_next_page()
        if next_page:
            return next_page
        return self.next_page

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            logger.info(f"User {CustomUser.sissy_name} (ID: {
                        CustomUser.email}) is logging out.")
            messages.success(request, "You have successfully logged out.")
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, "You are not logged in.")
            return redirect('journal:welcome')


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


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'profile.html'

    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView, SafeMixin):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'profile_update.html'
    success_url = reverse_lazy('journal:dashboard')

    def get_object(self):
        return self.request.user


class ProfileCustomizeView(LoginRequiredMixin, SafeMixin, UpdateView):
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


class HomeView(TemplateView, SafeMixin):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ResourceCategory.objects.all()
        return context


class ProfileSettingsView(LoginRequiredMixin, TemplateView):
    form_class = ProfileSettingsForm
    template_name = "profile_settings.html"
    model = CustomUser


class ModeratorListView(LoginRequiredMixin, ListView):
    model = Thread
    template_name = "moderators.html"
    context_object_name = 'threads'

    def get_queryset(self):
        self = self.request.user
        if self.is_staff:
            return Thread.objects.all() # Return all threads if user is staff
        elif self.is_moderator:
            return Thread.objects.filter(moderators=self) # Return threads where user is a moderator
        else:
            return Thread.objects.none() # Return no threads if user is not staff or moderator


class ThreadListView(ListView):
    model = Thread
    template_name = 'thread_list.html'
    context_object_name = 'threads'


class FeatureListView(ListView):
    # this is for the welcome page to display the different features of the website to draw in subscribers
    template_name = "feature_list.html"
    context_object_name = 'features'


class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(thread=self.kwargs['thread_id'])


class ForumPostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = 'post'


class ForumCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "create_post.html"
    fields = ["title", "content", "thread"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ForumDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("journal:thread_list")

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user) | self.model.objects.filter(author__is_staff=True)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = "create_comment.html"
    fields = ["content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.content_object = self.get_content_object()
        return super().form_valid(form)

    def get_content_object(self):
        raise NotImplementedError("Define how to get content_object here")


class HabitListView(LoginRequiredMixin, ListView):
    model = Habit
    template_name = "habit_list.html"
    paginate_by = 10

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitCreateView(LoginRequiredMixin, CreateView):
    model = Habit
    template_name = 'habit_form.html'
    form_class = HabitForm
    success_url = reverse_lazy('journal:dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class HabitUpdateView(LoginRequiredMixin, UpdateView):
    model = Habit
    template_name = "habit_form.html"
    form_class = HabitForm
    success_url = reverse_lazy('journal:dashboard')


class HabitDetailView(LoginRequiredMixin, DetailView):
    model = Habit
    template_name = "habit_detail.html"

    def increment_habit_counter(request, pk):
        habit = get_object_or_404(Habit, pk=pk)
        habit.increment_count()
        return redirect('journal:habit_detail', pk=pk)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        habit = context['object']
        context['current_streak'] = habit.get_current_streak()
        context['longest_streak'] = habit.get_longest_streak()
        return context


class IncrementHabitCounter(View):
    def post(self, request, pk):
        habit = get_object_or_404(Habit, pk=pk, user=request.user)
        habit.increment_count()
        insight = habit.get_insights()
        return JsonResponse({'status': 'success', 'new_count': habit.increment_counter, 'insight': insight})


@csrf_exempt
def generate_task_view(request):
    if request.method == 'POST':  # Ensure it matches the method in your view
        try:
            task = generate_task()
            return JsonResponse({'task': task})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def fail_task_view(request):
    if request.method == 'POST':
        user = request.user
        penalty_type = request.POST.get('penaltyType')
        points_to_deduct = int(request.POST.get('pointsToDeduct', 0))
        content_name = request.POST.get('contentName', '')

        if penalty_type == 'LOCK_CONTENT' and content_name:
            user.lock_content(content_name)
            message = f"{user.sissy_name} has failed the task. Content '{
                content_name}' is now locked."
        elif penalty_type == 'DEDUCT_POINTS':
            user.deduct_points(points_to_deduct)
            message = f"{user.sissy_name} has failed the task. {
                points_to_deduct} points have been deducted."
        else:
            message = "Invalid penalty type."

        return JsonResponse({'message': message})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


class CompleteToDoView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            todo_id = data.get('todo_id')
            todo = ToDo.objects.get(id=todo_id, user=request.user)
            todo.completed = True
            todo.save()
            return JsonResponse({'status': 'success'})
        except ToDo.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'ToDo does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


logger = logging.getLogger(__name__)


def privacy_policy(request):
    return HttpResponse("<h1>Privacy Policy</h1><p>This is a placeholder for the privacy policy.</p>")


def terms_of_service(request):
    return HttpResponse("<h1>Terms of Service</h1><p>This is a placeholder for the terms of service.</p>")


class CompleteTaskView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            task_id = data.get('task_id')
            task = Task.objects.get(id=task_id)

            if not TaskCompletion.objects.filter(user=request.user, task=task).exists():
                # Redirect to the journal entry form with the task details
                return redirect('journal:new_entry', task_id=task_id)
            else:
                return JsonResponse({'status': 'error', 'message': 'Task already completed'}, status=400)
        except Task.DoesNotExist:
            logger.error(f"Task with ID {task_id} does not exist.")
            return JsonResponse({'status': 'error', 'message': 'Task does not exist'}, status=404)
        except Exception as e:
            logger.error(f"Error completing task: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


class ToDoCreateView(LoginRequiredMixin, CreateView):
    model = ToDo
    form_class = ToDoForm
    template_name = 'create_todo.html'
    success_url = reverse_lazy('journal:dashboard')

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
    success_url = reverse_lazy('journal:dashboard')


class ToDoListView(LoginRequiredMixin, ListView):
    model = ToDo
    template_name = "todo_list.html"

    def get_queryset(self):
        completed = self.request.GET.get('completed', None)
        queryset = ToDo.objects.filter(user=self.request.user)
        if completed is not None:
            queryset = queryset.filter(completed=completed)
        return queryset


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

        # Save the journal entry
        journal_entry.save()

        # Save tags
        form.save_m2m()

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
        return context


class JournalEntryListView(LoginRequiredMixin, ListView):
    model = JournalEntry
    template_name = "entry_list.html"
    context_object_name = 'page_obj'
    paginate_by = 10  # Adjust as needed

    def get_queryset(self):
        user = self.request.user
        return JournalEntry.objects.filter(user=user)


class JournalEntryUpdateView(LoginRequiredMixin, UpdateView):
    model = JournalEntry
    template_name = "entry_update.html"
    form_class = JournalEntryForm
    success_url = reverse_lazy('journal:entry_list')

    def get_queryset(self):
        # Ensure that the user can only update their own entries
        return JournalEntry.objects.filter(user=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        ActivityLog.objects.create(user=self.request.user,
                                   action=f"Updated a journal entry: {form.instance.content[:20]}...")
        return response


class JournalEntryDeleteView(LoginRequiredMixin, DeleteView):
    model = JournalEntry
    template_name = "entry_delete.html"
    success_url = reverse_lazy('journal:entry_list')

    def get_queryset(self):
        # Ensure that the user can only delete their own entries
        return JournalEntry.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        # Get the object before it's deleted to log the action
        journal_entry = self.get_object()
        response = super().delete(request, *args, **kwargs)
        # Log the deletion action
        ActivityLog.objects.create(user=self.request.user,
                                   action=f"Deleted a journal entry: {journal_entry.title}")
        return response


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_quote_of_the_day(self):
        today = date.today()
        quotes = Quote.objects.all()
        if quotes.exists():
            random.seed(today.toordinal())
            quote = random.choice(quotes)
            return quote.content
        return "No quote available"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        try:
            # Fetch recent journal entries, todos, and habits
            recent_entries = JournalEntry.objects.filter(
                user=user).order_by('-timestamp')[:3]
            todos = ToDo.objects.filter(user=user).order_by('-timestamp')[:5]
            habits = Habit.objects.filter(user=user).order_by('-timestamp')[:5]

            # Process overdue todos
            for todo in todos:
                if now().date() > todo.due_date and not todo.completed:
                    todo.processed = True
                    todo.save()

            # Calculate sentiment data
            sentiment_data = get_average_sentiment(
                JournalEntry.objects.filter(user=user))

            # Update context with all necessary data
            context.update({
                'user': user,
                'points': user.points,
                'quote_of_the_day': self.get_quote_of_the_day(),
                'todos': todos,
                'habits': habits,
                'recent_entries': recent_entries,
                'frequent_keywords': extract_keywords(recent_entries),
                'common_tags': get_most_common_tags(recent_entries),
                'most_common_emotions': get_most_common_emotions(recent_entries),
                'average_word_count': get_average_word_count(recent_entries),
                'current_streak_length': get_current_streak(recent_entries),
                'most_active_hour': get_peak_journaling_time(recent_entries),
                'entries_with_insights': [entry for entry in recent_entries if entry.insight],
                'sentiment_data': sentiment_data,
                'polarity': sentiment_data.get('avg_polarity', 0),
                'subjectivity': sentiment_data.get('avg_subjectivity', 0),
            })
        except Exception as e:
            # Log the error if needed, and provide user-friendly error messages
            context['error'] = "There was an issue loading your dashboard. Please try again later."
            # Optional: for development/debugging
            context['debug_error'] = str(e)

        return context


logger = logging.getLogger(__name__)


def guide_list(request):
    guides = Guide.objects.all()
    return render(request, 'journal/guide_list.html', {'guides': guides})


class GuideDetailView(DetailView):
    model = Guide
    template_name = "guide_detail.html"
    context_object_name = 'guide'




class ResourceListView(ListView):
    model = ResourceCategory
    template_name = "resource_category_detail.html"
    # Optional, for clarity in the template
    context_object_name = "resource_category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve all ResourceCategories
        context["journal_categories"] = ResourceCategory.objects.all()

        # Retrieve Guides, optionally filtering by the current ResourceCategory
        guides = Guide.objects.all()

        # Pagination
        paginator = Paginator(guides, 5)  # Show 5 guides per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context["journal_guides"] = page_obj
        context["is_paginated"] = page_obj.has_other_pages()
        context["paginator"] = paginator

        return context


class ResourceCategoryView(ListView):
    model = ResourceCategory  # The primary model for this view
    template_name = "resource_category_detail.html"
    paginate = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all ResourceCategories for display
        context["journal_categories"] = ResourceCategory.objects.all()

        # Get all Guides, or you can filter them if needed
        context["journal_guides"] = Guide.objects.all()

        return context


class ResourceDetailView(DetailView):
    model = Resource
    template_name = "resource_detail.html"


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['question']
    template_name = 'question_form.html'
    success_url = reverse_lazy('journal:qna_list')

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_subscriber:
            return HttpResponseForbidden("You must be a subscriber to ask a question.")
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        ActivityLog.objects.create(user=self.request.user,
                                   action=f"Asked a question: {form.instance.question}")
                                    
        return super().form_valid(form)


class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    fields = ['answer']
    template_name = 'answer_form.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_premium() and not self.request.user.is_moderator_or_admin():
            return HttpResponseForbidden("You must be a premium subscriber, moderator, or admin to answer questions.")
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.professional = self.request.user
        form.instance.question = get_object_or_404(
            Question, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('journal:qna_detail', kwargs={'pk': self.kwargs['pk']})


def qna_list(request):
    questions = Question.objects.all()
    return render(request, 'qna_list.html', {'questions': questions})


def qna_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = Answer.objects.filter(question=question)
    return render(request, 'qna_detail.html', {'question': question, 'answers': answers})


class ContactView(TemplateView):
    template_name = "contact_form.html"
    fields = ["name", "email", "subject", "message"]


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "messages.html"


# a log of the user's activity for admin purposes

class ActivityLogListView(LoginRequiredMixin, ListView):
    model = ActivityLog
    template_name = "activity_log.html"
    context_object_name = 'activity_logs'
    paginate_by = 10
    ordering = ['-timestamp']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_logs'] = ActivityLog.objects.order_by('-timestamp')[:5]
        return context

    def get_queryset(self):
        return ActivityLog.objects.all().order_by('-timestamp')


# a log of the user's activity for admin purposes


# need to get subscription billing working

class BillingView(LoginRequiredMixin, ListView):
    model = Billing
    template_name = "billing.html"
    context_object_name = 'billing'
    fields = ['user', 'subscription_tier', 'payment_method',
              'status', 'created_at', 'updated_at']
    success_url = reverse_lazy('journal:billing')
    paginate_by = 10
    ordering = ['-created_at']


# class NotificationListView(LoginRequiredMixin, ListView):
#    model = Notification
#    template_name = "notifications.html"

class FeedbackView(LoginRequiredMixin, TemplateView):
    template_name = "feedback.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feedback'] = "We'd love to hear your feedback!"
        return context


class FaqView(LoginRequiredMixin, TemplateView):
    template_name = "faqs.html"
    model = Faq

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faq'] = Faq.objects.all()
        return context
