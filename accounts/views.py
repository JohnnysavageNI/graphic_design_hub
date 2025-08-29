from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from orders.models import DesignRequest, OrderUpload
from .forms import DesignRequestEditForm


# ----- Forms -----
class RequestEditForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ["instructions"]
        widgets = {
            "instructions": forms.Textarea(
                attrs={"rows": 4}
            )
        }


def _can_edit(dr: DesignRequest) -> bool:
    return getattr(dr, "status", "pending") == "pending"


def _can_delete(dr: DesignRequest) -> bool:
    return getattr(dr, "status", "pending") in ("pending", "in_progress")


# ----- Views -----
@login_required
def profile_view(request):
    active = (
        DesignRequest.objects.filter(
            user=request.user,
            status__in=["pending", "in_progress"]
        )
        .order_by("-id")
        .prefetch_related("uploads", "service")
    )
    completed = (
        DesignRequest.objects.filter(
            user=request.user,
            status="completed"
        )
        .order_by("-id")
        .prefetch_related("uploads", "service")
    )
    return render(
        request,
        "account/profile.html",
        {
            "active_requests": active,
            "completed_requests": completed,
        },
    )


@login_required
def request_edit(request, pk):
    dr = get_object_or_404(DesignRequest, pk=pk, user=request.user)

    if request.method == "POST":
        form = RequestEditForm(request.POST, instance=dr)
        if form.is_valid():
            form.save()
            messages.success(request, "Request updated successfully.")
            return redirect("accounts:profile")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RequestEditForm(instance=dr)

    return render(
        request,
        "account/request_edit.html",
        {"dr": dr, "form": form},
    )


@login_required
@require_POST
def request_delete(request, pk: int):
    dr = get_object_or_404(DesignRequest, pk=pk, user=request.user)
    if not _can_delete(dr):
        messages.warning(
            request,
            "This request can no longer be deleted."
        )
        return redirect("accounts:profile")

    service_name = dr.service.name
    ref = dr.id
    dr.delete()
    messages.success(
        request,
        f"Deleted: {service_name} (Ref: #{ref})."
    )
    return redirect("accounts:profile")
