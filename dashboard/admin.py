from django.contrib import admin

from .models import Deck,Flashcard, Evento, Nivel, Prova, Vestibular, Caderno, Correcao, DayOfWeek, Planejamento

# Register your models here.

admin.site.register(Deck)

admin.site.register(Evento)
admin.site.register(Flashcard)

admin.site.register(Nivel)
admin.site.register(Vestibular)
admin.site.register(Prova)
admin.site.register(Caderno)
admin.site.register(Correcao)

admin.site.register(DayOfWeek)
admin.site.register(Planejamento)
