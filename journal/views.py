
import json
import logging
from datetime import date
from typing import Any, Dict

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView as AuthLoginView
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)
from django.views.generic.edit import CreateView

from journal.models import CustomUser, Habit, JournalEntry, ToDo

# Local application imports
from .forms import (CommentForm, CustomUserCreationForm, CustomUserLoginForm,
                    CustomUserUpdateForm, HabitForm, JournalEntryForm,
                    ResendActivationForm, ThemeForm, ToDoForm)
from .generate import generate_insight, generate_prompt
from .models import (ActivityLog, Answer, Billing, BlogPost, Comment,
                     CustomUser, Faq, Guide, Habit, JournalEntry, Message,
                     Post, Question, Quote, Resource, ResourceCategory, Task,
                     TaskCompletion, Thread, ToDo)
from .utils.ai_utils import (extract_keywords, get_average_sentiment,
                             get_average_word_count, get_current_streak,
                             get_most_common_emotions, get_most_common_tags,
                             get_peak_journaling_time)
from .utils.utils import (calculate_penalty, generate_task,
                          generate_task_truth, send_activation_email)

# Set up the logger
logger = logging.getLogger(__name__)

User = get_user_model()




class SafeMixin:
    """
    Mixin to safely handle exceptions in views.
    """

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            messages.error(
                request,
                "An unexpected error occurred. Please try again later."
            )
            return redirect("journal:some_error_page")


class ResendActivationView(SafeMixin, FormView):
    """View to resend account activation email."""

    template_name = "resend_activation.html"
    form_class = ResendActivationForm
    success_url = reverse_lazy("journal:activation_sent")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = CustomUser.objects.filter(email=email, is_active=False).first()
        if user:
            send_activation_email(user, self.request)
            messages.success(
                self.request,
                "Activation email resent! Please check your email."
            )
        else:
            messages.error(
                self.request,
                "No inactive account found with that email."
            )
        return super().form_valid(form)


def activation_sent(request):
    """View to inform the user that activation email has been sent."""
    return render(request, "activation_sent.html")


class RegistrationSuccessView(TemplateView):
    template_name = "registration_success.html"

    def send_welcome_email(self, user):
        """
        Send a welcome email to the newly registered user.

        Args:
            user (CustomUser): The user who has just registered.
        """
        subject = "Welcome to Our Community!"
        message = "Thank you for registering. We're excited to have you!"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

    def get(self, request, *args, **kwargs):
        user_id = request.session.get('registered_user_id')
        if user_id:
            user = CustomUser.objects.get(id=user_id)

            # Specify the backend for allauth
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            
            self.send_welcome_email(user)
            messages.success(
                request,
                "Your account was activated successfully. Welcome to the community!",
            )
            request.session.pop('registered_user_id', None)
        else:
            messages.error(request, "No user found. Please log in.")
            return redirect("journal:welcome")
        return super().get(request, *args, **kwargs)


class RegisterView(SafeMixin, FormView):
    """View to register a new user."""

    template_name = "register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("journal:registration_success")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        send_activation_email(user, self.request)
        # Store user ID in session
        self.request.session['registered_user_id'] = user.id
        messages.success(
            self.request,
            "Your account has been created! Please check your email to activate your account."
        )
        return redirect(self.success_url)


class ActivateAccountView(SafeMixin, View):
    """View to activate a user account."""

    def get(self, request, uidb64, token):
        """
        Activate the user account using the provided UID and token.

        Args:
            request: The HTTP request.
            uidb64: The base64-encoded user ID.
            token: The activation token.

        Returns:
            The response to redirect the user to the dashboard or an error message.
        """
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist) as e:
            user = None
            logger.error(f"Activation error: {e}")

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            # Log in the user after activation
            login(request, user)
            messages.success(
                request, "Your account has been activated successfully."
            )
            return redirect("journal:dashboard")
        else:
            messages.error(
                request, "Activation link is invalid or has expired!")
            return redirect("journal:some_error_page")


class CustomLoginView(SafeMixin, AuthLoginView):
    """Custom login view with additional logging and messaging."""

    template_name = "welcome.html"
    authentication_form = CustomUserLoginForm
    success_url = reverse_lazy("journal:dashboard")

    def form_valid(self, form: CustomUserLoginForm):
        """
        Handle a valid login form submission.

        This method logs in the user and logs the successful login event.
        """
        user = form.get_user()
        login(self.request, user)
        logger.info(
            f"User {user.sissy_name} (Email: {user.email}) logged in successfully."
        )
        return redirect(self.success_url)

    def form_invalid(self, form: CustomUserLoginForm) -> HttpResponse:
        """
        Handle an invalid form submission by logging the error and displaying an error message.

        Args:
            form: The form instance that was submitted.

        Returns:
            The response to render the form with errors.
        """
        logger.warning(f"Failed login attempt with errors: {form.errors}")
        messages.error(
            self.request, "Login failed. Please check your username and password."
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
                f"User {user.get_username()} (Email: {user.email}) is logging out."
            )
            messages.success(request, "You have successfully logged out.")
        else:
            messages.error(request, "You are not logged in.")
        return super().dispatch(request, *args, **kwargs)


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

    def get_object(self, queryset=None):
        """
        Retrieve the current user object.

        This method is used to fetch the user object associated with the current session.
        It ensures that the profile update view operates on the correct user instance.

        Returns:
            CustomUser: The user object associated with the current session.
        """
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

    def form_invalid(self, form: ThemeForm) -> HttpResponse:
        """
        Handle invalid form submissions.

        Args:
            form: The form instance that was submitted.

        Returns:
            The response to render the form with errors.
        """
        messages.error(
            self.request,
            "An error occurred while updating your profile. Please try again."
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = getattr(user, "profile", None)
        context["profile"] = profile
        return context

    def get_object(self):
        return self.request.user


class ProfileSettingsView(LoginRequiredMixin, SafeMixin, TemplateView):
    """View to display user profile settings."""

    template_name = "profile_settings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = getattr(user, "profile", None)
        context["profile"] = profile
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    """Enhanced View for the user dashboard."""
    template_name = "dashboard.html"

    def get_profile_pic(self):
        """Retrieve the URL of the user's profile picture."""
        user = self.request.user
        if user.profile_picture:
            return user.profile_picture.url
        return "/static/journal/media/default-profile-pic.jpg"

    def get_quote_of_the_day(self):
        """Select a deterministic quote based on the current day."""
        today = date.today()
        quotes = list(Quote.objects.all())
        if quotes:
            index = today.toordinal() % len(quotes)
            return quotes[index].content
        return "Every day is a chance to be fabulous!"

    def get_context_data(self, **kwargs):
        """Populate context with dashboard data and ensure dynamic updates."""
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Optimize database queries
        recent_entries = JournalEntry.objects.filter(
            user=user).order_by("-timestamp")[:3]
        todos = ToDo.objects.filter(user=user).order_by("-timestamp")[:5]
        habits = Habit.objects.filter(user=user).order_by("-timestamp")[:5]
        # Reset habit counters if needed
        for habit in habits:
            if habit.check_reset_needed():
                habit.reset_counter()

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

        # Profile and points
        points = getattr(user, "points", 0)
        profile_pic = self.get_profile_pic()

        # Additional context
        context.update({
            "user": user,
            "points": points,
            "profile_pic": profile_pic,
            "quote_of_the_day": self.get_quote_of_the_day(),
            "todos": todos,
            "habits": habits,
            "entries": recent_entries,
        })

        return context


class HomeView(SafeMixin, TemplateView):
    """Home page view."""

    template_name = "welcome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = ResourceCategory.objects.all()
        return context


class JournalEntryCreateView(LoginRequiredMixin, CreateView):
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = "new_entry.html"

    def get_initial(self) -> dict:
        initial = super().get_initial()
        generated_prompt = generate_prompt()
        initial['generated_prompt'] = generated_prompt
        return initial

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["generated_prompt"] = self.get_initial().get('generated_prompt')
        return context

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        form.instance.prompt_text = form.cleaned_data.get("generated_prompt")
        response = super().form_valid(form)

        # Generate and attach the insight
        try:
            insight_text = generate_insight(form.instance.content)
            form.instance.insight = insight_text
            form.instance.save(update_fields=['insight'])
        except Exception:
            messages.error(self.request, "Error generating insight.")
            form.instance.insight = "Insight generation failed."
            form.instance.save(update_fields=['insight'])

        # Award points to the user
        points_earned = form.instance.calculate_points()
        self.request.user.points += points_earned
        self.request.user.save()

        # Success message
        if points_earned > 0:
            messages.success(
                self.request,
                f"Journal entry created successfully! You have earned {points_earned} points."
            )
        else:
            messages.warning(
                self.request,
                f"You need to follow instructions to earn points. You lost {abs(points_earned)} points."
            )

        return response

    def get_success_url(self) -> str:
        return reverse("journal:entry_detail", kwargs={"pk": self.object.pk})


class JournalEntryWithTaskView(LoginRequiredMixin, CreateView):
    model = JournalEntry
    form_class = JournalEntryForm
    template_name = "new_entry_with_task.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_id = self.kwargs.get("task_id")
        task = get_object_or_404(Task, task_id=task_id, user=self.request.user)
        context["task"] = task
        return context

    def form_valid(self, form):
        task_id = self.kwargs.get("task_id")
        task = get_object_or_404(Task, task_id=task_id, user=self.request.user)

        form.instance.task = task.description
        form.instance.prompt_text = task.description
        form.instance.user = self.request.user

        # Analyze content for topic relevance after saving
        response = super().form_valid(form)
        form.instance.analyze_content()

        # Award or penalize points based on the AI analysis
        if form.instance.passes_ai_analysis():
            self.request.user.points += task.points_awarded
        else:
            self.request.user.points -= task.points_penalty  # Deduct points if the task fails

        self.request.user.save()

        messages.success(self.request, "Journal entry created successfully!")
        return response

    def get_success_url(self) -> str:
        return reverse("journal:entry_detail", kwargs={"pk": self.object.pk})


class JournalEntryDetailView(LoginRequiredMixin, DetailView):
    model = JournalEntry
    template_name = "entry_detail.html"
    context_object_name = "entry"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entry = context["entry"]
        # These may already be accessible in the template as entry.prompt_text and entry.insight
        context["prompt_text"] = entry.prompt_text
        context["insight"] = entry.insight
        context['tags'] = entry.tags.all()
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

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user, pk=self.kwargs.get("pk"))

    def delete(self, request, *args, **kwargs):
        journal_entry = self.get_object()
        ActivityLog.objects.create(
            user=request.user,
            action=f"Deleted a journal entry: {journal_entry.title[:20]}...",
        )
        return super().delete(request, *args, **kwargs)


def redeem_points(request):
    user_points = CustomUser.objects.get(request.user).points
    if request.method == "POST":
        points_to_redeem = int(request.POST.get("points", 0))
        if user_points.redeem_points(points_to_redeem):
            messages.success(
                request, f"Successfully redeemed {points_to_redeem} points!")
        else:
            messages.error(request, "Insufficient points.")
        return redirect('redeem_points')

    return render(request, 'redeem_points.html', {'points': user_points.points})


class TruthTaskGenerateView(LoginRequiredMixin, TemplateView):
    
    def get(self, request, *args, **kwargs):
        if truth_task := generate_task_truth(request.user):
            return redirect('journal:new_entry_with_task', task_id=str(truth_task.task_id))
        
        messages.error(
            request, "Failed to generate taask. Please try again.")
        return redirect('journal:dashboard')
        

class TaskGenerateView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        if task := generate_task(request.user):
            return redirect('journal:new_entry_with_task', task_id=str(task.task_id))

        messages.error(
            request, "Failed to generate a task. Please try again.")
        return redirect('journal:dashboard')


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
    def post(self, request, pk):
        habit = get_object_or_404(Habit, pk=pk, user=request.user)
        habit.increment_count()
        current_count = habit.increment_counter
        target_count = habit.target_count
        is_completed = habit.is_completed()
        current_streak = habit.get_current_streak()
        longest_streak = habit.get_longest_streak()
        insight = habit.get_insights()  # Add this line to generate insights dynamically
        return JsonResponse(
            {
                "status": "success",
                "new_count": current_count,
                "target_count": target_count,
                "is_completed": is_completed,
                "frequency": habit.frequency,
                "current_streak": current_streak,
                "longest_streak": longest_streak,
                "insight": insight,  # Include insights in the response
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
    user = request.user

    if request.method == "POST":
        try:
            task = generate_task(user)
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

    def get_context_data(self, **kwargs):
        """
        Add the latest blog posts to the context data.

        This method fetches the latest published blog posts and adds them to the context
        data for rendering in the template.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The context data dictionary to be used in the template.
        """
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

    def get_content_object(self):
        """
        Retrieve the post object that the comment is associated with.

        This method fetches the post object based on the post_id provided in the URL.
        It ensures that the comment is correctly linked to the post.

        Returns:
            Post: The post object that the comment is associated with.
        """
        post_id = self.kwargs.get("post_id")
        return get_object_or_404(Post, id=post_id)


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

    def get_context_data(self, **kwargs):
        """
        Add guides and pagination information to the context data.

        This method fetches all guides, paginates them, and adds the paginated
        guides to the context data for rendering in the template.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The context data dictionary to be used in the template.
        """
        context = super().get_context_data(**kwargs)
        guides = Guide.objects.all()
        paginator = Paginator(guides, 5)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["guides"] = page_obj
        return context


class ResourceCategoryListView(ListView):
    model = ResourceCategory
    template_name = "journal/resource_category_list.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Assuming the featured resource is the most recent one
        context["featured_resource"] = Resource.objects.order_by(
            "-timestamp").first()
        return context


class ResourceCategoryDetailView(DetailView):
    """View to display resources within a single category."""
    model = ResourceCategory
    template_name = "journal/resource_category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        context["resources"] = category.resources.order_by(
            "-timestamp")  # List of resources
        # Featured resource
        context["featured_resource"] = category.get_featured_resource()
        return context


def blog_detail(request, pk):
    """View to display blog post details."""
    post = get_object_or_404(BlogPost, pk=pk)
    related_posts = BlogPost.objects.filter(
        published=True).exclude(id=pk).order_by("-timestamp")[:5]
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


class AnswerCreateView(LoginRequiredMixin, CreateView):
    """View to create an answer to a question."""

    model = Answer
    fields = ["answer"]
    template_name = "answer_form.html"

    def dispatch(request, *args, **kwargs):
        user = CustomUser.objects.get(pk=request.user.pk)
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
        """
        Add FAQs to the context data.

        This method fetches all FAQs from the database and adds them to the context
        data for rendering in the template.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The context data dictionary to be used in the template.
        """
        context = super().get_context_data(**kwargs)
        context["faqs"] = Faq.objects.all()
        return context


class FaqView(LoginRequiredMixin, TemplateView):
    """View to display frequently asked questions."""

    template_name = "faqs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["faqs"] = Faq.objects.all()
        return context


def some_error_page(request):
    """View to display an error page."""
    return render(request, "some_error_page.html")
