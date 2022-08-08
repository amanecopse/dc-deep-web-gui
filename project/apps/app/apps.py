from django.apps import AppConfig
# from background_task.models import Task
# from app.tasks import storePduData

# class AppConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'app'


class MyAppConfig(AppConfig):
    name = 'project.apps.app'
    verbose_name = 'My App Config'

    # def ready(self):
    #     from background_task.models import Task
    #     from app.tasks import storePduData

    #     tasks = Task.objects.filter(verbose_name="store_pdu")
    #     if len(tasks) == 0:
    #         storePduData(repeat=20, verbose_name="store_pdu")
    #     else:
    #         return
