from django.db import models
from django.urls import reverse

# Create your models here.
class PAcientes(models.Model):
    queixa_choices = (
        ('TDAH', 'TDAH'),
        ('D', 'Depressão'),
        ('A', 'Ansiedade'),
        ('TAG', 'Transtorno de ansiedade generalizada')
    )

    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=50, null=True, blank=True)
    foto = models.ImageField(upload_to='fotos')
    pagamento_em_dia = models.BooleanField(default=True)
    queixa = models.CharField(max_length=4, choices=queixa_choices)

    def __str__(self):
        return self.nome
    
class Tarefas(models.Model):
    frequencia_choices = (
        ('D', 'Diário'),
        ('1S', '1 vez por semana'),
        ('2S', '2 vezes por semana'),
        ('3S', '3 vezes por semana'),
        ('N', 'Ao necessitar')
    )

    tarefa = models.CharField(max_length=100)
    instrucoes = models.TextField()
    frequencia = models.CharField(max_length=2, choices=frequencia_choices, default='D')

    def __str__(self):
        return self.tarefa
    
class Consultas(models.Model):
    humor = models.PositiveIntegerField()
    registro_geral = models.TextField()
    video = models.FileField(upload_to="video")
    tarefas = models.ManyToManyField(Tarefas)
    paciente = models.ForeignKey(PAcientes, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.paciente.nome
    

    @property
    def link_publico(self):
        return f"http://127.0.0.1:8000{reverse('consulta_publica', kwargs={'id': self.id})}"