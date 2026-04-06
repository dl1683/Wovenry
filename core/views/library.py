from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from core.models import Category, Metaprompt, Project


@login_required
def public_library(request):
    categories = Category.objects.all()
    metaprompts = Metaprompt.objects.filter(
        visibility="public", status="published"
    ).distinct().select_related("owner")
    return render(request, "library/index.html", {
        "categories": categories,
        "metaprompts": metaprompts,
        "q": "",
        "active_category": "",
    })


@login_required
def library_tab(request, tab):
    categories = Category.objects.all()
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")

    if tab == "projects":
        items = Project.objects.filter(visibility="public")
        if q:
            items = items.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if category:
            items = items.filter(category_tags__slug=category)
        items = items.distinct().select_related("owner")
        return render(request, "library/_tab_projects.html", {
            "projects": items, "categories": categories,
            "q": q, "active_category": category,
        })
    else:
        items = Metaprompt.objects.filter(visibility="public", status="published")
        if q:
            items = items.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if category:
            items = items.filter(category_tags__slug=category)
        items = items.distinct().select_related("owner")
        return render(request, "library/_tab_metaprompts.html", {
            "metaprompts": items, "categories": categories,
            "q": q, "active_category": category,
        })


@login_required
def public_projects(request):
    categories = Category.objects.all()
    projects = Project.objects.filter(visibility="public")

    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")

    if q:
        projects = projects.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if category:
        projects = projects.filter(category_tags__slug=category)

    projects = projects.distinct().select_related("owner")

    if request.htmx:
        return render(request, "library/_results_grid.html", {
            "items": projects, "item_type": "project",
        })

    return render(request, "library/projects.html", {
        "projects": projects, "categories": categories,
        "q": q, "active_category": category,
    })


@login_required
def public_metaprompts(request):
    categories = Category.objects.all()
    metaprompts = Metaprompt.objects.filter(visibility="public", status="published")

    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")

    if q:
        metaprompts = metaprompts.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if category:
        metaprompts = metaprompts.filter(category_tags__slug=category)

    metaprompts = metaprompts.distinct().select_related("owner")

    if request.htmx:
        return render(request, "library/_results_grid.html", {
            "items": metaprompts, "item_type": "metaprompt",
        })

    return render(request, "library/metaprompts.html", {
        "metaprompts": metaprompts, "categories": categories,
        "q": q, "active_category": category,
    })
