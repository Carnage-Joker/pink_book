
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


from .models import (Comment, CustomUser, Habit, JournalEntry, Post, Report,
                     ResourceComment, Tag, ToDo, UserProfile,
                     UserTheme)


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'description', 'reward',
                  'penalty', 'reminder_frequency']

    def __init__(self, *args, **kwargs):
        super(HabitForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'frequency',
            Submit('submit', 'Save Habit', css_class='btn-primary')
        )
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
        labels = {
            'title': 'Post Title',
            'content': 'What’s on your mind, darling?',
            'category': 'Choose a Category',
        }
        help_texts = {
            'title': 'Make it snappy and sweet!',
            'content': 'Feel free to express yourself. 💖',
        }


class ResourceCommentForm(forms.ModelForm):
    class Meta:
        model = ResourceComment
        fields = ['content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content is not None and 'unpleasant' in content.lower():
            raise forms.ValidationError('Please keep the vibe positive '
                                        'and uplifting! 💕')
        return content


class ThemeForm(forms.ModelForm):
    class Meta:
        model = UserTheme
        fields = ['color', 'layout']


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason']


class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = [
            "task",
            "description",
            "due_date",
            "completed",
            "priority",
            "category"
        ]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            # Hide completed field if it shouldn't be user-editable
            'completed': forms.HiddenInput(),
        }


class CustomUserLoginForm(AuthenticationForm):
    sissy_name = forms.CharField(
        label="Sissy Name", widget=forms.TextInput(attrs={'autofocus': True}))

    class Meta:
        model = CustomUser
        fields = ('sissy_name', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'] = self.fields['sissy_name']
        del self.fields['sissy_name']
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Sign In'),
        )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'sissy_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'email',
            'sissy_name',
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Sign Up'),
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.sissy_name = self.cleaned_data['sissy_name']
        if commit:
            user.save()
        return user


class CustomUserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    sissy_name = forms.CharField(max_length=255)

    class Meta:
        model = CustomUser
        fields = (
            'date_of_birth',
            'bio',
            'location',
            'profile_picture',
            'pronouns',
            'sissy_type',
            'chastity_status',
            'owned_status',
            'email'
        )


class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['privacy_level', 'nsfw_blur', 'insight_opt']
        labels = {
            'privacy_level': 'Who Can See Me, Darling? 💋',
            'nsfw_blur': 'Blur NSFW Content 🙈',
            'insight_opt': 'Opt-in to AI Insights 🤖'
        }
        widgets = {
            'privacy_level': forms.Select(choices=[
                ('public', 'Public Darling 💋'),
                ('friends', 'Just for Friends 🎀'),
                ('private', 'My Secret 🤫')
            ]),
            'nsfw_blur': forms.CheckboxInput(
                attrs={'label': 'Blur it for me, please! 🌸'}
            ),
            'insights_opt': forms.CheckboxInput(
                attrs={'label': 'Yes, please! 🤖'}
            )
        }


class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['title', 'content', 'tags',
                  'image', 'video', 'audio', 'file',]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'title',
            'content',
            'tags',
            'image',
            'video',
            'audio',
            'file',
            Submit('submit', 'Post Entry')

        )


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag

        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'name',
            'description',
            Submit('submit', 'Create Tag')
        )
