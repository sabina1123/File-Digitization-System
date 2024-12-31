from django.apps import AppConfig


class FiledigitizationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'filedigitization'
    
    
    def ready(self):
        import filedigitization.signals
