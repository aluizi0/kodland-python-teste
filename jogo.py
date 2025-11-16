import pgzrun
import time
import random 
import sys # Usado para fechar o jogo
from pygame import Rect # O import que faltava

# Define as dimensões da tela
WIDTH = 800
HEIGHT = 600

# Titulo do jogo
TITLE = "Teste Kodland - Jogo Completo"

# Define o estado inicial do jogo
game_state = "menu"

# Controla se a música está ligada ou desligada
music_on = True

# Define a simple actor (sprite)
class Player(Actor):

    # O método __init__ é o 'construtor', é chamado quando criamos o objeto
    def __init__(self, start_pos): 
        # Carrega os frames de animação
        self.idle_frame = 'hero.png'      # Imagem de parado
        self.walk_frame = 'hero_walk.png' # Imagem de andando

        # Avisa ao 'Actor' para carregar a imagem e posição
        super().__init__(self.idle_frame, pos=start_pos)

        # Variáveis de física
        self.vy = 0  # Velocidade Vertical
        self.gravity = 1 # Força da Gravidade
        self.speed = 5 # Velocidade de Movimento Horizontal
        self.jump_strength = -15 # Força do Pulo (valor negativo para subir)
        self.on_ground = False # Indica se o jogador está no chão
        
        # Variáveis de Animação
        self.animation_timer = time.time() # Timer para controlar a animação
        self.is_walking = False   # Flag para saber se está andando

    # Nova Função de Animação
    def update_animation(self):
        # Se não estiver andando, usa a imagem de parado
        if not self.is_walking:
            self.image = self.idle_frame
            return # Para a função aqui

        # Se estiver andando, "pisca" entre as duas imagens
        now = time.time()
        if int(now * 10) % 2 == 0: # Alterna 5x por segundo
            self.image = self.walk_frame
        else:
            self.image = self.idle_frame

    # Lógica de 'update' agora controla a animação
    def update(self, platform_list):
        # Reseta o flag de 'andando' a cada frame
        self.is_walking = False 

        # Movimento lateral
        if keyboard.left:
            self.x -= self.speed
            self.is_walking = True 
        if keyboard.right:
            self.x += self.speed
            self.is_walking = True 

        # Pulo
        if keyboard.up and self.on_ground:
            self.vy = self.jump_strength
            self.on_ground = False # Sai do chão ao pular
            try:
                sounds.jump.play() # Toca o som de pulo
            except:
                pass # Ignora se o som falhar
        
        # Aplica a gravidade
        self.vy += self.gravity
        self.y += self.vy

        # Verifica colisão com plataformas
        self.on_ground = False

        for plat in platforms:
            # Verifica se está colidindo com a plataforma
            if self.colliderect(plat) and self.vy >= 0:
                # Verifica se a colisão é por cima (evita grudar na lateral)
                if self.bottom <= plat.top + 20: 
                    # Colidiu com a plataforma, ajusta a posição
                    self.bottom = plat.top
                    self.vy = 0 # Zera a velocidade vertical
                    self.on_ground = True # Está no chão
                    break
        
        # Chama a função de animação no final de toda a lógica
        self.update_animation()

# Define a classe do inimigo
class Enemy(Actor):
    
    # Construtor da classe Inimigo
    def __init__(self, start_pos):
        # Carrega os frames de animação do Inimigo
        self.idle_frame = 'enemy.png'      # Imagem do inimigo parado
        self.walk_frame = 'enemy_walk.png' # Imagem do inimigo andando

        # Inicia o Actor com o frame parado
        super().__init__(self.idle_frame, pos=start_pos)
        
        # Variáveis de Patrulha
        self.speed = 2          # Velocidade do inimigo
        self.direction = 1      # 1 = direita, -1 = esquerda
        self.patrol_range = 100 # Distância que ele anda para cada lado
        self.start_x = self.x   # Posição X inicial
        
        # Variáveis de Animação
        self.animation_timer = time.time()

    # Animação do Inimigo (sempre animando)
    def update_animation(self):
        now = time.time()
        # O inimigo pisca entre as duas imagens
        if int(now * 5) % 2 == 0: # Alterna 2.5x por segundo
            self.image = self.walk_frame
        else:
            self.image = self.idle_frame

    # Lógica de atualização do Inimigo
    def update(self):
        # Movimento de patrulha
        self.x += self.speed * self.direction
        
        # Verifica se atingiu o limite da patrulha
        if self.x > self.start_x + self.patrol_range:
            self.direction = -1 # Vira para a esquerda
        elif self.x < self.start_x - self.patrol_range:
            self.direction = 1  # Vira para a direita
            
        # Chama a função de animação
        self.update_animation()

# Criação dos Objetos e Nível

# Definindo a posição inicial do jogador
posicao_inicial = (WIDTH // 2, HEIGHT // 2 - 100)

# Pgzero procura automaticamente por 'hero.png' na pasta 'images/'
hero = Player(posicao_inicial)

# Armazena todas as plataformas do nosso nível
platforms = []

# criar um chão de 10 blocos na parte de baixo da tela
for i in range(10):
    x_pos = 50 + (i * 70)  # Espaçamento entre blocos
    y_pos = HEIGHT - 35    # Posição vertical do chão
    plat = Actor('platform.png', pos=(x_pos, y_pos))
    platforms.append(plat)

# Plataforma flutuante
plat_flutuante = Actor('platform.png', pos=(WIDTH / 2, HEIGHT / 2))
platforms.append(plat_flutuante)

# Armazena todos os inimigos
enemies = []

# Cria um inimigo e o posiciona em cima do chão
enemy_pos = (200, HEIGHT - 70) 
enemy1 = Enemy(enemy_pos)
enemies.append(enemy1)

# Define os botões do Menu
# Usamos 'Rect' (Retângulos) para os botões clicáveis
start_button = Rect((WIDTH/2 - 100, HEIGHT/2 - 50), (200, 50))
sound_button = Rect((WIDTH/2 - 100, HEIGHT/2 + 20), (200, 50))
quit_button = Rect((WIDTH/2 - 100, HEIGHT/2 + 90), (200, 50))

# Funções principais do jogo (update e draw)

# Lógica do jogo (dividida por estado)
def update():
    global game_state # Avisa que vamos alterar a variável global
    
    # Se estivermos no estado 'game', rodamos a lógica do jogo
    if game_state == "game":
        # Atualiza o jogador
        hero.update(platforms)
        
        # Atualiza todos os inimigos
        for enemy in enemies:
            enemy.update()
            
        # Verifica colisão do herói com inimigos
        if hero.collidelist(enemies) != -1:
            # Se colidiu, "reinicia" o herói e toca som
            hero.pos = posicao_inicial
            hero.vy = 0 
            try:
                sounds.die.play() # Toca o som de morte
            except:
                pass
            
        # Verifica se o herói caiu para fora da tela
        if hero.top > HEIGHT:
            # Se caiu, "reinicia" o herói e toca som
            hero.pos = posicao_inicial
            hero.vy = 0
            try:
                sounds.die.play() # Toca o som de morte
            except:
                pass

# Desenhando elementos na tela (dividido por estado)
def draw():
    global game_state, music_on
    
    # Se estivermos no estado 'menu'
    if game_state == "menu":
        screen.fill((50, 50, 150)) # Fundo azul escuro
        
        # Desenha o título
        screen.draw.text("MEU JOGO DE PLATAFORMA", 
                         center=(WIDTH/2, HEIGHT/2 - 150), 
                         fontsize=50, color="white")
        
        # Desenha os botões
        screen.draw.filled_rect(start_button, "green")
        screen.draw.text("Começar o Jogo", 
                         center=start_button.center, 
                         fontsize=30, color="black")
        
        screen.draw.filled_rect(sound_button, "yellow")
        # Mostra o texto do botão de som (ligado ou desligado)
        sound_text = f"Música: {'LIGADA' if music_on else 'DESLIGADA'}"
        screen.draw.text(sound_text, 
                         center=sound_button.center, 
                         fontsize=30, color="black")
        
        screen.draw.filled_rect(quit_button, "red")
        screen.draw.text("Sair", 
                         center=quit_button.center, 
                         fontsize=30, color="black")

    # Se estivermos no estado 'game'
    elif game_state == "game":
        screen.fill((210, 240, 255)) # Cor de fundo (céu azul claro)
        
        for plat in platforms:
            plat.draw()  # Desenha cada plataforma
        
        for enemy in enemies:
            enemy.draw() # Desenha todos os inimigos
            
        hero.draw()  # Desenha o jogador

# Função de clique do mouse (só funciona no menu)
def on_mouse_down(pos):
    global game_state, music_on
    
    # Só processa cliques se estivermos no menu
    if game_state == "menu":
        
        # Se clicou no botão "Começar"
        if start_button.collidepoint(pos):
            game_state = "game" # Muda o estado para 'game'
            # Toca a música AGORA, quando o jogo começa
            try:
                # CORREÇÃO: Carregando o arquivo .MP3 original
                music.play('music.mp3') 
                music.set_volume(0.2)
            except Exception as e:
                print(f"Aviso: Não foi possível tocar a música: {e}")
                print("Verifique se 'music.mp3' está na pasta 'music/'")
        
        # Se clicou no botão "Sair"
        if quit_button.collidepoint(pos):
            sys.exit() # Fecha o jogo
            
        # Se clicou no botão "Música"
        if sound_button.collidepoint(pos):
            music_on = not music_on # Inverte o valor
            if music_on:
                music.unpause()
            else:
                music.pause()

# Inicia o jogo
pgzrun.go()