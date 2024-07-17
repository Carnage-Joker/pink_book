from django.urls import path
from .views import (ContactView, DashboardView, ForumPostDetailView,
                    HabitCreateView, HabitListView,
                    HabitUpdateView, HabitDetailView, JournalEntryDetailView,
                    JournalEntryCreateView, JournalEntryUpdateView,
                    JournalEntryDeleteView, JournalEntryListView,
                    LogoutView, ProfileUpdateView, ProfileView,
                    ProfileSettingsView, ProfileCustomizeView, RegisterView,
                    ResourceCategoryView, ResourceListView, ResourceDetailView,
                    ToDoCreateView,
                    ToDoDetailView, ToDoListView, ToDoUpdateView, AboutView,
                    complete_task_view, generate_task_view, fail_task_view,
                    PasswordResetDoneView, PasswordResetView,
                    complete_todo_view,
                    guide_list, guide_detail, ActivityLogListView, BillingView,
                    qna_list, qna_detail, activate_account, MessageListView,
                    CustomLoginView, ModeratorListView, TemplateView,
                    ForumCreateView, ForumDeleteView, PostListView, ThreadListView,
                    ForumDeleteView, ForumPostDetailView, FeatureListView)

app_name = 'journal'

urlpatterns = [
    # Authentication
    path('', CustomLoginView.as_view(), name='welcome'),
    path('features/', FeatureListView.as_view(), name='feature_list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('about/', AboutView.as_view(), name='about'),
    path('activate/<str:token>/', activate_account, name='activate_account'),
    path('registration_complete/', TemplateView.as_view(
        template_name='registration_complete.html'), name='registration_complete'),


    # Dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/settings/', ProfileSettingsView.as_view(), name='profile_settings'),
    path('profile/customize/', ProfileCustomizeView.as_view(), name='customize_theme'),

    # Journal
    path('new/', JournalEntryCreateView.as_view(), name='new_entry'),
    path('list', JournalEntryListView.as_view(), name='entry_list'),
    path('entry/<int:pk>/', JournalEntryDetailView.as_view(), name='entry_detail'),
    path('entry/<int:pk>/edit/', JournalEntryUpdateView.as_view(), name='entry_update'),
    path('entry/<int:pk>/delete/', JournalEntryDeleteView.as_view(), name='entry_delete'),

    # Forum
    # Forum
    path('forum/', ThreadListView.as_view(), name='thread_list'),
    path('forum/posts/', PostListView.as_view(), name='post_list'),
    path('forum/create/', ForumCreateView.as_view(), name='create_post'),
    path('forum/<int:pk>/', ForumPostDetailView.as_view(), name='post_detail'),
    path('forum/<int:pk>/delete/', ForumDeleteView.as_view(), name='post_delete'),
    path('forum/moderators/', ModeratorListView.as_view(), name='moderators'),
     

    # Habit Tracker
    path('habits/', HabitListView.as_view(), name='habit_list'),
    path('habits/create/', HabitCreateView.as_view(), name='habit_create'),
    path('habits/<int:pk>/', HabitDetailView.as_view(), name='habit_detail'),
    path('activity/', ActivityLogListView.as_view(), name='activity_log'),
    path('billing/', BillingView.as_view(), name='billing'),
    path('inbox/', MessageListView.as_view(), name='message_list'),

    path('habits/<int:pk>/update/', HabitUpdateView.as_view(), name='habit_update'),

    # To-Do List
    path('todos/', ToDoListView.as_view(), name='todo_list'),
    path('todos/new/', ToDoCreateView.as_view(), name='create_todo'),
    path('todos/<int:pk>/edit/', ToDoUpdateView.as_view(), name='todo_update'),
    path('todo/<int:pk>/', ToDoDetailView.as_view(), name='todo_detail'),
    path('generate-task/', generate_task_view, name='generate-task'),
    path('complete-task/', complete_task_view, name='complete-task'),
    path('fail-task/', fail_task_view, name='fail-task'),
    path('complete-todo/', complete_todo_view, name='complete-todo'),


    # Resources
    
    path('guides/', guide_list, name='guide_list'),
    path('guides/<int:pk>/', guide_detail, name='guide_detail'),
    path('resources/', ResourceListView.as_view(), name='resource_list'),
    path('resources/<int:pk>/', ResourceCategoryView.as_view(),
         name='resource_category_detail'),
    path('resource/<int:pk>/', ResourceDetailView.as_view(),
         name='resource_detail'),
    


    # Contact
    path('contact/', ContactView.as_view(), name='contact'),
    path('qna/', qna_list, name='qna_list'),
    path('qna/<int:pk>/', qna_detail, name='qna_detail'),
]
    # Other features (commented out for now)
    # path('notifications/', NotificationListView.as_view(), name='notification_list'),
  
