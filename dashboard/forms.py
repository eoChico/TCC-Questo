from django import forms
from .models import Deck, Flashcard, Evento, Planejamento,Notes
from colorfield.widgets import ColorWidget

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['nome', 'descricao']
        labels = {
            'nome': 'Nome do Deck',
            'descricao': 'Descrição do Deck',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
        }

class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['pergunta', 'resposta']
        labels = {
            'pergunta': 'Pergunta',
            'resposta': 'Resposta',
        }
        widgets = {
            'pergunta': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'resposta': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
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

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['content', 'color']
        labels = {
            'content': 'Conteúdo',
            'color': 'Cor',
        }
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'color': forms.Select(choices=Notes.COLOR_CHOICES),
        }