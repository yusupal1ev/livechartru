from datetime import datetime


CHOICES = [
    ('-rating', 'по рейтингу'),
    ('title_russian', 'по русскому названию'),
    ('title_english', 'по английскому названию'),
    ('title_romaji', 'по японскому названию')
]


def get_current_season(seasons):
    now = datetime.now()
    for season in seasons:
        if season.season_end_date > now > season.season_start_date:
            return season

