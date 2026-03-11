from django.urls import path
from core.views import auth, cockpit, projects, metaprompts, library, mixer, social

urlpatterns = [
    # Auth
    path("auth/login/", auth.login_view, name="login"),
    path("auth/logout/", auth.logout_view, name="logout"),
    path("auth/register/", auth.register_view, name="register"),

    # Cockpit
    path("", cockpit.home, name="home"),
    path("cockpit/tab/<str:tab>/", cockpit.tab_content, name="cockpit-tab"),

    # Projects
    path("projects/new/", projects.create, name="project-create"),
    path("projects/<int:pk>/", projects.detail, name="project-detail"),
    path("projects/<int:pk>/edit/", projects.edit, name="project-edit"),
    path("projects/<int:pk>/delete/", projects.delete, name="project-delete"),
    path("projects/<int:pk>/pin/", projects.toggle_pin, name="project-pin"),
    path("projects/<int:pk>/visibility/", projects.toggle_visibility, name="project-visibility"),
    path("projects/<int:pk>/categories/", projects.category_modal, name="project-categories"),
    path("projects/<int:pk>/grid/", projects.metaprompt_grid, name="project-grid"),

    # Metaprompts
    path("metaprompts/new/", metaprompts.create, name="metaprompt-create"),
    path("metaprompts/<int:pk>/edit/", metaprompts.edit, name="metaprompt-edit"),
    path("metaprompts/<int:pk>/delete/", metaprompts.delete, name="metaprompt-delete"),
    path("metaprompts/<int:pk>/pin/", metaprompts.toggle_pin, name="metaprompt-pin"),
    path("metaprompts/<int:pk>/publish/", metaprompts.publish, name="metaprompt-publish"),
    path("metaprompts/<int:pk>/visibility/", metaprompts.toggle_visibility, name="metaprompt-visibility"),
    path("metaprompts/<int:pk>/categorize/", metaprompts.ai_categorize, name="metaprompt-categorize"),
    path("metaprompts/<int:pk>/categories/", metaprompts.category_modal, name="metaprompt-categories"),

    # Public libraries
    path("library/projects/", library.public_projects, name="library-projects"),
    path("library/metaprompts/", library.public_metaprompts, name="library-metaprompts"),

    # Mixer
    path("mixer/<int:pk>/", mixer.view, name="mixer"),

    # Social
    path("copy/project/<int:pk>/", social.copy_project, name="copy-project"),
    path("copy/metaprompt/<int:pk>/", social.copy_metaprompt, name="copy-metaprompt"),
    path("report/", social.report, name="report"),
]
