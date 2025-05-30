from django.apps import AppConfig


# Конфигурация приложения "meds"
# Это имя используется Django для регистрации и управления приложением
class MedsConfig(AppConfig):
    # Тип поля по умолчанию для моделей (используется для автоматических id)
    default_auto_field = 'django.db.models.BigAutoField'

    # Название приложения (должно совпадать с названием папки)
    name = 'meds'
