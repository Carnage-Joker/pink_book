from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .validators import validate_sissy_name
from .models import UserProfile, CustomUser, JournalEntry, Tag, Habit, ToDo, Comment, ResourceComment, Post, Report, UserTheme, UserFeedback
from .ai_utils import get_chatgpt_prompt, get_sentiment


class ThemeForm(forms.ModelForm):
    class Meta:
        model = UserTheme
        fields = ['color', 'layout']
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'description']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason']
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']

class ResourceCommentForm(forms.ModelForm):
    class Meta:
        model = ResourceComment  # Use the ResourceComment model
        fields = ['content']  # Use the 'content' field

        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Use the 'content' field

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'description', 'reminder_frequency']


class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['task', 'description', 'due_date']




class CustomUserLoginForm(AuthenticationForm):
    sissy_name = forms.CharField(label="Sissy Name", widget=forms.TextInput(attrs={'autofocus': True}))

    class Meta:
        model = CustomUser
        fields = ('sissy_name', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'] = self.fields['sissy_name']  # Override the 'username' field with 'sissy_name'
        del self.fields['sissy_name']
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'username',  # Use 'username' here
            'password',
            Submit('submit', 'Sign In'),
        )

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    sissy_name = forms.CharField(max_length=255, validators=[validate_sissy_name])

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
    sissy_name = forms.CharField(max_length=255, validators=[validate_sissy_name])
    class Meta:
        model = CustomUser
        fields = ('date_of_birth', 'sissy_name', 'bio','location', 'profile_picture', 'pronouns', 'sissy_type', 'chastity_status', 'owned_status')
        widgets = {
            'email': forms.EmailInput(),
          'sissy_name': forms.TextInput(),
        }
class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['privacy_level', 'nsfw_blur']
        labels = {
            'privacy_level': 'Who Can See Me, Darling? 💋',
            'nsfw_blur': 'Blur NSFW Content 🙈'
        }
        widgets = {
            'privacy_level': forms.Select(choices=[
                ('public', 'Public Darling 💋'),
                ('friends', 'Just for Friends 🎀'),
                ('private', 'My Secret 🤫')
            ]),
            'nsfw_blur': forms.CheckboxInput(attrs={'label': 'Blur it for me, please! 🌸'})
        }

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['title', 'content', 'tags', 'image', 'video', 'audio', 'file',]
        exclude = ['timestamp', 'polarity', 'subjectivity']
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
        exclude = ['created_at', 'updated_at']
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'name',
            'description',
            Submit('submit', 'Create Tag')
        )
