from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from orders.models import DesignRequest

@login_required
def profile_view(request):
    active_requests = (
        DesignRequest.objects
        .filter(user=request.user)
        .exclude(status__in=["completed", "cancelled"])
        .select_related("service")
        .prefetch_related("uploads")
        .order_by("-id")
    )
    completed_requests = (
        DesignRequest.objects
        .filter(user=request.user, status="completed")
        .select_related("service")
        .prefetch_related("uploads")
        .order_by("-id")
    )
    return render(
        request,
        "account/profile.html",
        {
            "active_requests": active_requests,
            "completed_requests": completed_requests,
        },
    )
