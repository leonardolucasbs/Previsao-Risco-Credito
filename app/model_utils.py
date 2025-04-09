import joblib
from django.conf import settings


def load_ml_model():
    """Carrega o modelo de machine learning uma vez durante o startup"""
    try:
        model = joblib.load(settings.MODEL_PATH)
        return model
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        return None

# Carrega o modelo quando o módulo é importado
ml_model = load_ml_model()