import math

from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.safestring import SafeText

from app.forms import JogadaForm
from app.models import Jogada, Game


def start_game(request):
    if request.method == 'GET':
        return render(request, 'init_game.html')
    if request.method == 'POST':
        game = Game.criar_novo_game()

        return redirect('play_game', pk=game.id)


def play_game(request, pk=None):
    try:
        game = Game.objects.get(id=pk)
    except:
        return redirect('init_game')

    if request.method == "GET":
        form = JogadaForm()

    if request.method == "POST":
        linha = request.POST['linha']
        coluna = request.POST['coluna']
        borda = math.sqrt(game.tamanho)
        pass
        if not (int(linha) < 1 or int(linha) > int(borda)) or  not (int(coluna) < 1 or int(coluna) > int(borda)):
            if not Jogada.objects.filter(game=game, linha=linha, coluna=coluna):
                game.fazer_jogada(linha, coluna)



        form = JogadaForm()

    else:
        form = JogadaForm()

    jogadas = Jogada.objects.filter(game=game)

    table = '<table style="border-collapse: collapse; border: 1px solid black">'
    for l in range(1, 9):
        table += '<tr>'
        for c in range(1, 9):
            jogada = Jogada.objects.filter(game=game,linha=l, coluna=c)
            if jogada:
                table += f"""
                    <td style="border: 1px solid black">
                        <button>{jogada[0].value}</button>
                    </td>
                """
            else:
                table += f"""
                    <td style="border: 1px solid black">
                        <button>?</button>
                    </td>
                """
        table += '</tr>'

    table += '</table>'
    #transforma o elemento em html
    table = SafeText(table)


    context = {
        'form': form,
        'jogadas': jogadas,
        'table': table
    }
    return render(request, 'game.html', context)
