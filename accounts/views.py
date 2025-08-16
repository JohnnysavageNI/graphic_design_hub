from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from orders.models import DesignRequest


@login_required(login_url="/account/login/")
def profile_view(request):
    qs = DesignRequest.objects.select_related("service").filter(user=request.user)
    pending = qs.filter(status="pending")
    in_progress = qs.filter(status="in_progress")
    completed = qs.filter(status="completed").prefetch_related("uploads")
    ctx = {
        "pending": pending,
        "in_progress": in_progress,
        "completed": completed,
    }
    return render(request, "account/profile.html", ctx)
