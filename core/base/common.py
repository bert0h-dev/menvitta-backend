from django.db.models import Model

def GetModelName(instance: Model) -> str:
    """
    Retorna el nombre completo del modelo en formato 'app_label.model_name'.

    Args:
        instance (Model): Instancia de un modelo de Django.

    Returns:
        str: Nombre completo del modelo, ej. 'auth.user'
    """
    model = instance.__class__
    return f"{model._meta.app_label}.{model._meta.model_name}"