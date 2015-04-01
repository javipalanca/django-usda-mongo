from django.views.generic import DetailView, ListView

from .models import Food


class FoodList(ListView):
    model = Food


class FoodDetail(DetailView):
    model = Food
