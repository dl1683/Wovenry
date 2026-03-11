from django.contrib import admin
from .models import AllowedEmail, Category, Project, Metaprompt, Report


@admin.register(AllowedEmail)
class AllowedEmailAdmin(admin.ModelAdmin):
    list_display = ("email", "invited_at", "registered")
    list_filter = ("registered",)
    search_fields = ("email",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "visibility", "is_pinned", "created_at")
    list_filter = ("visibility", "is_pinned")
    search_fields = ("title",)


@admin.register(Metaprompt)
class MetapromptAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "project", "visibility", "status", "created_at")
    list_filter = ("visibility", "status")
    search_fields = ("title",)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("reporter", "project", "metaprompt", "resolved", "created_at")
    list_filter = ("resolved",)
