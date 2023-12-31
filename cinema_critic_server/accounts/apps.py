from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cinema_critic_server.accounts'

    def ready(self):
        import cinema_critic_server.accounts.signals
