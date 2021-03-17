from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.views.generic import TemplateView, ListView, DetailView

from .crawler import crawler
from .models import Anime, Category, Studio, Season
from .utils import CHOICES, get_current_season


class HomeView(TemplateView):
    def get(self, request, *args, **kwargs):
        seasons = Season.objects.all()
        if not seasons:
            raise Http404("There are not anime in this season")
        current_season = get_current_season(seasons=seasons)
        return redirect(current_season, permanent=True)


class CrawlerView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'crawler.html')

    def post(self, request, *args, **kwargs):
        titles, seasons = crawler('summer', '2021', 'tv')

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
            title_model, created = Anime.objects.update_or_create(data_id=title['data_id'], defaults={**defaults})

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


class AnimeListView(ListView):
    template_name = 'season.html'
    context_object_name = 'anime_list'
    paginate_by = 20
    paginate_orphans = 4
    ordering = '-rating'

    def get_ordering(self):
        if self.request.GET.get('order_by'):
            return self.request.GET["order_by"]
        return self.ordering

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = bool(self.request.GET.get("page"))
        context["order_by"] = self.get_order_by()
        context["choices"] = CHOICES
        context["ordering"] = self.get_ordering()
        context["seasons"] = Season.objects.all()

        return context

    def get_order_by(self):
        if self.request.GET.get('order_by'):
            return "order_by=" + self.get_ordering() + "&"
        else:
            return ""


class SeasonView(AnimeListView):
    def get_queryset(self):
        season = Season.objects.get(season=self.kwargs['season'], year=self.kwargs['year'])
        anime_list = Anime.objects.filter(season=season).order_by(self.get_ordering())
        if not anime_list:
            raise Http404("There are not anime in this season")

        return anime_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        season = context["seasons"].get(season=self.kwargs['season'], year=self.kwargs['year'])
        context["season"] = str(season)

        return context


class CategoryView(AnimeListView):
    template_name = 'anime_list.html'

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['category'])
        anime_list = Anime.objects.filter(categories=category).order_by(self.get_ordering())
        if not anime_list:
            raise Http404("There are not anime in this season")
        return anime_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.kwargs["category"]

        return context


class StudioView(AnimeListView):
    template_name = 'anime_list.html'

    def get_queryset(self):
        studio = get_object_or_404(Studio, slug=self.kwargs['studio'])
        anime_list = Anime.objects.filter(studios=studio).order_by(self.get_ordering())
        if not anime_list:
            raise Http404("There are not anime in this season")
        return anime_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["studio"] = self.kwargs["studio"]

        return context


class AnimeView(DetailView):
    model = Anime
    context_object_name = 'anime'
    template_name = 'anime.html'
    pk_url_kwarg = 'data_id'

    def get_object(self, queryset=None):
        data_id = self.kwargs.get(self.pk_url_kwarg, None)
        try:
            anime = self.model.objects.get(data_id=data_id)
        except:
            raise Http404()
        return anime

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        seasons = Season.objects.all()
        context["seasons"] = seasons
        return context
