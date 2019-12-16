import math
from random import randint

from django.db import models
from django.utils import timezone

class Game(models.Model):
    tamanho = models.IntegerField()
    bombas = models.CharField(max_length=100)
    created_date = models.DateField(default=timezone.now)
    ended_date = models.DateField(null=True)


    def fazer_jogada(self, linha, coluna):
        linha = int(linha)
        coluna = int(coluna)
        posicao_jogada = self.obter_posicao_jogada(linha, coluna)
        posicao_jogada = int(posicao_jogada)
        bombas = [x.replace(' ', '') for x in self.bombas.split(',')]
        if str(posicao_jogada) in bombas:
            for bomba in bombas:
                coordenada = self.posicao_para_coordenada(bomba)
                jogada = Jogada()
                jogada.linha = int(coordenada['linha'])
                jogada.coluna = int(coordenada['coluna'])
                jogada.created_date = timezone.now()
                jogada.value = 'B'
                jogada.game = self
                jogada.save()
        else:
            jogada = Jogada()
            linha = int(linha)
            coluna = int(coluna)
            jogada.linha = linha
            jogada.coluna = coluna
            jogada.created_date = timezone.now()
            jogada.value = self.verificar_qts_bombas_redor(linha, coluna)
            jogada.game = self
            jogada.save()

    def verificar_qts_bombas_redor(self, linha, coluna):
        borda = math.sqrt(self.tamanho)
        bombas = [int(x.replace(' ', '')) for x in self.bombas.split(',')]
        list_linha = list(filter(lambda x: (x >= 1 and x <= borda), [linha - 1, linha, linha + 1]))
        list_coluna = list(filter(lambda x: (x >= 1 and x <= borda), [coluna - 1, coluna, coluna + 1]))
        # obtem todas as combinaçeõs possíveis
        comb_posicao = [[x, y] for x in list_linha for y in list_coluna]
        count_bombas = 0
        for posicao_linha_coluna in comb_posicao:
            posicao = self.obter_posicao_jogada(linha=posicao_linha_coluna[0], coluna=posicao_linha_coluna[1])
            if int(posicao) in bombas:
                count_bombas = count_bombas + 1
        return count_bombas


    def posicao_para_coordenada(self, posicao):
        borda = math.sqrt(self.tamanho)
        linha = int(int(posicao) / borda) + 1
        coluna = int(posicao) - ((linha - 1) * borda)

        if coluna == 0:
            linha = linha - 1
            coluna = borda
        return {'linha': linha, 'coluna': coluna}

    def obter_posicao_jogada(self, linha, coluna):
        borda = math.sqrt(self.tamanho)
        linha = linha - 1
        posicao_jogada = (linha * borda) + coluna
        return posicao_jogada

    @staticmethod
    def criar_novo_game(tamanho=8):
        game = Game()
        game.tamanho = tamanho ** 2
        game.bombas = str(game.criar_bombas()).replace('[', '').replace(']', '')
        game.save()
        return game

    def criar_bombas(self, area_bomba=20):

        porc_bomba = area_bomba / 100
        qtd_bomba = int(self.tamanho * porc_bomba)

        list_bombas = []

        while qtd_bomba > 0:
            self.verificar_posicao_bomba(posicao=randint(1, self.tamanho), list_bombas=list_bombas)
            qtd_bomba -= 1
        return list_bombas

    def verificar_posicao_bomba(self, posicao, list_bombas):
        if posicao in list_bombas:
            if posicao == self.tamanho:
                posicao = 0
            posicao += 1

            self.verificar_posicao_bomba(posicao, list_bombas)
            return
        list_bombas.append(posicao)

class Jogada(models.Model):
    linha = models.CharField(max_length=2)
    coluna = models.CharField(max_length=2)
    value = models.CharField(max_length=10, default='?')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)