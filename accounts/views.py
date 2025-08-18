from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from orders.models import DesignRequest


@login_required
def profile_view(request):
    in_progress = (
        DesignRequest.objects
        .filter(user=request.user, status__in=["pending", "in_progress"])
        .select_related("service")
        .prefetch_related("uploads")
        .order_by("-id")
    )
    completed = (
        DesignRequest.objects
        .filter(user=request.user, status="completed")
        .select_related("service")
        .prefetch_related("uploads")
        .order_by("-id")
    )
    return render(request, "account/profile.html", {"in_progress": in_progress, "completed": completed})
