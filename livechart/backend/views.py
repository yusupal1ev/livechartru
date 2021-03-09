from django.http import Http404
from django.shortcuts import render, redirect, get_list_or_404
from django.utils.text import slugify
from django.views.generic import View, TemplateView, ListView, DetailView

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
        titles, seasons = crawler('spring', '2021', 'tv')

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

        return redirect('crawler', permanent=True)

    @staticmethod
    def create_and_fill_category_and_studio(title_model, title):
        for category_name in title["categories"]:
            category, created = Category.objects.get_or_create(name=category_name, slug=slugify(category_name))
            title_model.categories.add(category)

        for studio_name in title["studios"]:
            studio, created = Studio.objects.get_or_create(name=studio_name, slug=slugify(studio_name))
            title_model.studios.add(studio)


class SeasonView(ListView):
    template_name = 'season.html'
    context_object_name = 'titles'

    def get_queryset(self):
        season = Season.objects.get(season=self.kwargs['season'], year=self.kwargs['year'])
        titles = get_list_or_404(Title, season=season)
        return titles

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        seasons = Season.objects.all()
        season = self.kwargs['season']
        year = self.kwargs['year']
        context["current_season"] = f"{season}-{year}"
        context["seasons"] = seasons
        return context


class TitleView(DetailView):
    model = Title
    context_object_name = 'title'
    template_name = 'title.html'
    pk_url_kwarg = 'data_id'

    def get_object(self, queryset=None):
        data_id = self.kwargs.get(self.pk_url_kwarg, None)
        try:
            anime = self.model.objects.get(data_id=data_id)
        except:
            raise Http404()
        return anime
