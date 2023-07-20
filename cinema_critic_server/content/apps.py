from django.apps import AppConfig


class ContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cinema_critic_server.content'

    def ready(self):
        import cinema_critic_server.content.signals
