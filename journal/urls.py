from django.urls import path

from .views import (ContactView, DashboardView, ForumPostDetailView,
                    ForumThreadListView, HabitCreateView, HabitListView,
                    HabitUpdateView, HabitDetailView, JournalEntryDetailView,
                    JournalEntryCreateView, JournalEntryUpdateView,
                    JournalEntryDeleteView, JournalEntryListView, LoginView,
                    LogoutView, ProfileUpdateView, ProfileView,
                    ProfileSettingsView, ProfileCustomizeView, RegisterView,
                    ResourceCategoryView, ResourceListView, ToDoCreateView,
                    ToDoDetailView, ToDoListView, ToDoUpdateView, AboutView,
                    complete_todo, fail_todo, PasswordResetDoneView, 
                    PasswordResetView)


urlpatterns = [
    # Authentication
    path('', LoginView.as_view(), name='welcome'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('about/', AboutView.as_view(), name='about'),
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
    path('forum/', ForumThreadListView.as_view(), name='categories'),
    path('forum/<int:pk>/', ForumPostDetailView.as_view(), name='post_detail'),

    # Habit Tracker
    path('habits/', HabitListView.as_view(), name='habit_list'),
    path('habits/create/', HabitCreateView.as_view(), name='habit_create'),
    path('habits/<int:pk>/', HabitDetailView.as_view(), name='habit_detail'),

    path('habits/<int:pk>/update/', HabitUpdateView.as_view(), name='habit_update'),

    # To-Do List
    path('todos/', ToDoListView.as_view(), name='todo_list'),
    path('todos/new/', ToDoCreateView.as_view(), name='create_todo'),
    path('todos/<int:pk>/edit/', ToDoUpdateView.as_view(), name='todo_update'),
    path('todo/<int:pk>/', ToDoDetailView.as_view(), name='todo_detail'),
    path('todos/<int:pk>/complete/', complete_todo, name='complete_todo'),
    path('todos/<int:pk>/fail/', fail_todo, name='fail_todo'),


    # Resources
    path('resources/', ResourceListView.as_view(), name='resources'),
    path('resources/new/', ResourceCategoryView.as_view(), name='category_detail'),

    # Contact
    path('contact/', ContactView.as_view(), name='contact'),

    # Other features (commented out for now)
    # path('notifications/', NotificationListView.as_view(), name='notification_list'),
    # path('messages/', MessageListView.as_view(), name='message_list'),
    # path('activity/', ActivityLogListView.as_view(), name='activity_log'),
    # path('billing/', BillingView.as_view(), name='billing'),
    # path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
]
