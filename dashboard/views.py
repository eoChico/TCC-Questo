from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DeckForm, EventoForm, PlannerForm
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from .models import Evento, Deck, Nivel, Vestibular, Prova, Caderno, Correcao, DayOfWeek, Planejamento
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime, time
import json
from django.utils.html import format_html
from django.forms.models import model_to_dict

# Create your views here.
def home(request):
    return render(request,'home.html')

@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
@csrf_exempt
def calendar(request):    
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.usuario = request.user
            data_selecionada = request.POST.get('data')
            evento.data = data_selecionada
            evento.save()
            return redirect('calendar')
    else:
        form = EventoForm()

    if 'dataAtiva' in request.POST:
        data_selecionada = request.POST.get('dataAtiva')
        data_selecionada = datetime.strptime(data_selecionada, '%Y-%m-%d').date()

        eventos = Evento.objects.filter(usuario=request.user, data=data_selecionada).order_by('hora')
        eventos_dict = [model_to_dict(evento) for evento in eventos]
        lista_data_evento = [evento.data.strftime('%Y-%m-%d') for evento in eventos]

        context = {'eventos': eventos_dict, 'lista_data_evento': lista_data_evento}
        return JsonResponse(context)
    else:
        form = EventoForm()
        eventos_marcados = Evento.objects.filter(usuario=request.user)
        datas_eventos = [evento.data for evento in eventos_marcados]
        lista_data_evento = [data.strftime('%Y-%m-%d') for data in datas_eventos]

        eventos = Evento.objects.filter(usuario=request.user, data=date(2024, 4, 30))

        context = {'form': form, 'datas_eventos': datas_eventos, 'lista_data_evento': lista_data_evento, 'eventos': eventos}
        return render(request, 'calendar.html', context=context)

@login_required
def detalhes_event(request):
    if request.method == 'GET':
        evento_id = request.GET.get('eventoId')

        try:
            evento = Evento.objects.get(id=evento_id, usuario=request.user)
            # Retornar os detalhes do evento em formato JSON
            return JsonResponse({'titulo': evento.titulo, 'descricao': evento.descricao, 'hora': evento.hora})  # Adicione outros campos conforme necessário
        except Evento.DoesNotExist:
            return JsonResponse({'error': 'Evento não encontrado ou você não tem permissão para acessá-lo.'})
    return JsonResponse({'error': 'Método de requisição não suportado.'})

def detalhes_event(request):
    if request.method == 'GET':
        evento_id = request.GET.get('eventoId')

        try:
            evento = Evento.objects.get(id=evento_id, usuario=request.user)
            return JsonResponse({'titulo': evento.titulo, 'descricao': evento.descricao, 'hora': evento.hora, 'data': evento.data})  # Adicione outros campos conforme necessário
        except Evento.DoesNotExist:
            return JsonResponse({'error': 'Evento não encontrado ou você não tem permissão para acessá-lo.'})
    return JsonResponse({'error': 'Método de requisição não suportado.'})

@login_required
@csrf_exempt
def edit_event(request):
    if request.method == 'POST':
        evento_id = request.POST.get('eventoId')
        novo_titulo = request.POST.get('novoTitulo')
        nova_descricao = request.POST.get('novaDescricao')
        nova_hora = datetime.strptime(request.POST.get('novaHora'), "%H:%M").time()
        nova_data = datetime.strptime(request.POST.get('novaData'), "%Y-%m-%d").date()

        try:
            evento = Evento.objects.get(id=evento_id, usuario=request.user)
            evento.titulo = novo_titulo
            evento.descricao = nova_descricao
            evento.hora = nova_hora
            evento.data = nova_data
            evento.save(update_fields=['titulo', 'descricao', 'hora', 'data'])
            
            return JsonResponse({'status': 'success', 'message': 'Evento editado com sucesso!'})
        except Evento.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Evento não encontrado ou você não tem permissão para editá-lo.'})
    return JsonResponse({'status': 'error', 'message': 'Método de requisição não suportado.'})

@login_required
@csrf_exempt
def delete_event(request):
    if request.method == 'POST':
        evento_id = request.POST.get('eventoId')
        try:
            evento = Evento.objects.get(id=evento_id, usuario=request.user)
            evento.delete()
            return JsonResponse({'status': 'success', 'message': 'Evento excluído com sucesso!'})
        except Evento.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Evento não encontrado ou você não tem permissão para excluí-lo.'})
    return JsonResponse({'status': 'error', 'message': 'Método de requisição não suportado.'})

@login_required
def flashcards(request):
    decks = Deck.objects.filter(usuario=request.user)
    if request.method == 'POST':
        deck_form = DeckForm(request.POST)  # Inicialize o formulário com os dados submetidos
        if deck_form.is_valid():  # Verifique se o formulário é válido
            deck = deck_form.save(commit=False)  # Salve os dados do formulário sem commit no banco de dados
            deck.usuario = request.user  # Atribua o usuário atual ao deck
            deck.save()  # Salve o deck no banco de dados
            return redirect('flashcards')
    else:
        deck_form = DeckForm()  # Caso contrário, crie um formulário em branco para ser exibido
    
    # Renderize o template com o formulário e os decks do usuário atual
    return render(request, 'flashcards.html', {'decks': decks, 'deck_form': deck_form})

@login_required
def flashcards_details(request,deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    return render(request, 'flashcards_details.html', {'deck': deck})



@login_required
def deletar_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    if request.method == 'POST':
        deck.delete()
        return redirect('flashcards')
    return redirect('flashcards')

@login_required
def exams(request):
    niveis = Nivel.objects.all()
    return render(request, 'exams.html', {'niveis': niveis})



@login_required
def planner(request):
    form = PlannerForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        planejamento = form.save(commit=False)
        planejamento.usuario = request.user
        planejamento.save()
        form.save_m2m()
        return redirect('planner')
    dias_semana = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado']
    planejamentos_por_dia = {dia.lower(): Planejamento.objects.filter(days_of_week__name=dia, usuario=request.user).order_by('hora') for dia in dias_semana}
    return render(request, 'planner.html', {'form': form, 'planejamentos': planejamentos_por_dia})

@login_required
def deletar_planejamentos(request):
    if request.method == 'POST':
        planejamentos_ids = set(request.POST.getlist('planejamentos'))
        if planejamentos_ids:
            try:
                Planejamento.objects.filter(id__in=planejamentos_ids).delete()
            except:
                return redirect('planner')
    return redirect('planner')