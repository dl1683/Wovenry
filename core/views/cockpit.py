from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.models import Metaprompt, Project


@login_required
def home(request):
    return render(request, "cockpit/home.html", {
        "active_tab": "metaprompts",
    })


@login_required
def tab_content(request, tab):
    if tab == "projects":
        items = Project.objects.filter(owner=request.user)
        pinned = items.filter(is_pinned=True)
        recent = items.filter(is_pinned=False)
        return render(request, "cockpit/_tab_projects.html", {
            "pinned": pinned, "recent": recent,
        })
    else:
        items = Metaprompt.objects.filter(owner=request.user)
        pinned = items.filter(is_pinned=True)
        recent = items.filter(is_pinned=False)
        return render(request, "cockpit/_tab_metaprompts.html", {
            "pinned": pinned, "recent": recent,
        })
