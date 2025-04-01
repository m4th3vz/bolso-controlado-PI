# staticpages/views.py
from django.views.generic import TemplateView
from django.shortcuts import render
import urllib.request
import json
from decouple import config

# Página de boas-vindas e API de dados da bolsa
class WelcomeView(TemplateView):
    template_name = 'staticpages/welcome.html'
    
    def get(self, request, *args, **kwargs):
        api_key = config('BOLSA_API_KEY')
        url = f'https://api.polygon.io/v1/open-close/I:NDX/2024-04-05?apiKey={api_key}'

        try:
            # Usando urllib para fazer a requisição
            with urllib.request.urlopen(url) as response:
                # Verifica se a requisição foi bem-sucedida
                if response.status != 200:
                    context = {'error': 'Erro ao consultar a API.'}
                    return render(request, self.template_name, context)

                # Lendo e decodificando a resposta
                data = json.loads(response.read().decode('utf-8'))

            # Verifica se o status da resposta é OK
            if data['status'] != 'OK':
                context = {'error': 'Erro na resposta da API.'}
                return render(request, self.template_name, context)

            # Contexto com os dados da API
            context = {
                'from': data['from'],
                'symbol': data['symbol'],
                'open': data['open'],
                'high': data['high'],
                'low': data['low'],
                'close': data['close'],
                'after_hours': data['afterHours'],
                'pre_market': data['preMarket']
            }

        except (urllib.error.URLError, json.JSONDecodeError) as e:
            # Exibe a mensagem de erro diretamente na página
            context = {'error': f'Ocorreu um erro: {str(e)}'}

        return render(request, self.template_name, context)

# Página de sobre
class AboutView(TemplateView):
    template_name = 'staticpages/about.html'

# Página de notícias
class NewsView(TemplateView):
    template_name = 'staticpages/news.html'

# Página de notícia 1
class News1View(TemplateView):
    template_name = 'staticpages/news1.html'

# Página de notícia 2
class News2View(TemplateView):
    template_name = 'staticpages/news2.html'
