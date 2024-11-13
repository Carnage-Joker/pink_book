# Standard library imports
from .models import Task
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import TemplateView, RedirectView
from django.views.generic import CreateView
from django.shortcuts import get_object_or_404
from .models import JournalEntry, Task
from .forms import JournalEntryForm
import json
import logging
import random
from datetime import date

# Django imports
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView as AuthLoginView
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import (HttpResponse, HttpResponseForbidden,
                         HttpResponseRedirect, JsonResponse)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.timezone import now
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)

# Local application imports
from .forms import (CommentForm, CustomUserCreationForm, CustomUserLoginForm,
                    CustomUserUpdateForm, HabitForm, JournalEntryForm,
                    ProfileSettingsForm, ResendActivationForm, ThemeForm,
                    ToDoForm)
from .models import (ActivityLog, Answer, Billing, BlogPost, Comment,
                     CustomUser, Faq, Guide, Habit, JournalEntry, Message,
                     Post, Question, Quote, Resource, ResourceCategory, Task,
                     TaskCompletion, Thread, ToDo)
from .generate import generate_insight, generate_prompt
from .utils.ai_utils import (extract_keywords, get_average_sentiment,
                             get_average_word_count, get_current_streak,
                             get_most_common_emotions, get_most_common_tags,
                             get_peak_journaling_time)
from .utils.utils import generate_task, send_activation_email, calculate_penalty


# Set up the logger
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
                request, "An unexpected error occurred. Please try again later."
            )
            return redirect("journal:dashboard")


# Authentication and User Management Views
class RegisterView(View):
    """View for user registration."""

    template_name = "register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("journal:welcome")
    extra_context = {"title": "Register"}
    success_message = (
        "Your account was created successfully. Please check your email to activate your account."
    )
    failure_message = "There was an error creating your account. Please try again."

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_activation_email(user, request)
            return redirect("journal:activation_sent")
        return render(request, self.template_name, {"form": form})


class ActivateAccountView(View):
    """View to activate user account via email link."""

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("journal:registration_success")
        else:
            return render(request, "activation_invalid.html")


class ResendActivationView(FormView):
    """View to resend account activation email."""

    template_name = "resend_activation.html"
    form_class = ResendActivationForm
    success_url = reverse_lazy("journal:activation_sent")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = CustomUser.objects.filter(email=email, is_active=False).first()
        if user:
            send_activation_email(user, self.request)
        return super().form_valid(form)


def activation_sent(request):
    """View to inform the user that activation email has been sent."""
    return render(request, "activation_sent.html")


class RegistrationSuccessView(TemplateView):
    """View displayed after successful registration and account activation."""

    template_name = "registration_success.html"

    def send_welcome_email(self, user):
        subject = "Welcome to the Journal!"
        message = (
            f"Hi {user.first_name},\n\n"
            "Welcome to our community! We're excited to have you join us.\n\n"
            "If you have any questions or need help getting started, feel free to reach out to us.\n\n"
            "Best wishes,\n"
            "The Team"
        )
        user.email_user(subject, message)

    def get(self, request):
        user = request.user
        self.send_welcome_email(user)
        messages.success(
            request,
            "Your account was activated successfully. Welcome to the community!",
        )
        return redirect("journal:welcome")


class CustomLoginView(AuthLoginView, SafeMixin):
    """Custom login view with additional logging and messaging."""

    template_name = "welcome.html"
    authentication_form = CustomUserLoginForm
    success_url = reverse_lazy("journal:dashboard")

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        # Use 'sissy_name' as the identifier
        logger.info(
            f"User {user.sissy_name} (Email: {
                user.email}) logged in successfully."
        )
        messages.success(self.request, "You have successfully logged in.")
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning(f"Failed login attempt with errors: {form.errors}")
        messages.error(
            self.request, "Login failed. Please check your sissy name and password."
        )
        return super().form_invalid(form)


class CustomLogoutView(auth_views.LogoutView):
    """Custom logout view with additional logging and messaging."""

    next_page = reverse_lazy("journal:welcome")
    redirect_field_name = "next"

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            logger.info(
                f"User {user.get_full_name()} (Email: {
                    user.email}) is logging out."
            )
            messages.success(request, "You have successfully logged out.")
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, "You are not logged in.")
            return redirect("journal:welcome")


class PasswordResetView(auth_views.PasswordResetView):
    """View for initiating a password reset."""

    template_name = "password_reset.html"
    email_template_name = "password_reset_email.html"
    subject_template_name = "password_reset_subject.txt"
    success_url = reverse_lazy("journal:password_reset_done")

    def form_valid(self, form):
        messages.success(
            self.request, "Password reset email sent successfully.")
        return super().form_valid(form)


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    """View displayed after a password reset email has been sent."""

    template_name = "password_reset_done.html"


class ProfileView(LoginRequiredMixin, DetailView):
    """View to display user profile."""

    model = CustomUser
    template_name = "profile.html"

    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView, SafeMixin):
    """View to update user profile."""

    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = "profile_update.html"
    success_url = reverse_lazy("journal:dashboard")

    def get_object(self):
        return self.request.user


class ProfileCustomizeView(LoginRequiredMixin, SafeMixin, UpdateView):
    """View to customize user profile theme."""

    form_class = ThemeForm
    template_name = "profile_customize.html"
    model = CustomUser
    success_url = reverse_lazy("journal:dashboard")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(
            self.request, "Your profile has been updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "An error occurred while updating your profile. Please try again."
        )
        return super().form_invalid(form)


class ProfileSettingsView(LoginRequiredMixin, TemplateView):
    """View for user profile settings."""

    template_name = "profile_settings.html"
    form_class = ProfileSettingsForm
    model = CustomUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(instance=self.request.user)
        return context


# Dashboard and Home Views
class DashboardView(LoginRequiredMixin, TemplateView):
    """User dashboard view displaying various statistics and recent activity."""

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
        profile = getattr(user, "profile", None)

        # Fetch recent data
        recent_entries = JournalEntry.objects.filter(
            user=user).order_by("-timestamp")[:3]
        todos = ToDo.objects.filter(user=user).order_by("-timestamp")[:5]
        habits = Habit.objects.filter(user=user).order_by("-timestamp")[:5]

        # Get the most recent task and check task_id
        task = Task.objects.filter(user=self.request.user).last()
        if task:
            context['task'] = task
            context['task_id'] = getattr(task, 'task_id', None)

        # Sentiment and journal insights
        if recent_entries.exists():
            sentiment_data = get_average_sentiment(recent_entries)
            context.update({
                "avg_polarity": sentiment_data.get("avg_polarity", 0),
                "avg_subjectivity": sentiment_data.get("avg_subjectivity", 0),
                "streak": get_current_streak(recent_entries),
                "frequent_keywords": extract_keywords(recent_entries),
                "common_tags": get_most_common_tags(recent_entries),
                "most_common_emotions": get_most_common_emotions(recent_entries),
                "average_word_count": get_average_word_count(recent_entries),
                "most_active_hour": get_peak_journaling_time(recent_entries),
            })
        else:
            context.update({
                "avg_polarity": 0,
                "avg_subjectivity": 0,
                "streak": 0,
                "frequent_keywords": [],
                "common_tags": [],
                "most_common_emotions": [],
                "average_word_count": 0,
                "most_active_hour": None,
            })

        # General context update
        context.update({
            "user": user,
            "profile": profile,
            "points": getattr(profile, "points", 0) if profile else 0,
            "quote_of_the_day": self.get_quote_of_the_day(),
            "todos": todos,
            "habits": habits,
            "entries": recent_entries,
            "entries_with_insights": recent_entries,
        })

        return context


class HomeView(TemplateView, SafeMixin):
    """Home page view."""

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ResourceCategory.objects.all()
        return context


# Journal Entry Views


class JournalEntryCreateView(LoginRequiredMixin, CreateView):
    """View to create a new journal entry."""

    model = JournalEntry
    template_name = "new_entry.html"
    form_class = JournalEntryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Only display the generated prompt for context, not to be stored here
        if "generated_prompt" not in context:
            context["generated_prompt"] = generate_prompt()

        return context

    def form_valid(self, form):
        # Assign the logged-in user to the form instance
        form.instance.user = self.request.user
        # Generate and save the prompt with the journal entry instance
        # Generate directly during form submission
        form.instance.prompt_text = generate_prompt()
        journal_entry = form.save(commit=False)

        # Generate and attach the insight for the journal entry content
        try:
            insight_text = generate_insight(journal_entry.content)
            journal_entry.insight = insight_text
        except Exception as e:
            messages.error(self.request, f"Error generating insight: {str(e)}")
            journal_entry.insight = "Insight generation failed."

        # Save the journal entry to the database
        journal_entry.save()
        form.save_m2m()

        # Award points to the user for creating a journal entry
        self.request.user.award_points(10)  # Adjust points as needed

        messages.success(
            self.request, "Journal entry created successfully with insights and points awarded."
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("journal:entry_detail", kwargs={"pk": self.object.pk})


class JournalEntryWithTaskView(LoginRequiredMixin, CreateView):
    """View for writing a journal entry with a generated task."""

    model = JournalEntry
    template_name = "new_entry_with_task.html"
    form_class = JournalEntryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_id = self.kwargs.get("task_id")
        if task_id:
            context["task"] = get_object_or_404(
                Task, pk=task_id, user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        task_id = self.kwargs.get("task_id")
        if task_id:
            task = get_object_or_404(Task, pk=task_id, user=self.request.user)
            form.instance.task = task
            # Using task description as a prompt
            form.instance.prompt_text = task.description

        journal_entry = form.save(commit=False)
        journal_entry.save()
        form.save_m2m()

        messages.success(self.request, "Journal entry created successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("journal:entry_detail", kwargs={"pk": self.object.pk})


class JournalEntryDetailView(LoginRequiredMixin, DetailView):
    """View to display a journal entry in detail."""

    model = JournalEntry
    template_name = "entry_detail.html"
    context_object_name = "entry"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entry = context["entry"]
        # These may already be accessible in the template as entry.prompt_text and entry.insight
        context["prompt_text"] = entry.prompt_text
        context["insight"] = entry.insight
        if entry.task:
            context["task"] = entry.task
        return context
    
    
class JournalEntryListView(LoginRequiredMixin, ListView):
    """View to list all journal entries of the user."""

    model = JournalEntry
    template_name = "entry_list.html"
    context_object_name = "entries"
    paginate_by = 10

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)


class JournalEntryUpdateView(LoginRequiredMixin, UpdateView):
    """View to update a journal entry."""

    model = JournalEntry
    template_name = "entry_update.html"
    form_class = JournalEntryForm
    success_url = reverse_lazy("journal:entry_list")

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        ActivityLog.objects.create(
            user=self.request.user,
            action=f"Updated a journal entry: {form.instance.content[:20]}...",
        )
        return response


class JournalEntryDeleteView(LoginRequiredMixin, DeleteView):
    """View to delete a journal entry."""

    model = JournalEntry
    template_name = "entry_delete.html"
    success_url = reverse_lazy("journal:entry_list")

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        journal_entry = self.get_object()
        ActivityLog.objects.create(
            user=request.user,
            action=f"Deleted a journal entry: {journal_entry.title}",
        )
        return super().delete(request, *args, **kwargs)


def redeem_points(request):
    user_points = UserPoints.objects.get(user=request.user)
    if request.method == "POST":
        points_to_redeem = int(request.POST.get("points", 0))
        if user_points.redeem_points(points_to_redeem):
            messages.success(request, f"Successfully redeemed {
                             points_to_redeem} points!")
        else:
            messages.error(request, "Insufficient points.")
        return redirect('redeem_points')

    return render(request, 'redeem_points.html', {'points': user_points.points})


class TaskGenerateView(LoginRequiredMixin, TemplateView):
    """View to generate a task for the user and redirect them to write about it."""

    template_name = "task_generate.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Generate a task and add it to the context
        task, task_id = generate_task()
        context["task"] = task
        context["task_id"] = task_id
        context["points_awarded"] = task["points"]
        context["points_penalty"] = calculate_penalty(task["points"])

        # Create and save the task in the database for the user to complete
        new_task = Task.objects.create(
            user=self.request.user,
            description=task["description"],
            points_awarded=task["points"],
            points_penalty=calculate_penalty(task["points"]),
            task_id=task_id
        )

        # Redirect the user to the new entry template to write about the task
        return redirect(reverse('journal:new_entry_with_task', kwargs={'task_id': new_task.pk}))



class HabitListView(LoginRequiredMixin, ListView):
    """View to list habits."""

    model = Habit
    template_name = "habit_list.html"
    paginate_by = 10

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitCreateView(LoginRequiredMixin, CreateView):
    """View to create a new habit."""

    model = Habit
    template_name = "habit_form.html"
    form_class = HabitForm
    success_url = reverse_lazy("journal:dashboard")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class HabitUpdateView(LoginRequiredMixin, UpdateView):
    """View to update an existing habit."""

    model = Habit
    template_name = "habit_form.html"
    form_class = HabitForm
    success_url = reverse_lazy("journal:dashboard")


class HabitDetailView(LoginRequiredMixin, DetailView):
    """View to display habit details."""

    model = Habit
    template_name = "habit_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        habit = context["habit"]
        context["current_streak"] = habit.get_current_streak()
        context["longest_streak"] = habit.get_longest_streak()
        return context


class IncrementHabitCounterView(LoginRequiredMixin, View):
    """View to increment habit counter via AJAX."""

    def post(self, request, pk):
        habit = get_object_or_404(Habit, pk=pk, user=request.user)
        habit.increment_count()
        current_streak = habit.get_current_streak()
        longest_streak = habit.get_longest_streak()

        return JsonResponse(
            {
                "status": "success",
                "new_count": habit.increment_counter,
                "current_streak": current_streak,
                "longest_streak": longest_streak,
            }
        )


# To-Do Management Views
class ToDoCreateView(LoginRequiredMixin, CreateView):
    """View to create a new to-do item."""

    model = ToDo
    form_class = ToDoForm
    template_name = "create_todo.html"
    success_url = reverse_lazy("journal:dashboard")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ToDoDetailView(LoginRequiredMixin, DetailView):
    """View to display to-do item details."""

    model = ToDo
    template_name = "todo_detail.html"


class ToDoUpdateView(LoginRequiredMixin, UpdateView):
    """View to update a to-do item."""

    model = ToDo
    form_class = ToDoForm
    template_name = "todo_update.html"
    success_url = reverse_lazy("journal:dashboard")


class ToDoListView(LoginRequiredMixin, ListView):
    """View to list to-do items."""

    model = ToDo
    template_name = "todo_list.html"

    def get_queryset(self):
        completed = self.request.GET.get("completed")
        queryset = ToDo.objects.filter(user=self.request.user)
        if completed is not None:
            queryset = queryset.filter(completed=completed)
        return queryset


class CompleteToDoView(View):
    """View to mark a to-do item as completed via AJAX."""

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            todo_id = data.get("todo_id")
            todo = ToDo.objects.get(id=todo_id, user=request.user)
            todo.completed = True
            todo.save()
            return JsonResponse({"status": "success"})
        except ToDo.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "ToDo does not exist"}, status=404
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)


# Task Views
@csrf_exempt
def generate_task_view(request):
    """View to generate a new task."""

    if request.method == "POST":
        try:
            task = generate_task()
            return JsonResponse({"task": task})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def fail_task_view(request):
    """View to handle task failure and apply penalties."""

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)
    user = request.user
    penalty_type = request.POST.get("penaltyType")
    points_to_deduct = int(request.POST.get("pointsToDeduct", 0))
    content_name = request.POST.get("contentName", "")

    if penalty_type == "LOCK_CONTENT" and content_name:
        user.lock_content(content_name)
        message = (
            f"{user.get_full_name()} has failed the task. Content '{
                content_name}' is now locked."
        )
    elif penalty_type == "DEDUCT_POINTS":
        user.deduct_points(points_to_deduct)
        message = (
            f"{user.get_full_name()} has failed the task. {
                points_to_deduct} points have been deducted."
        )
    else:
        message = "Invalid penalty type."

    return JsonResponse({"message": message})


class CompleteTaskView(View):
    """View to mark a task as completed."""

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            task_id = data.get("task_id")
            task = Task.objects.get(id=task_id)

            if not TaskCompletion.objects.filter(user=request.user, task=task).exists():
                return redirect("journal:new_entry", task_id=task_id)
            else:
                return JsonResponse(
                    {"status": "error", "message": "Task already completed"}, status=400
                )
        except Task.DoesNotExist:
            logger.error(f"Task with ID {task_id} does not exist.")
            return JsonResponse(
                {"status": "error", "message": "Task does not exist"}, status=404
            )
        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON format"}, status=400
            )
        except Exception as e:
            logger.error(f"Error completing task: {str(e)}")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)


# Forum and Blog Views
class BlogListView(ListView):
    """View to list blog posts."""

    template_name = "blog_list.html"
    model = BlogPost
    context_object_name = "blog_posts"
    paginate_by = 5

    def get_queryset(self):
        return BlogPost.objects.filter(published=True).order_by("-timestamp")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_posts"] = BlogPost.objects.filter(published=True).order_by(
            "-timestamp"
        )[:5]
        return context


class BlogDetailView(DetailView):
    """View to display blog post details."""

    model = BlogPost
    template_name = "blog_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_posts"] = BlogPost.objects.filter(published=True).exclude(
            id=self.object.id
        ).order_by("-timestamp")[:5]
        context["comment_form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.content_object = self.object
            comment.user = request.user
            comment.save()
            return redirect("journal:blog_detail", pk=self.object.pk)
        context = self.get_context_data()
        context["comment_form"] = comment_form
        return self.render_to_response(context=context)


class ThreadListView(ListView):
    """View to list forum threads."""
    model = Thread
    template_name = "thread_list.html"
    context_object_name = "threads"


class PostListView(ListView):
    """View to list posts within a thread."""
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        self.thread = get_object_or_404(Thread, id=self.kwargs["thread_id"])
        return Post.objects.filter(thread=self.thread)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["thread"] = self.thread
        return context


class ForumCreateView(LoginRequiredMixin, CreateView):
    """View to create a new forum post."""
    model = Post
    template_name = "create_post.html"
    fields = ["title", "content", "thread"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ForumPostDetailView(DetailView):
    """View to display a forum post in detail."""
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"


class CommentCreateView(LoginRequiredMixin, CreateView):
    """View to create a comment on a post."""

    model = Comment
    template_name = "create_comment.html"
    fields = ["content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.content_object = self.get_content_object()
        return super().form_valid(form)

    def get_content_object(self):
        post_id = self.kwargs.get("post_id")
        return get_object_or_404(Post, id=post_id)


# Guides and Resources Views
def guide_list(request):
    """View to list guides."""
    guides = Guide.objects.all()
    return render(request, "journal/guide_list.html", {"guides": guides})


class GuideDetailView(DetailView):
    """View to display guide details."""

    model = Guide
    template_name = "journal/guide_detail.html"
    context_object_name = "guide"


class ResourceListView(ListView):
    """View to list resource categories and guides."""

    model = ResourceCategory
    template_name = "journal/resources.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        guides = Guide.objects.all()
        paginator = Paginator(guides, 5)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["guides"] = page_obj
        return context


class ResourceCategoryView(DetailView):
    """View to display resources within a category."""

    model = ResourceCategory
    template_name = "journal/resource_category_detail.html"
    context_object_name = "category"


class ResourceDetailView(DetailView):
    """View to display resource details."""

    model = Resource
    template_name = "journal/resource_detail.html"
    context_object_name = "resource"


def blog_detail(request, pk):
    """View to display blog post details."""
    post = get_object_or_404(BlogPost, pk=pk)
    related_posts = BlogPost.objects.filter(published=True).exclude(id=pk).order_by("-timestamp")[:5]
    comment_form = CommentForm()
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.content_object = post
            comment.user = request.user
            comment.save()
            return redirect("journal:blog_detail", pk=pk)
    return render(request, "blog_detail.html", {
        "post": post,
        "related_posts": related_posts,
        "comment_form": comment_form
    })
# Q&A Views


class QuestionCreateView(LoginRequiredMixin, CreateView):
    """View to create a new question."""

    model = Question
    fields = ["question"]
    template_name = "question_form.html"
    success_url = reverse_lazy("journal:qna_list")

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_subscriber:
            return HttpResponseForbidden(
                "You must be a subscriber to ask a question."
            )
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        ActivityLog.objects.create(
            user=self.request.user, action=f"Asked a question: {
                form.instance.question}"
        )
        return super().form_valid(form)


class AnswerCreateView(LoginRequiredMixin, CreateView):
    """View to create an answer to a question."""

    model = Answer
    fields = ["answer"]
    template_name = "answer_form.html"

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_premium and not user.is_moderator_or_admin:
            return HttpResponseForbidden(
                "You must be a premium subscriber, moderator, or admin to answer questions."
            )
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.professional = self.request.user
        form.instance.question = get_object_or_404(
            Question, pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("journal:qna_detail", kwargs={"pk": self.kwargs["pk"]})


def qna_list(request):
    """View to list all questions."""
    questions = Question.objects.all()
    return render(request, "qna_list.html", {"questions": questions})


def qna_detail(request, pk):
    """View to display question and its answers."""
    question = get_object_or_404(Question, pk=pk)
    answers = Answer.objects.filter(question=question)
    return render(
        request, "qna_detail.html", {"question": question, "answers": answers}
    )


# Miscellaneous Views
def privacy_policy(request):
    """View to display the privacy policy."""
    return HttpResponse(
        "<h1>Privacy Policy</h1><p>This is a placeholder for the privacy policy.</p>"
    )


def terms_of_service(request):
    """View to display the terms of service."""
    return HttpResponse(
        "<h1>Terms of Service</h1><p>This is a placeholder for the terms of service.</p>"
    )


class ContactView(TemplateView):
    """View for the contact page."""

    template_name = "contact.html"
    fields = ["name", "email", "subject", "message"]


class AboutView(TemplateView):
    """View for the about page."""

    template_name = "about.html"
    
    
class ModeratorListView(LoginRequiredMixin, ListView):
    """View to list moderators."""

    model = CustomUser
    template_name = "moderators.html"
    context_object_name = "moderators"

    def get_queryset(self):
        return CustomUser.objects.filter(is_moderator=True)


class MessageListView(LoginRequiredMixin, ListView):
    """View to list messages."""

    model = Message
    template_name = "messages.html"
    
    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user)
    
    
class FeatureListView(ListView):
    """View to list features."""
    template_name = "features.html"


class ActivityLogListView(LoginRequiredMixin, ListView):
    """View to display the activity log."""

    model = ActivityLog
    template_name = "activity_log.html"
    context_object_name = "activity_logs"
    paginate_by = 10
    ordering = ["-timestamp"]

    def get_queryset(self):
        return ActivityLog.objects.all().order_by("-timestamp")


class BillingView(LoginRequiredMixin, ListView):
    """View to display billing information."""

    model = Billing
    template_name = "billing.html"
    context_object_name = "billing"
    paginate_by = 10
    ordering = ["-created_at"]


class FeedbackView(LoginRequiredMixin, TemplateView):
    """View for submitting feedback."""

    template_name = "feedback.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_message"] = "We'd love to hear your feedback!"
        return context


class FaqView(LoginRequiredMixin, TemplateView):
    """View to display frequently asked questions."""

    template_name = "faqs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["faqs"] = Faq.objects.all()
        return context
