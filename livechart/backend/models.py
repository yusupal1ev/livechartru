from django.db import models


class Title(models.Model):
    data_id = models.IntegerField()
    title_english = models.CharField(max_length=255)
    title_native = models.CharField(max_length=255)
    title_romaji = models.CharField(max_length=255)
    title_russian = models.CharField(max_length=255, blank=True, null=True)
    premiere = models.IntegerField()
    premiere_precision = models.IntegerField()
    rating = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    date = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    episodes = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    description_russian = models.TextField(blank=True, null=True)
    spoiler = models.BooleanField()
    image_url = models.CharField(max_length=1024)
    season = models.CharField(max_length=6)
    year = models.IntegerField()
    form = models.CharField(max_length=40)

    def __str__(self):
        if self.title_russian:
            return self.title_russian
        if self.title_english:
            return self.title_english
        elif self.title_romaji:
            return self.title_romaji
        else:
            return self.title_native

    class Meta:
        verbose_name = "Тайтл"
        verbose_name_plural = "Тайтлы"


class Category(models.Model):
    name = models.CharField(max_length=255)
    name_russian = models.CharField(max_length=255, blank=True, null=True)
    titles = models.ManyToManyField(Title, related_name='categories')

    def __str__(self):
        if self.name_russian:
            return self.name_russian
        else:
            return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Studio(models.Model):
    name = models.CharField(max_length=255)
    titles = models.ManyToManyField(Title, related_name='studios')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Студия"
        verbose_name_plural = "Студии"
