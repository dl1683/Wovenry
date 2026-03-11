from django.conf import settings
from django.db import models


class AllowedEmail(models.Model):
    email = models.EmailField(unique=True)
    invited_at = models.DateTimeField(auto_now_add=True)
    registered = models.BooleanField(default=False)

    class Meta:
        ordering = ["-invited_at"]

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    class Visibility(models.TextChoices):
        PRIVATE = "private", "Private"
        PUBLIC = "public", "Public"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    visibility = models.CharField(
        max_length=7, choices=Visibility.choices, default=Visibility.PRIVATE
    )
    is_pinned = models.BooleanField(default=False)
    category_tags = models.ManyToManyField(Category, blank=True, related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_pinned", "-updated_at"]

    def __str__(self):
        return self.title


class Metaprompt(models.Model):
    class Visibility(models.TextChoices):
        PRIVATE = "private", "Private"
        PUBLIC = "public", "Public"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="metaprompts"
    )
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="metaprompts"
    )
    title = models.CharField(max_length=200)
    content = models.TextField(help_text="The metaprompt template content")
    description = models.TextField(blank=True, help_text="Instructions for using this metaprompt")
    visibility = models.CharField(
        max_length=7, choices=Visibility.choices, default=Visibility.PRIVATE
    )
    status = models.CharField(
        max_length=9, choices=Status.choices, default=Status.DRAFT
    )
    is_pinned = models.BooleanField(default=False)
    category_tags = models.ManyToManyField(Category, blank=True, related_name="metaprompts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_pinned", "-updated_at"]

    def __str__(self):
        return self.title


class Report(models.Model):
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True, blank=True
    )
    metaprompt = models.ForeignKey(
        Metaprompt, on_delete=models.CASCADE, null=True, blank=True
    )
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        target = self.project or self.metaprompt
        return f"Report on {target} by {self.reporter}"
