from django import forms
from django.contrib.auth.models import User
from .models import Project, Metaprompt, Report


class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
        "placeholder": "you@example.com",
    }))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
        "placeholder": "Choose a username",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
        "placeholder": "Choose a password",
    }))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
        "placeholder": "Confirm password",
    }))

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get("email", "").lower()

        if cleaned.get("password") != cleaned.get("password_confirm"):
            raise forms.ValidationError("Passwords do not match.")

        if User.objects.filter(username=cleaned.get("username")).exists():
            raise forms.ValidationError("Username already taken.")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")

        return cleaned


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
        "placeholder": "Username",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
        "placeholder": "Password",
    }))


tw_input = "w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
tw_textarea = tw_input + " min-h-[120px]"


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"class": tw_input, "placeholder": "Project title"}),
            "description": forms.Textarea(attrs={"class": tw_textarea, "placeholder": "Project description (optional)", "rows": 3}),
        }


class MetapromptForm(forms.ModelForm):
    class Meta:
        model = Metaprompt
        fields = ["title", "content", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"class": tw_input, "placeholder": "e.g., NDA Risk Analyzer"}),
            "content": forms.Textarea(attrs={
                "class": tw_input + " min-h-[250px] font-mono text-sm",
                "placeholder": "[Role Definition]\n\n[Strategic Goal & Context]\n\n[Step-by-Step Reasoning Process]\n\n[Output Constraints & Format]",
            }),
            "description": forms.Textarea(attrs={
                "class": tw_textarea,
                "placeholder": "Instructions for the human user on how to use this metaprompt...",
                "rows": 4,
            }),
        }


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["reason"]
        widgets = {
            "reason": forms.Textarea(attrs={"class": tw_textarea, "placeholder": "Describe why you are reporting this content...", "rows": 4}),
        }
