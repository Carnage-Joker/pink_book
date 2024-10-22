from django.shortcuts import render
from django.core.paginator import Paginator
from .utils.utils import generate_task, send_activation_email
from .utils.ai_utils import (extract_keywords, get_average_sentiment,
                             get_average_word_count, get_current_streak,
                             get_most_common_emotions, get_most_common_tags,
                             get_peak_journaling_time)
from .models import (ActivityLog, Answer, Billing, BlogPost, Comment,
                     CustomUser, Faq, Guide, Habit, JournalEntry, Message,
                     Post, Question, Quote, Resource, ResourceCategory, Task,
                     TaskCompletion, Thread, ToDo)
from .generate import generate_insight, generate_prompt
from .forms import (CommentForm, CustomUserCreationForm, CustomUserLoginForm,
                    CustomUserUpdateForm, HabitForm, JournalEntryForm,
                    ProfileSettingsForm, ResendActivationForm, ThemeForm,
                    ToDoForm)
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.timezone import now
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.db.models import Q
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model, login
from django.contrib import messages
from datetime import date
import random
import logging
import json

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
    success_url = reverse_lazy('journal:welcome')
    redirect_authenticated_user = True
    extra_context = {'title': 'Register'}
    success_message = "Your account was created successfully. Please check your email to activate your account."
    failure_message = "There was an error creating your account. Please try again."

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
            #  automatically redirect from the activation_sent view to the welcome view after 5 seconds

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
        return redirect('journal:welcome')


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
        user = self.request.user
        if user.is_staff:  # type: ignore
            return Thread.objects.all()  # Return all threads if user is staff
        elif user.is_moderator:
            return Thread.objects.filter(moderators=user)  # Return threads where user is a moderator
        else:
            return Thread.objects.none()  # Return no threads if user is not staff or moderator


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

    def increment_habit_counter(self, pk):
        habit = get_object_or_404(Habit, pk=pk)
        habit.increment_count()
        return redirect('journal:habit_detail', pk=pk)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        habit = context['object']
        context['current_streak'] = habit.get_current_streak()
        context['longest_streak'] = habit.get_longest_streak()
        return context


class IncrementHabitCounterView(LoginRequiredMixin, View):
    def post(self, request, pk):
        habit = get_object_or_404(Habit, pk=pk, user=request.user)
        habit.increment_count()
        current_streak = habit.get_current_streak()
        longest_streak = habit.get_longest_streak()

        return JsonResponse({
            'status': 'success',
            'new_count': habit.increment_counter,
            'current_streak': current_streak,
            'longest_streak': longest_streak
        })


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
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
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
                # Task completion logic or redirect to journal entry form
                return redirect('journal:new_entry', task_id=task_id)
            else:
                return JsonResponse({'status': 'error', 'message': 'Task already completed'}, status=400)
        except Task.DoesNotExist:
            logger.error(f"Task with ID {task_id} does not exist.")
            return JsonResponse({'status': 'error', 'message': 'Task does not exist'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
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

        if task_id := self.kwargs.get('task_id'):
            context['task'] = Task.objects.get(pk=task_id)

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user

        if task_id := self.kwargs.get('task_id'):
            form.instance.task = Task.objects.get(pk=task_id)

        # Set the prompt text from context (which is already generated)
        form.instance.prompt_text = self.get_context_data()['generated_prompt']

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

        # Save the tags (many-to-many relationships)
        form.save_m2m()

        messages.success(
            self.request, "Journal entry created successfully with insights.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'journal:entry_detail',
            kwargs={'pk': self.object.pk}
        )


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
        if entry.task:
            context['task'] = entry.task
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
                                   action=(
                                       f"Updated a journal entry: "
                                       f"{form.instance.content[:20]}..."
                                   ))
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
        # Log the deletion action
        ActivityLog.objects.create(
            user=request.user,
            action=f"Deleted a journal entry: {journal_entry.title}"
        )
        return super().delete(request, *args, **kwargs)


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

        # Fetch necessary data before slicing
        recent_entries = JournalEntry.objects.filter(
            user=user).order_by('-timestamp')[:3]
        todos = ToDo.objects.filter(user=user).order_by(
            '-timestamp')  # Do not slice yet
        habits = Habit.objects.filter(user=user).order_by('-timestamp')[:5]

        # Process overdue todos (filter before slicing)
        overdue_todos = todos.filter(
            Q(due_date__lt=now().date()) & Q(completed=False))
        overdue_todos.update(processed=True)

        # Slice todos after filtering
        todos = todos[:5]  # Now apply the slice after all filtering is done

        # Calculate sentiment data
        sentiment_data = get_average_sentiment(recent_entries)

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
            'sentiment_data': sentiment_data,
            'polarity': sentiment_data.get('avg_polarity', 0),
            'subjectivity': sentiment_data.get('avg_subjectivity', 0),
        })
        return context


logger = logging.getLogger(__name__)


# Guide List View

def guide_list(request):
    guides = Guide.objects.all()
    return render(request, 'journal/guide_list.html', {'guides': guides})

# Guide Detail View


class GuideDetailView(DetailView):
    model = Guide
    template_name = "journal/guide_detail.html"
    context_object_name = 'guide'

# Resource List View (Listing Resources by Category)


class ResourceListView(ListView):
    model = ResourceCategory
    # More specific name for clarity
    template_name = "journal/resources.html"
    context_object_name = "categories"  # Consistent naming convention for categories

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        guides = Guide.objects.all()

        # Pagination: 5 guides per page
        paginator = Paginator(guides, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context["guides"] = page_obj
        return context

# Resource Category Detail View (Show Resources of Selected Category)


class ResourceCategoryView(DetailView):
    model = ResourceCategory
    template_name = "journal/resource_category_detail.html"
    context_object_name = 'category'

# Resource Detail View (Show Detailed Info for a Single Resource)


class ResourceDetailView(DetailView):
    model = Resource
    template_name = "journal/resource_detail.html"
    context_object_name = 'resource'


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
