from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView

from .crawler import crawler
from .models import Title, Category, Studio


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')

    def post(self, request, *args, **kwargs):
        titles = crawler('winter', '2021', 'tv')
        for title in titles:
            # for key, value in title.items():
            #     print(key, ': ', value, '|', type(value))

            defaults = {**title}
            del defaults["data_id"]
            del defaults["categories"]
            del defaults["studios"]
            ttl, created = Title.objects.get_or_create(data_id=title['data_id'], defaults={**defaults})

            if created:
                for category in title["categories"]:
                    ctg, created = Category.objects.get_or_create(name=category)
                    ttl.categories.add(ctg)

                for studio in title["studios"]:
                    std, created = Studio.objects.get_or_create(name=studio)
                    ttl.studios.add(std)

        return redirect('main', permanent=True)


class RefreshView(View):
    pass
