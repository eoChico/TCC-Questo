from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import FlashcardForm,DeckForm, EventoForm, PlannerForm,NotesForm
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from .models import Evento,Flashcard, Deck, Nivel, Vestibular,Notes, Prova, Caderno, Correcao, DayOfWeek, Planejamento
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime, time
import json
from django.utils.html import format_html
from django.forms.models import model_to_dict
from django.utils import timezone
from django.template.loader import render_to_string


# Create your views here.
def home(request):
    return render(request,'home.html')

@login_required
def profile(request):
    eventos = Evento.objects.filter(usuario=request.user,data__gte=timezone.now())[:10]
    decks = Deck.objects.filter(usuario=request.user).count()
    notes = Notes.objects.filter(usuario=request.user).count()
    return render(request, 'profile.html',{'eventos':eventos,'decks':decks,'notes':notes})


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

@login_required
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

# Função para visualizar os detalhes do deck
@login_required
def flashcards_details(request, deck_id):
    # Obter o deck e os flashcards associados ao deck
    deck = get_object_or_404(Deck, id=deck_id)
    flashcards = Flashcard.objects.filter(deck=deck)

    # Criar um formulário vazio se o método for GET
    if request.method == 'POST':
        flashcards_form = FlashcardForm(request.POST)
        if flashcards_form.is_valid():
            # Salvar o flashcard com referência ao deck
            flashcard = flashcards_form.save(commit=False)
            flashcard.deck = deck
            flashcard.save()

            # Redirecionar para a mesma página para evitar reenvio do formulário
            return redirect('flashcards_details', deck_id=deck_id)
    else:
        flashcards_form = FlashcardForm()  # Formulário vazio para GET

    # Renderizar a página com o deck, flashcards e o formulário
    return render(
        request,
        'flashcards_details.html',
        {
            'deck': deck,
            'flashcards': flashcards,
            'flashcards_form': flashcards_form
        }
    )
# Função para deletar o deck
@login_required
def delete_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    if request.method == 'POST':
        deck.delete()
        return redirect('flashcards')
    return render(request, 'flashcards_details.html', {'deck': deck})
# Função para editar o deck
@login_required
def edit_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    if request.method == 'POST':
        form = DeckForm(request.POST, instance=deck)
        if form.is_valid():
            form.save()
            # Retorna uma resposta JSON com os novos dados do deck
            return JsonResponse({'nome': deck.nome, 'descricao': deck.descricao})
    else:
        form = DeckForm(instance=deck)
    return render(request, 'flashcards_details.html', {'form': form, 'deck': deck})
# Função para deletar o card
@login_required
def delete_flashcard(request, id):
    flashcard = get_object_or_404(Flashcard, id=id)
    flashcard.delete()
    return JsonResponse({'success': True})
# Função para editar o card
@login_required
def edit_flashcard(request, id):
    flashcard = get_object_or_404(Flashcard, id=id)
    if request.method == "POST":
        form = FlashcardForm(request.POST, instance=flashcard)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

    
    



@login_required
def exams(request):
    niveis = Nivel.objects.all()
    return render(request, 'exams.html', {'niveis': niveis})

@login_required
def vestibulares(request, pk):
    nivel = get_object_or_404(Nivel, pk=pk)
    vestibulares = nivel.vestibular_set.all()
    return render(request, 'vestibulares.html', {'nivel': nivel, 'vestibulares': vestibulares})

@login_required
def provas(request, pk):
    vestibulares = get_object_or_404(Vestibular, pk=pk)
    provas = vestibulares.prova_set.all()
    return render(request, 'provas.html', {'vestibulares': vestibulares, 'provas': provas})



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

    
@login_required
def notes(request):
    notes = Notes.objects.filter(usuario=request.user)
    if request.method == 'POST':
        notes_form = NotesForm(request.POST)  # Inicialize o formulário com os dados submetidos
        if notes_form.is_valid():  # Verifique se o formulário é válido
            notes = notes_form.save(commit=False)  # Salve os dados do formulário sem commit no banco de dados
            notes.usuario = request.user  # Atribua o usuário atual ao deck
            notes.save()  # Salve o deck no banco de dados
            return redirect('notes')
    else:
        notes_form = NotesForm()
    return render(request,'notes.html',{'notes':notes,'notes_form':notes_form})

@login_required
def notes_delete(request, note_id):
    if request.method == 'POST':
        note = get_object_or_404(Notes, id=note_id)
        note.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
@login_required
def notes_edit(request, note_id):
    note = get_object_or_404(Notes, id=note_id)
    if request.method == "POST":
        form = NotesForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'success': False}, status=401)
