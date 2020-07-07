from django.apps import AppConfig


class ContributeConfig(AppConfig):
    name = 'contribute'
    
    def ready(self):
        import contribute.hooks
        import contribute.crons
        import contribute.signals

