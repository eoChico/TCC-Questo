from django import forms
from .models import Deck, Flashcard, Evento, Planejamento

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['nome', 'descricao']
        labels = {
            'nome': 'Nome do Deck',
            'descricao': 'Descrição do Deck',
        }

class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['pergunta', 'resposta']
        labels = {
            'pergunta': 'Pergunta',
            'resposta': 'Resposta',
        }

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'descricao', 'hora']
        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição',
            'hora': 'Hora',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'hora': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'class': 'form-control'}),
        }


class PlannerForm(forms.ModelForm):
    class Meta:
        model = Planejamento
        fields = ['name', 'days_of_week', 'hora']
        labels = {
            'name': 'Nome',
            'days_of_week': '‎ Dias da semana',
            'hora': 'Hora',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'days_of_week': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'hora': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'class': 'form-control'}),
        }
