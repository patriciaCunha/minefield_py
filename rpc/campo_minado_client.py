import time
import rpyc


def display_campo_minado(self):
    for display in self.display:
        print(display)

def start_game():
    # tamanho = input('Insira o tamanho do seu campo minado: ')
    # if int(tamanho) < 6:
    #     print('Tamanha mínimo aceitável é 6')
    #     return

    config = {'allow_public_attrs': True}
    cm = rpyc.connect('localhost', 18861, config=config)

    while True:
        for display in cm.root.get_display():
            print(display)
        print('\nFaça sua jogada: \n')
        linha = input('Escolha a linha:')
        coluna = input('Escolha a coluna:')
        cm.root.jogada(linha=int(linha),coluna=int(coluna))
        if cm.root.get_next_game():
            print(cm.root.get_message())
            print(cm.root.get_valor_qt_bomba_campo())
            continue
        else:
            for display in cm.root.get_display():
                print(display)
            print(cm.root.get_status())
            print(cm.root.get_message())

            time_sleep = 0.35
            print('-' * 39)
            time.sleep(time_sleep)
            print('-' * 39)
            time.sleep(time_sleep)
            print('-' * 39)
            time.sleep(time_sleep)
            print('-' * 39)
            time.sleep(time_sleep)
            print('-' * 39)
            break


def client():
    time_sleep = 0.35
    print('-' * 39)
    time.sleep(time_sleep)
    print('-' * 39)
    time.sleep(time_sleep)
    print('-' * 15 + 'Bem Vindo' + '-' * 15)
    time.sleep(time_sleep)
    print('-' * 39)
    time.sleep(time_sleep)
    print('-' * 39 + '\n')
    time.sleep(1)
    while True:
        print('Escolha as seguintes opções:\n')
        print('1) INICIAR JOGO\n')
        print('2) Sair')
        opcao = input('Escolha opção 1 ou 2: ')
        if opcao == '1':
            start_game()
            continue
        elif opcao == '2':
            print('Fim de Jogo')

            break
        else:
            print('opção incorreta')
            continue


