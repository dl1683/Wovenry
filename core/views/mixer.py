from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from core.models import Metaprompt


@login_required
def view(request, pk):
    mp = get_object_or_404(Metaprompt, pk=pk)
    if mp.visibility == "private" and mp.owner != request.user:
        return render(request, "403.html", status=403)
    return render(request, "mixer/view.html", {"metaprompt": mp})
