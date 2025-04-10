import joblib
from django.conf import settings


def load_ml_model_svm():
    """Carrega o modelo de machine learning uma vez durante o startup"""
    try:
        model_svm = joblib.load(settings.MODEL_PATH_SVM)
        return model_svm
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        return None

def load_ml_model_logistic():
    """Carrega o modelo de machine learning uma vez durante o startup"""
    try:
        model_logistic = joblib.load(settings.MODEL_PATH_LOGISTIC)
        return model_logistic
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        return None

# Carrega o modelo quando o módulo é importado
ml_model_svm = load_ml_model_svm()
ml_model_logistic = load_ml_model_logistic()