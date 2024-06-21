from django.db import models
from django.contrib.auth.models import User
from colorfield.fields import ColorField

# Create your models here.
class Deck (models.Model):
    nome = models.CharField(max_length=11)
    descricao = models.TextField(max_length=70)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
    
class Flashcard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    pergunta = models.TextField(max_length=150)
    resposta = models.TextField(max_length=150)

    def __str__(self):
        return f"Flashcard: {self.pergunta}"
    

class Evento(models.Model):
    titulo = models.CharField(max_length=64)
    descricao = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return self.titulo
    


class Nivel(models.Model):
    ensino = models.CharField(max_length=200)
    def __str__(self):
        return self.ensino
    
class Vestibular(models.Model):
    nome = models.CharField(max_length=200)
    ensino = models.ForeignKey(Nivel, on_delete=models.CASCADE)
    urlImg = models.URLField()
    desc = models.TextField()
    def __str__(self):
        return self.nome

class Prova(models.Model):
    vestibular = models.ForeignKey(Vestibular, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    ano = models.IntegerField()
    def __str__(self):
        return self.titulo

class Caderno(models.Model):
    prova = models.ForeignKey(Prova, on_delete=models.CASCADE)
    numero = models.IntegerField()
    urlProva = models.URLField()
    def __str__(self):
        return f"Caderno {self.numero} da prova do {self.prova.titulo}"

class Correcao(models.Model):
    caderno = models.OneToOneField(Caderno, on_delete=models.CASCADE)
    urlCorrecao = models.URLField()
    def __str__(self):
        return f"Correção do caderno {self.caderno.numero} da prova do {self.caderno.prova.titulo}"



class Planejamento(models.Model):
    name = models.CharField(max_length=100)
    days_of_week = models.ManyToManyField('DayOfWeek', blank=True)  # tornando o campo opcional
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    hora = models.TimeField()
    def __str__(self):
        return self.name

class DayOfWeek(models.Model):
    name = models.CharField(max_length=15)
    def __str__(self):
        return self.name

class Notes(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    COLOR_CHOICES = [
        ("#000000", "Preto"),
        ("#3fa34d", "Verde"),
        ("#276fbf", "Azul"),
        ("#f9dc5c","Amarelo"),
        ("#fcab10","Laranja"),
        ("#f8333c","Vermelho"),
        ("#ee85b5","Rosa"),
        ("#9f6ba0","Roxo")


        # Adicione mais cores aqui
    ]
    color = models.CharField(max_length=7, choices=COLOR_CHOICES)
    def __str__(self):
        return self.content