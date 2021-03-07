from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView

from .crawler import crawler
from .models import Title, Category, Studio, Season


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')

    def post(self, request, *args, **kwargs):
        titles, seasons = crawler('winter', '2021', 'tv')

        for season in seasons:
            Season.objects.get_or_create(season=season["season"], year=season["year"])

        for title in titles:
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


class SeasonView(TemplateView):
    def get(self, request, *args, **kwargs):
        season = kwargs['season']
        year = kwargs['year']
        context = {'season': f"{season}-{year}"}
        return render(request, 'season.html', context=context)
