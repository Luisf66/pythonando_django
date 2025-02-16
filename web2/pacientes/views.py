from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import PAcientes, Tarefas, Consultas
from django.contrib import messages
from django.contrib.messages import constants
# Create your views here.
def pacientes(request):
    if request.method == 'GET':
        pacientes = PAcientes.objects.all()
        return render(request, 'pacientes.html', {'queixas': PAcientes.queixa_choices, 'pacientes': pacientes})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        queixa = request.POST.get('queixa')
        foto = request.FILES.get('foto')

        if len(nome.strip()) == 0 or not foto:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('pacientes')

        paciente = PAcientes(
            nome=nome,
            email=email,
            telefone=telefone,
            queixa=queixa,
            foto=foto
        )

        paciente.save()
        messages.add_message(request, constants.SUCCESS, 'Paciente cadastrado com sucesso')
        return redirect('pacientes')
    
def paciente_view(request, id):
    paciente = PAcientes.objects.get(id=id)
    if request.method == "GET":
        tarefas = Tarefas.objects.all()
        consultas = Consultas.objects.filter(paciente=paciente)
        return render(request, 'paciente.html', {'tarefas': tarefas, 'paciente': paciente, 'consultas': consultas})
    else:
        humor = request.POST.get('humor')
        registro_geral = request.POST.get('registro_geral')
        video = request.FILES.get('video')
        tarefas = request.POST.getlist('tarefas')

        consultas = Consultas(
            humor=int(humor),
            registro_geral=registro_geral,
            video=video,
            paciente=paciente
        )
        consultas.save()

        for i in tarefas:
            tarefa = Tarefas.objects.get(id=i)
            consultas.tarefas.add(tarefa)

        consultas.save()

        messages.add_message(request, constants.SUCCESS, 'Registro de consulta adicionado com sucesso.')
        return redirect(f'/pacientes/{id}')

    
def atualizar_paciente(request, id):
    pagamento_em_dia = request.POST.get('pagamento_em_dia')
    paciente = PAcientes.objects.get(id=id)

    if pagamento_em_dia == 'ativo':
        paciente.pagamento_em_dia = True
    else:
        paciente.pagamento_em_dia = False
    paciente.save()
    return redirect(f'/pacientes/{id}')

def excluir_consulta(request, id):
    consulta = Consultas.objects.get(id=id)
    consulta.delete()
    return redirect(f'/pacientes/{consulta.paciente.id}')

def consulta_publica(request, id):
    consulta = Consultas.objects.get(id=id)
    if not consulta.paciente.pagamento_em_dia:
        raise Http404()

    return render(request, 'consulta_publica.html', {'consulta': consulta})