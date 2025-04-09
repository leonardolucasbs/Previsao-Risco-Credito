from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')

def analise_credito(request):
    if request.method == 'POST':
        dados = {
            'nome': request.POST.get('nome'),
            'cpf': request.POST.get('cpf'),
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
            'possui_veiculo': 1 if request.POST.get('possui_veiculo') == 'sim' else 0,
            'risco_credito': request.POST.get('risco_credito'),
            'valor_solicitado': float(request.POST.get('valor_solicitado'))
        }
        return render(request, 'resultado.html', {'dados': dados})
    return redirect('home')
  