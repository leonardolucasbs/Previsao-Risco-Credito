from django.shortcuts import render, redirect
from django.conf import settings
import numpy as np
import joblib
from .model_utils import ml_model

def home(request):
    return render(request, 'home.html')

def analise_credito(request):
    if request.method == 'POST':

        model_path = settings.MODEL_PATH
        preprocessor_path = settings.PREPROCESSOR_PATH

        model = joblib.load(model_path)
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
        result = model.predict(record)
        proba = model.predict_proba(record)

        # Interpreta o resultado

        if result == 0:
            status_credit = "Alto"
        elif result == 1:
            status_credit = "Baixo"
        elif result == 2:
            status_credit = "Moderado"
        else:
            status_credit = "Desconhecido"

        confianca = max(proba[0])*100  # pega a maior probabilidade

        # Adiciona os resultados ao contexto
        results = {
                'Nome': dados['nome'],
                'resultado': status_credit,
                'confianca': f"{confianca:.2f}",
            }

        return render(request, 'resultado.html', {"results":results})
    return redirect('home')
  