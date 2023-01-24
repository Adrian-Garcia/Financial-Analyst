from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404

from .models import FundamentalAnalysis, Stock


class IndexView(generic.ListView):
    template_name = "stock_report/index.html"
    context_object_name = "fundamental_analysis_list"

    def get_queryset(self):
        return FundamentalAnalysis.objects.all()


def detail(request, fundamental_analysis_id):
    fundamental_analysis = get_object_or_404(
        FundamentalAnalysis, pk=fundamental_analysis_id
    )
    return render(
        request,
        "stock_report/detail.html",
        {"fundamental_analysis": fundamental_analysis},
    )
