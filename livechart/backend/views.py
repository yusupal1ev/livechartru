from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, ListView

from .crawler import crawler
from .models import Title, Category, Studio, Season


class HomeView(TemplateView):
    def get(self, request, *args, **kwargs):
        seasons = Season.objects.all()

        context = {"seasons": seasons}
        return render(request, 'base.html', context=context)


class CrawlerView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'crawler.html')

    def post(self, request, *args, **kwargs):
        titles, seasons = crawler('winter', '2021', 'tv')

        for season in seasons:
            Season.objects.get_or_create(season=season["season"],
                                         year=season["year"],
                                         month_started=season["month_started"],
                                         month_ended=season["month_ended"],
                                         )

        for title in titles:
            title["season"] = Season.objects.get(season=title["season"], year=title["year"])
            del title["year"]
            defaults = {**title}
            del defaults["data_id"]
            del defaults["categories"]
            del defaults["studios"]
            title_model, created = Title.objects.update_or_create(data_id=title['data_id'], defaults={**defaults})

            if created:
                self.create_and_fill_category_and_studio(title_model, title)

        return redirect('main', permanent=True)

    @staticmethod
    def create_and_fill_category_and_studio(title_model, title):
        for category_name in title["categories"]:
            category, created = Category.objects.get_or_create(name=category_name)
            title_model.categories.add(category)

        for studio_name in title["studios"]:
            studio, created = Studio.objects.get_or_create(name=studio_name)
            title_model.studios.add(studio)


class SeasonView(ListView):
    model = Title
    template_name = 'season.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        season = self.kwargs['season']
        year = self.kwargs['year']
        context["season"] = f"{season}-{year}"
