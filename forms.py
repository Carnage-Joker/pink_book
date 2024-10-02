from django import forms
from .models import CustomUser, JournalEntry, Habit, ToDo, Post, Comment, Question, Answer


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('sissy_name', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data["password"])
            user.save()
        return user


class CustomUserLoginForm(forms.Form):
    sissy_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'description']

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.user.is_free_user() and Habit.objects.filter(user=self.instance.user).count() >= 3:
            raise forms.ValidationError(
                "Free users can only create up to 3 habits. Please upgrade your subscription.")
        return cleaned_data


class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['title', 'description', 'due_date']

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.user.is_free_user() and ToDo.objects.filter(user=self.instance.user).count() >= 5:
            raise forms.ValidationError(
                "Free users can only create up to 5 ToDos. Please upgrade your subscription.")
        return cleaned_data


class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['title', 'content']

    def save(self, commit=True):
        journal_entry = super().save(commit=False)
        if commit:
            if self.instance.user.is_premium_user() or self.instance.user.is_highest_user():
                journal_entry.insight = generate_insight(journal_entry.content)
            journal_entry.save()
        return journal_entry


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['thread', 'title', 'content']

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.user.is_free_user():
            raise forms.ValidationError(
                "Free users cannot create posts. Please upgrade your subscription.")
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.user.is_free_user():
            raise forms.ValidationError(
                "Free users cannot comment on posts. Please upgrade your subscription.")
        return cleaned_data


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question']

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.user.is_free_user():
            raise forms.ValidationError(
                "Free users cannot ask questions. Please upgrade your subscription.")
        return cleaned_data


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer']

    def clean(self):
        cleaned_data = super().clean()
        if not self.instance.user.is_premium_user() and not self.instance.user.is_highest_user():
            raise forms.ValidationError(
                "Only premium or highest-tier users can answer questions.")
        return cleaned_data
