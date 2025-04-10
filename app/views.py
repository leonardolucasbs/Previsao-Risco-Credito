from django.shortcuts import render, redirect
from django.conf import settings
import numpy as np
import joblib
from .model_utils import ml_model_logistic, ml_model_svm

def home(request):
    return render(request, 'home.html')

def analise_credito(request):
    if request.method == 'POST':

        svm_model_path = settings.MODEL_PATH_SVM
        logistic_model_path = settings.MODEL_PATH_LOGISTIC
        preprocessor_path = settings.PREPROCESSOR_PATH

        model_SVM = joblib.load(svm_model_path)
        model_LOGISTIC = joblib.load(logistic_model_path)
        preprocessor = joblib.load(preprocessor_path)

        dados = {
            'nome': request.POST.get('nome'),
            'idade': int(request.POST.get('idade')),
            'renda_mensal': float(request.POST.get('renda_mensal')),
            'tempo_emprego': float(request.POST.get('tempo_emprego')),
            'dividas_total': float(request.POST.get('dividas_total')),
            'limite_cartao': float(request.POST.get('limite_cartao')),
            'historico_credito': float(request.POST.get('historico_credito')),
            'num_cartoes_credito': int(request.POST.get('num_cartoes_credito')),
            'num_emprestimos': int(request.POST.get('num_emprestimos')),
            'atraso_pagamento': int(request.POST.get('atraso_pagamento')),
            'possui_imovel': 1 if request.POST.get('possui_imovel') == 'sim' else 0,
            'possui_veiculo': 1 if request.POST.get('possui_veiculo') == 'sim' else 0
        }

        record = []
        for i in dados:
            if i == 'nome':
                continue
            else:
                record.append(dados[i])

        record = np.array(record).reshape(1, -1)
        record = preprocessor.transform(record)

        # Faz a predição
        result_SVM = model_SVM.predict(record)
        proba_SVM = model_SVM.predict_proba(record)

        # Interpreta o resultado

        if result_SVM  == 0:
            status_credit_SVM = "Alto"
        elif result_SVM  == 1:
            status_credit_SVM = "Baixo"
        elif result_SVM  == 2:
            status_credit_SVM = "Moderado"
        else:
            status_credit_SVM = "Desconhecido"

        confianca_SVM = max(proba_SVM[0]) *100 # pega a maior probabilidade

        # Faz a predição
        result_logistic = model_LOGISTIC.predict(record)
        proba_logistic = model_LOGISTIC.predict_proba(record)

        # Interpreta o resultado

        if result_logistic  == 0:
            status_credit_logistic = "Alto"
        elif result_logistic  == 1:
            status_credit_logistic = "Baixo"
        elif result_logistic  == 2:
            status_credit_logistic = "Moderado"
        else:
            status_credit_logistic = "Desconhecido"

        confianca_logistic = max(proba_logistic[0]) *100 # pega a maior probabilidade

        # Adiciona os resultados ao contexto
        results = {
                'Nome': dados['nome'],
                'resultado_svm': status_credit_SVM,
                'confianca_svm': f"{confianca_SVM:.3f}",
                'resultado_logistic': status_credit_logistic,
                'confianca_logistic': f"{confianca_logistic:.3f}"
            }

        return render(request, 'resultado.html', {"results":results})
    return redirect('home')
  