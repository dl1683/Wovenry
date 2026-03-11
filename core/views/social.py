from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.forms import ReportForm
from core.models import Metaprompt, Project


@login_required
def copy_metaprompt(request, pk):
    original = get_object_or_404(Metaprompt, pk=pk, visibility="public")
    if request.method == "POST":
        Metaprompt.objects.create(
            owner=request.user,
            title=f"{original.title} (Copy)",
            content=original.content,
            description=original.description,
            visibility="private",
            status="draft",
        )
        return redirect("home")
    return redirect("mixer", pk=pk)


@login_required
def copy_project(request, pk):
    original = get_object_or_404(Project, pk=pk, visibility="public")
    if request.method == "POST":
        Project.objects.create(
            owner=request.user,
            title=f"{original.title} (Copy)",
            description=original.description,
            visibility="private",
        )
        return redirect("home")
    return redirect("project-detail", pk=pk)


@login_required
def report(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            r = form.save(commit=False)
            r.reporter = request.user
            project_id = request.POST.get("project_id")
            metaprompt_id = request.POST.get("metaprompt_id")
            if project_id:
                r.project_id = int(project_id)
            if metaprompt_id:
                r.metaprompt_id = int(metaprompt_id)
            r.save()
            if request.htmx:
                return render(request, "components/_toast.html", {
                    "message": "Report submitted. Thank you.",
                    "type": "success",
                })
            return redirect("home")

    form = ReportForm()
    return render(request, "components/_report_form.html", {"form": form})
