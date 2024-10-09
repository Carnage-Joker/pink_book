from django.urls import path
from .views import (
    # Import your views without duplication
    ContactView, DashboardView, ForumPostDetailView, HabitCreateView,
    HabitListView, HabitUpdateView, HabitDetailView, JournalEntryDetailView,
    JournalEntryCreateView, JournalEntryUpdateView, JournalEntryDeleteView,
    JournalEntryListView, CustomLogoutView, ProfileUpdateView, ProfileView,
    ProfileSettingsView, ProfileCustomizeView, RegisterView,
    ResourceCategoryView, ResourceListView, ResourceDetailView, ToDoCreateView,
    ToDoDetailView, ToDoListView, ToDoUpdateView, AboutView, generate_task_view,
    fail_task_view, PasswordResetDoneView, PasswordResetView, CompleteToDoView,
    GuideDetailView, ActivityLogListView, BillingView, qna_list, qna_detail,
    MessageListView, CustomLoginView, ModeratorListView, ForumCreateView,
    ForumDeleteView, PostListView, ThreadListView, FeatureListView, BlogListView,
    blog_detail, IncrementHabitCounter, CompleteTaskView, privacy_policy,
    terms_of_service, ResendActivationView, RegistrationSuccessView,
    ActivateAccountView, activation_sent, FaqView, FeedbackView, BlogDetailView
)

app_name = 'journal'

urlpatterns = [
    # General
    path('', CustomLoginView.as_view(), name='welcome'),
    path('features/', FeatureListView.as_view(), name='feature_list'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('about/', AboutView.as_view(), name='about'),
    path('faq/', FaqView.as_view(), name='faq'),  # Removed duplicate
    path('register/', RegisterView.as_view(), name='register'),
    path('resend_activation/', ResendActivationView.as_view(),
         name='resend_activation'),
    path('registration-success/', RegistrationSuccessView.as_view(),
         name='registration_success'),
    path('activation_sent/', activation_sent, name='activation_sent'),
    path('activate/<uidb64>/<token>/',
         ActivateAccountView.as_view(), name='activate_account'),

    # Dashboard & Profile
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/settings/', ProfileSettingsView.as_view(),
         name='profile_settings'),
    path('profile/customize/', ProfileCustomizeView.as_view(),
         name='customize_theme'),

    # Journal
    path('journal/entry/create/<int:task_id>/',
         JournalEntryCreateView.as_view(), name='new_entry'),
    path('journal/entry/create/', JournalEntryCreateView.as_view(), name='new_entry'),
    path('journal/list/', JournalEntryListView.as_view(),
         name='entry_list'),  # Fixed missing slash
    path('journal/entry/<int:pk>/',
         JournalEntryDetailView.as_view(), name='entry_detail'),
    path('journal/entry/<int:pk>/edit/',
         JournalEntryUpdateView.as_view(), name='entry_update'),
    path('journal/entry/<int:pk>/delete/',
         JournalEntryDeleteView.as_view(), name='entry_delete'),

    # Forum
    path('forum/', ThreadListView.as_view(), name='thread_list'),
    path('forum/posts/<int:thread_id>/',
         PostListView.as_view(), name='post_list'),
    path('forum/create/', ForumCreateView.as_view(), name='create_post'),
    path('forum/<int:pk>/', ForumPostDetailView.as_view(), name='post_detail'),
    path('forum/<int:pk>/delete/', ForumDeleteView.as_view(), name='post_delete'),
    path('forum/moderators/', ModeratorListView.as_view(), name='moderators'),

    # Habit Tracker
    path('habits/', HabitListView.as_view(), name='habit_list'),
    path('habits/create/', HabitCreateView.as_view(), name='habit_form'),
    path('habits/<int:pk>/', HabitDetailView.as_view(), name='habit_detail'),
    path('habits/<int:pk>/update/', HabitUpdateView.as_view(), name='habit_update'),
    path('increment-habit-counter/<int:pk>/',
         IncrementHabitCounter.as_view(), name='increment_habit_counter'),

    # To-Do List
    path('todos/', ToDoListView.as_view(), name='todo_list'),
    path('todos/new/', ToDoCreateView.as_view(), name='create_todo'),
    path('todos/<int:pk>/edit/', ToDoUpdateView.as_view(), name='todo_update'),
    path('todos/<int:pk>/', ToDoDetailView.as_view(), name='todo_detail'),
    path('generate-task/', generate_task_view, name='generate_task'),
    path('fail-task/', fail_task_view, name='fail_task'),
    path('complete-todo/<int:todo_id>/',
         CompleteToDoView.as_view(), name='complete_todo'),
    path('complete-task/', CompleteTaskView.as_view(), name='complete_task'),

    # Resources
    path('guide/<int:pk>/', GuideDetailView.as_view(), name='guide_detail'),
    path('resources/', ResourceListView.as_view(), name='resource_list'),
    path('resources/<int:pk>/', ResourceCategoryView.as_view(),
         name='resource_category_detail'),
    path('resource/<int:pk>/', ResourceDetailView.as_view(), name='resource_detail'),

    # Blog
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),

    # Contact and FAQ
    path('contact/', ContactView.as_view(), name='contact'),
    path('qna/', qna_list, name='qna_list'),
    path('qna/<int:pk>/', qna_detail, name='qna_detail'),

    # Other
    path('activity/', ActivityLogListView.as_view(), name='activity_log'),
    path('billing/', BillingView.as_view(), name='billing'),
    path('inbox/', MessageListView.as_view(), name='message_list'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('terms-of-service/', terms_of_service, name='terms_of_service'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
]
