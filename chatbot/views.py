# chatbot/views.py
from django.http import JsonResponse
from django.views import View
import google.generativeai as genai
from django.views.generic import TemplateView
from decouple import config # Em produção remova o 'from decouple import config'

# Página principal
class ChatbotView(TemplateView):
    template_name = 'chatbot/chatbot.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mensagem inicial que será exibida no front-end
        context['initial_message'] = "Olá! Como posso ajudá-lo hoje com suas finanças?"
        return context

# Configure o modelo usando a chave da variável de ambiente
api_key = config("GEMINI_API_KEY")
genai.configure(api_key=api_key)
# Em produção remova 'api_key = config("GEMINI_API_KEY")' e use o genai.configure(api_key="Chave API aqui!")
# pip install google-generativeai

generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction=(
        "Você é especialista em finanças e controle financeiro."
        "Seu objetivo é ajudar usuários a organizar e gerenciar seu dinheiro."
        "Oferecendo conselhos práticos, técnicas de planejamento financeiro e estratégias de investimento."
        "Sempre comunique-se em português de forma clara e objetiva."
        "Adequando suas respostas ao nível de conhecimento do usuário e mantendo um tom profissional."
    ),
)

class ChatbotAPI(View):
    # Histórico inicial com a mensagem de abertura
    chat_session = model.start_chat(
        history=[
            {"role": "model", "parts": ["Olá! Como posso ajudá-lo hoje com suas finanças?"]}
        ]
    )

    def post(self, request, *args, **kwargs):
        import json
        data = json.loads(request.body)
        user_input = data.get("message")

        if not user_input:
            return JsonResponse({"error": "Mensagem não fornecida"}, status=400)

        response = self.chat_session.send_message(user_input)
        model_response = response.text

        # Adiciona histórico
        self.chat_session.history.append({"role": "user", "parts": [user_input]})
        self.chat_session.history.append({"role": "model", "parts": [model_response]})

        return JsonResponse({"response": model_response})
