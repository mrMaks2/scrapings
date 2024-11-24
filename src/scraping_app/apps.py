from django.apps import AppConfig


class ScrapingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scraping_app'
    verbose_name = 'Приложение по сбору вакансий'
