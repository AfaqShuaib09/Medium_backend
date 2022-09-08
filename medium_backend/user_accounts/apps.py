from django.apps import AppConfig


class UserAccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_accounts'

    def ready(self):
        """ Import the signal on startup """
        import user_accounts.signals
