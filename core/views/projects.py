from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from core.forms import ProjectForm
from core.models import Category, Project


@login_required
def create(request):
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        return redirect("project-detail", pk=project.pk)
    return render(request, "projects/create.html", {"form": form})


@login_required
def detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.visibility == "private" and project.owner != request.user:
        return render(request, "403.html", status=403)

    sort = request.GET.get("sort", "newest")
    metaprompts = project.metaprompts.all()
    if project.owner != request.user:
        metaprompts = metaprompts.filter(visibility="public")
    if sort == "oldest":
        metaprompts = metaprompts.order_by("created_at")
    elif sort == "title":
        metaprompts = metaprompts.order_by("title")
    else:
        metaprompts = metaprompts.order_by("-created_at")

    categories = Category.objects.all()
    return render(request, "projects/view.html", {
        "project": project,
        "metaprompts": metaprompts,
        "categories": categories,
        "is_owner": project.owner == request.user,
        "sort": sort,
    })


@login_required
def edit(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("project-detail", pk=project.pk)
    return render(request, "projects/create.html", {"form": form, "editing": True, "project": project})


@login_required
def delete(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if request.method == "POST":
        project.delete()
        return redirect("home")
    return render(request, "projects/confirm_delete.html", {"project": project})


@login_required
def toggle_pin(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    project.is_pinned = not project.is_pinned
    project.save(update_fields=["is_pinned"])
    if request.htmx:
        return render(request, "components/_pin_button.html", {
            "item": project, "pin_url": "project-pin", "item_type": "project",
        })
    return redirect("home")


@login_required
def toggle_visibility(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if request.method == "POST":
        new_vis = request.POST.get("visibility", "private")
        if new_vis == "public":
            tag_ids = request.POST.getlist("category_tags")
            if not tag_ids or len(tag_ids) > 3:
                categories = Category.objects.all()
                return render(request, "components/_category_modal.html", {
                    "item": project, "categories": categories,
                    "error": "Select 1 to 3 categories.", "item_type": "project",
                })
            project.visibility = "public"
            project.save(update_fields=["visibility"])
            project.category_tags.set(tag_ids)
        else:
            project.visibility = "private"
            project.save(update_fields=["visibility"])
            project.category_tags.clear()
    return redirect("project-detail", pk=project.pk)


@login_required
def category_modal(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    categories = Category.objects.all()
    return render(request, "components/_category_modal.html", {
        "item": project, "categories": categories, "item_type": "project",
    })


@login_required
def metaprompt_grid(request, pk):
    project = get_object_or_404(Project, pk=pk)
    sort = request.GET.get("sort", "newest")
    metaprompts = project.metaprompts.all()
    if project.owner != request.user:
        metaprompts = metaprompts.filter(visibility="public")
    if sort == "oldest":
        metaprompts = metaprompts.order_by("created_at")
    elif sort == "title":
        metaprompts = metaprompts.order_by("title")
    else:
        metaprompts = metaprompts.order_by("-created_at")

    return render(request, "projects/_metaprompt_grid.html", {
        "metaprompts": metaprompts, "project": project,
        "is_owner": project.owner == request.user, "sort": sort,
    })
