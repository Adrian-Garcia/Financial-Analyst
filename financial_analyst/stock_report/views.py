from django.shortcuts import render
from django.views import generic

from .models import FundamentalAnalysis, Stock


# class IndexView(generic.ListView):
#     template_name = "stock_report/index.html"
#     context_object_name = "fundamental_analysis_list"

#     def get_queryset(self):
#         return FundamentalAnalysis.objects.all()

def index(request):
    fundamental_analysis_list = FundamentalAnalysis.objects.all()
    return render(request, "stock_report/index.html", {
        "fundamental_analysis_list": fundamental_analysis_list
    })
