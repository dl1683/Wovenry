from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from core.forms import MetapromptForm
from core.models import Category, Metaprompt, Project
from core.services import generate_category_tags


TEMPLATE_CONTENT = (
    "[Role Definition]\n\n"
    "[Strategic Goal & Context]\n\n"
    "[Step-by-Step Reasoning Process]\n\n"
    "[Output Constraints & Format]"
)


@login_required
def create(request):
    project_id = request.GET.get("project")
    project = None
    if project_id:
        project = get_object_or_404(Project, pk=project_id, owner=request.user)

    initial = {"content": TEMPLATE_CONTENT}
    form = MetapromptForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        mp = form.save(commit=False)
        mp.owner = request.user
        mp.project = project

        save_action = request.POST.get("save_action", "save_private")
        mp.status = "published"
        mp.save()

        if save_action == "save_publish":
            messages.success(request, "Saved! Select categories to publish.")
            return redirect(
                reverse("metaprompt-edit", kwargs={"pk": mp.pk}) + "?show_categories=1"
            )
        messages.success(request, "Saved to Private Library.")
        return redirect("metaprompt-edit", pk=mp.pk)

    return render(request, "metaprompts/editor.html", {
        "form": form, "project": project, "creating": True,
    })


@login_required
def edit(request, pk):
    mp = get_object_or_404(Metaprompt, pk=pk, owner=request.user)
    form = MetapromptForm(request.POST or None, instance=mp)
    if request.method == "POST" and form.is_valid():
        save_action = request.POST.get("save_action", "save")

        if save_action == "save_private":
            mp = form.save(commit=False)
            mp.status = "published"
            mp.save()
            form.save_m2m()
            messages.success(request, "Saved to Private Library.")
            return redirect("metaprompt-edit", pk=mp.pk)
        elif save_action == "save_publish":
            mp = form.save(commit=False)
            mp.status = "published"
            mp.save()
            form.save_m2m()
            messages.success(request, "Saved! Select categories to publish.")
            return redirect(
                reverse("metaprompt-edit", kwargs={"pk": mp.pk}) + "?show_categories=1"
            )
        else:
            form.save()
            messages.success(request, "Changes saved.")
            return redirect("metaprompt-edit", pk=mp.pk)

    categories = Category.objects.all()
    show_categories = request.GET.get("show_categories") == "1"
    return render(request, "metaprompts/editor.html", {
        "form": form, "metaprompt": mp, "categories": categories,
        "show_categories": show_categories,
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
        if action == "draft":
            mp.status = "draft"
            mp.visibility = "private"
            mp.save(update_fields=["status", "visibility"])
            mp.category_tags.clear()
            messages.success(request, "Reverted to Draft.")
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
                form_action = reverse("metaprompt-visibility", kwargs={"pk": pk})
                return render(request, "components/_category_modal.html", {
                    "item": mp, "categories": categories,
                    "error": "Select 1 to 3 categories.", "item_type": "metaprompt",
                    "mode": "publish", "form_action": form_action,
                })
            mp.visibility = "public"
            mp.save(update_fields=["visibility"])
            mp.category_tags.set(tag_ids)
            messages.success(request, "Published to Public Library.")
        else:
            mp.visibility = "private"
            mp.save(update_fields=["visibility"])
            mp.category_tags.clear()
            messages.success(request, "Removed from Public Library.")
    return redirect("metaprompt-edit", pk=mp.pk)


@login_required
def category_modal(request, pk):
    mp = get_object_or_404(Metaprompt, pk=pk, owner=request.user)
    categories = Category.objects.all()
    mode = request.GET.get("mode", "publish")
    if mode == "edit":
        form_action = reverse("metaprompt-save-categories", kwargs={"pk": pk})
    else:
        form_action = reverse("metaprompt-visibility", kwargs={"pk": pk})
    return render(request, "components/_category_modal.html", {
        "item": mp, "categories": categories, "item_type": "metaprompt",
        "mode": mode, "form_action": form_action,
    })


@login_required
def save_categories(request, pk):
    mp = get_object_or_404(Metaprompt, pk=pk, owner=request.user)
    if request.method == "POST":
        tag_ids = request.POST.getlist("category_tags")
        if not tag_ids or len(tag_ids) > 3:
            categories = Category.objects.all()
            form_action = reverse("metaprompt-save-categories", kwargs={"pk": pk})
            return render(request, "components/_category_modal.html", {
                "item": mp, "categories": categories,
                "error": "Select 1 to 3 categories.", "item_type": "metaprompt",
                "mode": "edit", "form_action": form_action,
            })
        mp.category_tags.set(tag_ids)
        messages.success(request, "Tags updated.")
    return redirect("metaprompt-edit", pk=mp.pk)


@login_required
def ai_categorize(request, pk):
    mp = get_object_or_404(Metaprompt, pk=pk, owner=request.user)
    suggested_names = generate_category_tags(mp.title, mp.content, mp.description)
    suggested = Category.objects.filter(name__in=suggested_names)
    return render(request, "metaprompts/_category_result.html", {
        "suggested": suggested, "metaprompt": mp,
    })
