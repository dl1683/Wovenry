from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.forms import MetapromptForm
from core.models import Category, Metaprompt, Project
from core.services import generate_category_tags


@login_required
def create(request):
    project_id = request.GET.get("project")
    initial = {}
    project = None
    if project_id:
        project = get_object_or_404(Project, pk=project_id, owner=request.user)

    form = MetapromptForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        mp = form.save(commit=False)
        mp.owner = request.user
        mp.project = project
        mp.save()
        return redirect("metaprompt-edit", pk=mp.pk)

    return render(request, "metaprompts/editor.html", {
        "form": form, "project": project, "creating": True,
    })


@login_required
def edit(request, pk):
    mp = get_object_or_404(Metaprompt, pk=pk, owner=request.user)
    form = MetapromptForm(request.POST or None, instance=mp)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("metaprompt-edit", pk=mp.pk)

    categories = Category.objects.all()
    return render(request, "metaprompts/editor.html", {
        "form": form, "metaprompt": mp, "categories": categories,
    })


@login_required
def delete(request, pk):
    mp = get_object_or_404(Metaprompt, pk=pk, owner=request.user)
    project_pk = mp.project_id
    if request.method == "POST":
        mp.delete()
        if project_pk:
            return redirect("project-detail", pk=project_pk)
        return redirect("home")
    return render(request, "metaprompts/confirm_delete.html", {"metaprompt": mp})


@login_required
def toggle_pin(request, pk):
    mp = get_object_or_404(Metaprompt, pk=pk, owner=request.user)
    mp.is_pinned = not mp.is_pinned
    mp.save(update_fields=["is_pinned"])
    if request.htmx:
        return render(request, "components/_pin_button.html", {
            "item": mp, "pin_url": "metaprompt-pin", "item_type": "metaprompt",
        })
    return redirect("home")


@login_required
def publish(request, pk):
    mp = get_object_or_404(Metaprompt, pk=pk, owner=request.user)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "publish":
            mp.status = "published"
            mp.save(update_fields=["status"])
        elif action == "draft":
            mp.status = "draft"
            mp.visibility = "private"
            mp.save(update_fields=["status", "visibility"])
            mp.category_tags.clear()
        return redirect("metaprompt-edit", pk=mp.pk)
    return redirect("metaprompt-edit", pk=mp.pk)


@login_required
def toggle_visibility(request, pk):
    mp = get_object_or_404(Metaprompt, pk=pk, owner=request.user)
    if request.method == "POST":
        new_vis = request.POST.get("visibility", "private")
        if new_vis == "public":
            if mp.status != "published":
                return redirect("metaprompt-edit", pk=mp.pk)
            tag_ids = request.POST.getlist("category_tags")
            if not tag_ids or len(tag_ids) > 3:
                categories = Category.objects.all()
                return render(request, "components/_category_modal.html", {
                    "item": mp, "categories": categories,
                    "error": "Select 1 to 3 categories.", "item_type": "metaprompt",
                })
            mp.visibility = "public"
            mp.save(update_fields=["visibility"])
            mp.category_tags.set(tag_ids)
        else:
            mp.visibility = "private"
            mp.save(update_fields=["visibility"])
            mp.category_tags.clear()
    return redirect("metaprompt-edit", pk=mp.pk)


@login_required
def category_modal(request, pk):
    mp = get_object_or_404(Metaprompt, pk=pk, owner=request.user)
    categories = Category.objects.all()
    return render(request, "components/_category_modal.html", {
        "item": mp, "categories": categories, "item_type": "metaprompt",
    })


@login_required
def ai_categorize(request, pk):
    mp = get_object_or_404(Metaprompt, pk=pk, owner=request.user)
    suggested_names = generate_category_tags(mp.title, mp.content, mp.description)
    suggested = Category.objects.filter(name__in=suggested_names)
    return render(request, "metaprompts/_category_result.html", {
        "suggested": suggested, "metaprompt": mp,
    })
