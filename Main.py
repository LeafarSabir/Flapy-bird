import pygame
import os
import random
import json
from datetime import datetime

TELA_LARGURA = 600
TELA_ALTURA = 700

IMAGEM_CANO = pygame.transform.scale2x(
    pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(
    pygame.image.load(os.path.join('imgs', 'base.png')))
bg_temp = pygame.transform.scale2x(
    pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGEM_BACKGROUND = pygame.transform.scale(bg_temp,
                                           (TELA_LARGURA, TELA_ALTURA))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(
        pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(
        pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(
        pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)
FONTE_MENU = pygame.font.SysFont('arial', 40)
FONTE_PEQUENA = pygame.font.SysFont('arial', 25)
FONTE_TITULO = pygame.font.SysFont('arial', 70)

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
CINZA = (128, 128, 128)
LARANJA = (255, 165, 0)


class ConfiguracaoJogo:

    def __init__(self):
        self.dificuldade = "facil"
        self.velocidade_cano = 3
        self.velocidade_chao = 3
        self.distancia_canos = 220
        self.intervalo_canos = 700
        self.high_score = self.carregar_high_score()
        self.som_ativado = False
        self.mostrar_fps = True

    def definir_dificuldade(self, nivel):
        self.dificuldade = nivel
        if nivel == "facil":
            self.velocidade_cano = 3
            self.velocidade_chao = 3
            self.distancia_canos = 220
            self.intervalo_canos = 700
        elif nivel == "medio":
            self.velocidade_cano = 5
            self.velocidade_chao = 5
            self.distancia_canos = 200
            self.intervalo_canos = 600
        elif nivel == "dificil":
            self.velocidade_cano = 7
            self.velocidade_chao = 7
            self.distancia_canos = 180
            self.intervalo_canos = 500

    def carregar_high_score(self):
        try:
            with open('high_score.json', 'r') as f:
                dados = json.load(f)
                return dados.get('high_score', 0)
        except FileNotFoundError:
            return 0

    def salvar_high_score(self, pontos):
        if pontos > self.high_score:
            self.high_score = pontos
            try:
                with open('high_score.json', 'w') as f:
                    json.dump(
                        {
                            'high_score': pontos,
                            'data':
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }, f)
            except Exception as e:
                print(f"Erro ao salvar high score: {e}")





class Conquista:

    def __init__(self):
        self.conquistas = {
            'primeiro_ponto': {
                'desbloqueada': False,
                'nome': 'Primeiro Voo',
                'descricao': 'Consiga 1 ponto'
            },
            'dez_pontos': {
                'desbloqueada': False,
                'nome': 'Voador Experiente',
                'descricao': 'Consiga 10 pontos'
            },
            'vinte_pontos': {
                'desbloqueada': False,
                'nome': 'Mestre dos Céus',
                'descricao': 'Consiga 20 pontos'
            },
            'trinta_pontos': {
                'desbloqueada': False,
                'nome': 'Lenda Voadora',
                'descricao': 'Consiga 30 pontos'
            },
        }
        self.carregar_conquistas()

    def verificar_conquistas(self, pontos):
        mensagens = []
        if pontos >= 1 and not self.conquistas['primeiro_ponto'][
                'desbloqueada']:
            self.conquistas['primeiro_ponto']['desbloqueada'] = True
            mensagens.append(self.conquistas['primeiro_ponto']['nome'])
        if pontos >= 10 and not self.conquistas['dez_pontos']['desbloqueada']:
            self.conquistas['dez_pontos']['desbloqueada'] = True
            mensagens.append(self.conquistas['dez_pontos']['nome'])
        if pontos >= 20 and not self.conquistas['vinte_pontos']['desbloqueada']:
            self.conquistas['vinte_pontos']['desbloqueada'] = True
            mensagens.append(self.conquistas['vinte_pontos']['nome'])
        if pontos >= 30 and not self.conquistas['trinta_pontos'][
                'desbloqueada']:
            self.conquistas['trinta_pontos']['desbloqueada'] = True
            mensagens.append(self.conquistas['trinta_pontos']['nome'])
        if mensagens:
            self.salvar_conquistas()
        return mensagens

    def carregar_conquistas(self):
        try:
            with open('conquistas.json', 'r') as f:
                dados = json.load(f)
                for chave, valor in dados.items():
                    if chave in self.conquistas:
                        self.conquistas[chave]['desbloqueada'] = valor
        except FileNotFoundError:
            pass

    def salvar_conquistas(self):
        try:
            dados = {
                chave: valor['desbloqueada']
                for chave, valor in self.conquistas.items()
            }
            with open('conquistas.json', 'w') as f:
                json.dump(dados, f)
        except Exception as e:
            print(f"Erro ao salvar conquistas: {e}")


class Passaro:
    IMGS = IMAGENS_PASSARO
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]
        self.vivo = True
        self.invencivel = False
        self.tempo_invencivel = 0

    def pular(self):
        if self.vivo:
            self.velocidade = -5.0 # Ajustar para melhor responsividade
            self.tempo = 0
            self.altura = self.y

    def mover(self):
        if not self.vivo:
            return

        self.tempo += 1
        deslocamento = 0.5 * (self.tempo**2) + self.velocidade * self.tempo

        if deslocamento > 14:
            deslocamento = 14
        elif deslocamento < 0:
            deslocamento -= 0.6

        self.y += deslocamento

        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

        if self.invencivel:
            self.tempo_invencivel -= 1
            if self.tempo_invencivel <= 0:
                self.invencivel = False

    def desenhar(self, tela):
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO * 4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO * 2

        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x,
                                                          self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)

        if self.invencivel and self.tempo_invencivel % 10 < 5:
            pass
        else:
            tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

    def morrer(self):
        self.vivo = False


class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x, config):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.config = config
        self.DISTANCIA = config.distancia_canos
        self.VELOCIDADE = config.velocidade_cano
        self.definir_altura()
        self.cor_destaque = None
        self.tempo_destaque = 0

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE
        if self.tempo_destaque > 0:
            self.tempo_destaque -= 1

    def desenhar(self, tela):
        if self.cor_destaque and self.tempo_destaque > 0:
            overlay = pygame.Surface(self.CANO_TOPO.get_size())
            overlay.set_alpha(100)
            overlay.fill(self.cor_destaque)
            tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
            tela.blit(overlay, (self.x, self.pos_topo))
            tela.blit(self.CANO_BASE, (self.x, self.pos_base))
            tela.blit(overlay, (self.x, self.pos_base))
        else:
            tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
            tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        if passaro.invencivel:
            return False

        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            self.cor_destaque = VERMELHO
            self.tempo_destaque = 10
            return True
        else:
            return False


class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y, config):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA
        self.config = config
        self.VELOCIDADE = config.velocidade_chao

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))


class Botao:

    def __init__(self, x, y, largura, altura, texto, cor_normal, cor_hover):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor_normal = cor_normal
        self.cor_hover = cor_hover
        self.cor_atual = cor_normal
        self.ativo = True

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor_atual, self.rect, border_radius=10)
        pygame.draw.rect(tela, BRANCO, self.rect, 3, border_radius=10)

        texto_renderizado = FONTE_MENU.render(self.texto, True, BRANCO)
        texto_rect = texto_renderizado.get_rect(center=self.rect.center)
        tela.blit(texto_renderizado, texto_rect)

    def verificar_hover(self, pos_mouse):
        if self.rect.collidepoint(pos_mouse):
            self.cor_atual = self.cor_hover
            return True
        else:
            self.cor_atual = self.cor_normal
            return False

    def verificar_clique(self, pos_mouse):
        return self.rect.collidepoint(pos_mouse) and self.ativo


class Menu:

    def __init__(self, tela, config):
        self.tela = tela
        self.config = config
        self.opcao_selecionada = 0
        self.botoes = []
        self.criar_botoes()

    def criar_botoes(self):
        self.botoes = [
            Botao(150, 280, 300, 60, "Jogar", VERDE, (0, 200, 0)),
            Botao(150, 360, 300, 60, "Dificuldade", AZUL, (0, 0, 200)),
            Botao(150, 440, 300, 60, "Conquistas", LARANJA, (200, 130, 0)),
            Botao(150, 520, 300, 60, "Sair", VERMELHO, (200, 0, 0))
        ]

    def desenhar(self):
        self.tela.blit(IMAGEM_BACKGROUND, (0, 0))

        titulo = FONTE_TITULO.render("FLAPPY BIRD", True, AMARELO)
        titulo_rect = titulo.get_rect(center=(TELA_LARGURA // 2, 120))

        sombra = FONTE_TITULO.render("FLAPPY BIRD", True, PRETO)
        sombra_rect = sombra.get_rect(center=(TELA_LARGURA // 2 + 3, 123))
        self.tela.blit(sombra, sombra_rect)
        self.tela.blit(titulo, titulo_rect)

        high_score_texto = FONTE_PEQUENA.render(
            f"Recorde: {self.config.high_score}", True, BRANCO)
        self.tela.blit(
            high_score_texto,
            (TELA_LARGURA // 2 - high_score_texto.get_width() // 2, 180))

        pos_mouse = pygame.mouse.get_pos()
        for botao in self.botoes:
            botao.verificar_hover(pos_mouse)
            botao.desenhar(self.tela)

        pygame.display.update()

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return 'sair'
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if self.botoes[0].verificar_clique(pos_mouse):
                    return 'jogar'
                elif self.botoes[1].verificar_clique(pos_mouse):
                    return 'dificuldade'
                elif self.botoes[2].verificar_clique(pos_mouse):
                    return 'conquistas'
                elif self.botoes[3].verificar_clique(pos_mouse):
                    return 'sair'
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                    return 'jogar'
        return None


class MenuDificuldade:

    def __init__(self, tela, config):
        self.tela = tela
        self.config = config
        self.botoes = []
        self.criar_botoes()

    def criar_botoes(self):
        self.botoes = [
            Botao(150, 280, 300, 60, "Fácil", VERDE, (0, 200, 0)),
            Botao(150, 360, 300, 60, "Médio", AZUL, (0, 0, 200)),
            Botao(150, 440, 300, 60, "Difícil", VERMELHO, (200, 0, 0)),
            Botao(150, 540, 300, 60, "Voltar", CINZA, (100, 100, 100))
        ]

    def desenhar(self):
        self.tela.blit(IMAGEM_BACKGROUND, (0, 0))

        titulo = FONTE_TITULO.render("DIFICULDADE", True, AMARELO)
        titulo_rect = titulo.get_rect(center=(TELA_LARGURA // 2, 120))
        self.tela.blit(titulo, titulo_rect)

        dificuldade_atual = FONTE_PEQUENA.render(
            f"Atual: {self.config.dificuldade.capitalize()}", True, BRANCO)
        self.tela.blit(
            dificuldade_atual,
            (TELA_LARGURA // 2 - dificuldade_atual.get_width() // 2, 180))

        pos_mouse = pygame.mouse.get_pos()
        for botao in self.botoes:
            botao.verificar_hover(pos_mouse)
            botao.desenhar(self.tela)

        pygame.display.update()

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return 'sair'
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if self.botoes[0].verificar_clique(pos_mouse):
                    self.config.definir_dificuldade('facil')
                    return 'menu'
                elif self.botoes[1].verificar_clique(pos_mouse):
                    self.config.definir_dificuldade('medio')
                    return 'menu'
                elif self.botoes[2].verificar_clique(pos_mouse):
                    self.config.definir_dificuldade('dificil')
                    return 'menu'
                elif self.botoes[3].verificar_clique(pos_mouse):
                    return 'menu'
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return 'menu'
        return None


class MenuConquistas:

    def __init__(self, tela, conquistas):
        self.tela = tela
        self.conquistas = conquistas
        self.botoes = []
        self.criar_botoes()

    def criar_botoes(self):
        self.botoes = [
            Botao(150, 620, 300, 60, "Voltar", CINZA, (100, 100, 100))
        ]

    def desenhar(self):
        self.tela.blit(IMAGEM_BACKGROUND, (0, 0))

        titulo = FONTE_MENU.render("CONQUISTAS", True, AMARELO)
        titulo_rect = titulo.get_rect(center=(TELA_LARGURA // 2, 80))
        self.tela.blit(titulo, titulo_rect)

        y_pos = 150
        for chave, dados in self.conquistas.conquistas.items():
            cor = VERDE if dados['desbloqueada'] else CINZA
            status = "✓" if dados['desbloqueada'] else "✗"

            texto = FONTE_PEQUENA.render(f"{status} {dados['nome']}", True,
                                         cor)
            self.tela.blit(texto, (50, y_pos))

            descricao = FONTE_PEQUENA.render(dados['descricao'], True, BRANCO)
            self.tela.blit(descricao, (80, y_pos + 30))

            y_pos += 80

        pos_mouse = pygame.mouse.get_pos()
        for botao in self.botoes:
            botao.verificar_hover(pos_mouse)
            botao.desenhar(self.tela)

        pygame.display.update()

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return 'sair'
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if self.botoes[0].verificar_clique(pos_mouse):
                    return 'menu'
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return 'menu'
        return None


class TelaGameOver:

    def __init__(self, tela, pontos, high_score):
        self.tela = tela
        self.pontos = pontos
        self.high_score = high_score
        self.botoes = []
        self.criar_botoes()
        self.overlay = self.criar_overlay()

    def criar_botoes(self):
        self.botoes = [
            Botao(150, 500, 300, 60, "Jogar Novamente", VERDE, (0, 200, 0)),
            Botao(150, 590, 300, 60, "Menu Principal", AZUL, (0, 0, 200)),
            Botao(150, 680, 300, 60, "Sair", VERMELHO, (200, 0, 0))
        ]

    def criar_overlay(self):
        overlay = pygame.Surface((TELA_LARGURA, TELA_ALTURA))
        overlay.set_alpha(180)
        overlay.fill(PRETO)

        titulo = FONTE_TITULO.render("GAME OVER", True, VERMELHO)
        titulo_rect = titulo.get_rect(center=(TELA_LARGURA // 2, 150))
        overlay.blit(titulo, titulo_rect)

        pontos_texto = FONTE_MENU.render(f"Pontuação: {self.pontos}", True,
                                         BRANCO)
        pontos_rect = pontos_texto.get_rect(center=(TELA_LARGURA // 2, 250))
        overlay.blit(pontos_texto, pontos_rect)

        high_texto = FONTE_MENU.render(f"Recorde: {self.high_score}", True,
                                       AMARELO)
        high_rect = high_texto.get_rect(center=(TELA_LARGURA // 2, 320))
        overlay.blit(high_texto, high_rect)

        if self.pontos >= self.high_score and self.pontos > 0:
            novo_recorde = FONTE_PEQUENA.render("NOVO RECORDE!", True, AMARELO)
            novo_rect = novo_recorde.get_rect(center=(TELA_LARGURA // 2, 370))
            overlay.blit(novo_recorde, novo_rect)

        return overlay

    def desenhar(self):
        self.tela.blit(self.overlay, (0, 0))

        pos_mouse = pygame.mouse.get_pos()
        for botao in self.botoes:
            botao.verificar_hover(pos_mouse)
            botao.desenhar(self.tela)

        pygame.display.update()

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return 'sair'
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if self.botoes[0].verificar_clique(pos_mouse):
                    return 'restart'
                elif self.botoes[1].verificar_clique(pos_mouse):
                    return 'menu'
                elif self.botoes[2].verificar_clique(pos_mouse):
                    return 'sair'
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE or evento.key == pygame.K_RETURN:
                    return 'restart'
                elif evento.key == pygame.K_ESCAPE:
                    return 'menu'
        return None


def desenhar_tela_jogo(tela,
                       passaro,
                       canos,
                       chao,
                       pontos,
                       config,
                       pausado=False,
                       fps=0,
                       overlay_pausa=None):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))

    for cano in canos:
        cano.desenhar(tela)

    chao.desenhar(tela)
    passaro.desenhar(tela)

    texto_pontos = FONTE_PONTOS.render(f"{pontos}", True, BRANCO)
    tela.blit(texto_pontos,
              (TELA_LARGURA // 2 - texto_pontos.get_width() // 2, 50))

    texto_high = FONTE_PEQUENA.render(f"Recorde: {config.high_score}", True,
                                      BRANCO)
    tela.blit(texto_high, (10, 10))

    if config.mostrar_fps:
        texto_fps = FONTE_PEQUENA.render(f"FPS: {int(fps)}", True, VERDE)
        tela.blit(texto_fps, (TELA_LARGURA - texto_fps.get_width() - 10, 10))

    if pausado and overlay_pausa:
        tela.blit(overlay_pausa, (0, 0))

    pygame.display.update()


def loop_jogo(tela, config, conquistas):
    passaro = Passaro(280, 400)
    chao = Chao(830, config)
    canos = [Cano(700, config)]
    pontos = 0
    relogio = pygame.time.Clock()
    rodando = True
    pausado = False
    mensagens_conquista = []
    tempo_mensagem = 0

    overlay_pausa = pygame.Surface((TELA_LARGURA, TELA_ALTURA))
    overlay_pausa.set_alpha(150)
    overlay_pausa.fill(PRETO)
    texto_pausa = FONTE_TITULO.render("PAUSADO", True, AMARELO)
    texto_rect = texto_pausa.get_rect(center=(TELA_LARGURA // 2,
                                              TELA_ALTURA // 2))
    overlay_pausa.blit(texto_pausa, texto_rect)
    instrucao = FONTE_PEQUENA.render("Pressione P para continuar", True,
                                     BRANCO)
    instrucao_rect = instrucao.get_rect(center=(TELA_LARGURA // 2,
                                                TELA_ALTURA // 2 + 80))
    overlay_pausa.blit(instrucao, instrucao_rect)

    while rodando:
        fps = relogio.get_fps()
        relogio.tick(45)  # Aumentar para 60 FPS para melhor responsividade

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return 'sair', pontos

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and not pausado:
                    passaro.pular()
                elif evento.key == pygame.K_p:
                    pausado = not pausado
                elif evento.key == pygame.K_ESCAPE:
                    return 'menu', pontos
                elif evento.key == pygame.K_f:
                    config.mostrar_fps = not config.mostrar_fps

        # Verificar teclas pressionadas em tempo real para melhor responsividade
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_SPACE] and not pausado and passaro.vivo:
            # Evitar múltiplos pulos muito rápidos
            if not hasattr(passaro, 'ultimo_pulo'):
                passaro.ultimo_pulo = 0
            if pygame.time.get_ticks() - passaro.ultimo_pulo > 150:  # Delay mínimo entre pulos
                passaro.pular()
                passaro.ultimo_pulo = pygame.time.get_ticks()

        if not pausado and passaro.vivo:
            passaro.mover()
            chao.mover()

            adicionar_cano = False
            remover_canos = []

            for cano in canos:
                if cano.colidir(passaro):
                    passaro.morrer()

                if not cano.passou and passaro.x > cano.x + cano.CANO_TOPO.get_width(
                ):
                    cano.passou = True
                    adicionar_cano = True

                cano.mover()

                if cano.x + cano.CANO_TOPO.get_width() < 0:
                    remover_canos.append(cano)

            if adicionar_cano:
                pontos += 1
                canos.append(Cano(config.intervalo_canos, config))
                novas_conquistas = conquistas.verificar_conquistas(pontos)
                if novas_conquistas:
                    mensagens_conquista.extend(novas_conquistas)
                    tempo_mensagem = 180

            for cano in remover_canos:
                canos.remove(cano)

            if (passaro.y +
                    passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                if passaro.vivo:
                    passaro.morrer()

        desenhar_tela_jogo(tela, passaro, canos, chao, pontos, config, pausado,
                           int(fps), overlay_pausa)

        if mensagens_conquista and tempo_mensagem > 0:
            for i, msg in enumerate(mensagens_conquista):
                texto_conquista = FONTE_PEQUENA.render(f"Conquista: {msg}!",
                                                       True, AMARELO)
                tela.blit(texto_conquista,
                          (TELA_LARGURA // 2 -
                           texto_conquista.get_width() // 2, 400 + i * 30))
            pygame.display.update()
            tempo_mensagem -= 1
            if tempo_mensagem == 0:
                mensagens_conquista.clear()

        if not passaro.vivo:
            pygame.time.wait(500)  # Reduzir delay após morte
            config.salvar_high_score(pontos)
            tela_game_over = TelaGameOver(tela, pontos, config.high_score)

            esperando = True
            while esperando:
                tela_game_over.desenhar()
                resultado = tela_game_over.processar_eventos()
                if resultado:
                    return resultado, pontos

    return 'sair', pontos


def main():
    pygame.init()
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pygame.display.set_caption("Flappy Bird - Edição Completa")

    config = ConfiguracaoJogo()
    conquistas = Conquista()

    estado_atual = 'menu'
    relogio = pygame.time.Clock()

    while True:
        if estado_atual == 'menu':
            menu = Menu(tela, config)
            while estado_atual == 'menu':
                menu.desenhar()
                acao = menu.processar_eventos()
                if acao == 'jogar':
                    estado_atual = 'jogo'
                elif acao == 'dificuldade':
                    estado_atual = 'dificuldade'
                elif acao == 'conquistas':
                    estado_atual = 'conquistas'
                elif acao == 'sair':
                    pygame.quit()
                    return
                relogio.tick(120)

        elif estado_atual == 'dificuldade':
            menu_dificuldade = MenuDificuldade(tela, config)
            while estado_atual == 'dificuldade':
                menu_dificuldade.desenhar()
                acao = menu_dificuldade.processar_eventos()
                if acao == 'menu':
                    estado_atual = 'menu'
                elif acao == 'sair':
                    pygame.quit()
                    return
                relogio.tick(120)

        elif estado_atual == 'conquistas':
            menu_conquistas = MenuConquistas(tela, conquistas)
            while estado_atual == 'conquistas':
                menu_conquistas.desenhar()
                acao = menu_conquistas.processar_eventos()
                if acao == 'menu':
                    estado_atual = 'menu'
                elif acao == 'sair':
                    pygame.quit()
                    return
                relogio.tick(120)

        elif estado_atual == 'jogo':
            resultado, pontos_finais = loop_jogo(tela, config, conquistas)
            if resultado == 'restart':
                estado_atual = 'jogo'
            elif resultado == 'menu':
                estado_atual = 'menu'
            elif resultado == 'sair':
                pygame.quit()
                return


if __name__ == '__main__':
    main()