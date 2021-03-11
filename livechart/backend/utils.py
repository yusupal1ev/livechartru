from datetime import datetime


def get_current_season(seasons):
    now = datetime.now()
    for season in seasons:
        if season.season_end_date > now > season.season_start_date:
            return season

