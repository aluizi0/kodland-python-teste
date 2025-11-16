import pgzrun
import time
import random 
import sys # Usado para fechar o jogo
from pygame import Rect # O import que faltava

# Define as dimens?es da tela
WIDTH = 800
HEIGHT = 600

# Titulo do jogo
TITLE = "Teste Kodland - Jogo de Plataforma"

# Define o estado inicial do jogo
game_state = "menu"

# Controla se a música está ligada ou desligada
music_on = True

# Define a simple actor (sprite)
class Player(Actor):

    # O método __init__ é o 'construtor', é chamado quando criamos o objeto
    def __init__(self, start_pos): 
        # Carrega os frames de animaç?o
        self.idle_frame = 'hero.png'      # Imagem de parado
        self.walk_frame = 'hero_walk.png' # Imagem de andando

        # Avisa ao 'Actor' para carregar a imagem e posiç?o
        super().__init__(self.idle_frame, pos=start_pos)

        # Variáveis de física
        self.vy = 0  # Velocidade Vertical
        self.gravity = 1 # Força da Gravidade
        self.speed = 5 # Velocidade de Movimento Horizontal
        self.jump_strength = -18 # Pulo mais forte
        self.on_ground = False # Indica se o jogador está no ch?o
        
        # Variáveis de Animaç?o
        self.animation_timer = time.time() # Timer para controlar a animaç?o
        self.is_walking = False   # Flag para saber se está andando

    # Nova Funç?o de Animaç?o
    def update_animation(self):
        # Se n?o estiver andando, usa a imagem de parado
        if not self.is_walking:
            self.image = self.idle_frame
            return # Para a funç?o aqui

        # Se estiver andando, "pisca" entre as duas imagens
        now = time.time()
        if int(now * 10) % 2 == 0: # Alterna 5x por segundo
            self.image = self.walk_frame
        else:
            self.image = self.idle_frame

    # Lógica de 'update' agora controla a animaç?o
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
            self.on_ground = False # Sai do ch?o ao pular
            try:
                sounds.jump.play() # Toca o som de pulo
            except:
                pass # Ignora se o som falhar
        
        # Aplica a gravidade
        self.vy += self.gravity
        self.y += self.vy

        # Verifica colis?o com plataformas
        self.on_ground = False

        for plat in platform_list:
            # Verifica se está colidindo com a plataforma
            if self.colliderect(plat) and self.vy >= 0:
                # Verifica se a colis?o é por cima (evita grudar na lateral)
                if self.bottom <= plat.top + 20: 
                    # Colidiu com a plataforma, ajusta a posiç?o
                    self.bottom = plat.top
                    self.vy = 0 # Zera a velocidade vertical
                    self.on_ground = True # Está no ch?o
                    break
        
        # Chama a funç?o de animaç?o no final de toda a lógica
        self.update_animation()

# Define a classe do inimigo
class Enemy(Actor):
    
    # Construtor da classe Inimigo
    def __init__(self, start_pos, patrol_range=100):
        # Carrega os frames de animaç?o do Inimigo
        self.idle_frame = 'enemy.png'      # Imagem do inimigo parado
        self.walk_frame = 'enemy_walk.png' # Imagem do inimigo andando

        # Inicia o Actor com o frame parado
        super().__init__(self.idle_frame, pos=start_pos)
        
        # Variáveis de Patrulha
        self.speed = 2          # Velocidade do inimigo
        self.direction = 1      # 1 = direita, -1 = esquerda
        self.patrol_range = patrol_range # Distância que ele anda
        self.start_x = self.x   # Posiç?o X inicial
        
        # Variáveis de Animaç?o
        self.animation_timer = time.time()

    # Animaç?o do Inimigo (sempre animando)
    def update_animation(self):
        now = time.time()
        # O inimigo pisca entre as duas imagens
        if int(now * 5) % 2 == 0: # Alterna 2.5x por segundo
            self.image = self.walk_frame
        else:
            self.image = self.idle_frame

    # Lógica de atualizaç?o do Inimigo
    def update(self):
        # Movimento de patrulha
        self.x += self.speed * self.direction
        
        # Verifica se atingiu o limite da patrulha
        if self.x > self.start_x + self.patrol_range:
            self.direction = -1 # Vira para a esquerda
        elif self.x < self.start_x - self.patrol_range:
            self.direction = 1  # Vira para a direita
            
        # Chama a funç?o de animaç?o
        self.update_animation()

# Criaç?o dos Objetos e Nível

# Definindo a posiç?o inicial do jogador (o seu "Começo")
posicao_inicial = (70, 500)

# Pgzero procura automaticamente por 'hero.png' na pasta 'images/'
hero = Player(posicao_inicial)

# Armazena todas as plataformas do nosso nível
platforms = []

# criar a fileira de 5 blocos de baixo (mais espaçada)
for i in range(5):
    # Posiç?es X: 70, 210, 350, 490, 630
    x_pos = 70 + (i * 140)  
    y_pos = HEIGHT - 35    # Posiç?o vertical do ch?o
    plat = Actor('platform.png', pos=(x_pos, y_pos))
    platforms.append(plat)

# criar a fileira de 4 blocos de cima (no meio dos v?os)
for i in range(4):
    # CORREÇ?O: Posiç?es X: 140, 280, 420, 560
    x_pos = 140 + (i * 140)  
    y_pos = HEIGHT - 180   # Plataformas mais baixas
    plat = Actor('platform.png', pos=(x_pos, y_pos))
    platforms.append(plat)

# Armazena todos os inimigos
enemies = []

# Cria o inimigo de baixo (patrulha as 3 casas do meio)
# Centro: X=350. Alcance: 140 (de 210 a 490)
enemy_pos_1 = (350, HEIGHT - 70) 
enemy1 = Enemy(enemy_pos_1, patrol_range=140) 
enemies.append(enemy1)

# Cria o inimigo de cima (patrulha todas as 4 casas de cima)
# CORREÇ?O: Centro da patrulha: X=350 (entre 280 e 420)
# CORREÇ?O: Alcance da patrulha: 210 (de 140 a 560)
enemy_pos_2 = (350, HEIGHT - 215) 
enemy2 = Enemy(enemy_pos_2, patrol_range=210)
enemies.append(enemy2)

# Cria o objetivo final (o seu "Fim!")
# Posiç?o: no último bloco da plataforma de baixo (X=630)
goal_pos = (630, HEIGHT - 70) # Posiç?o X do último bloco
goal = Actor('goal.png', pos=goal_pos)


# Define os bot?es do Menu
start_button = Rect((WIDTH/2 - 100, HEIGHT/2 - 50), (200, 50))
sound_button = Rect((WIDTH/2 - 100, HEIGHT/2 + 20), (200, 50))
quit_button = Rect((WIDTH/2 - 100, HEIGHT/2 + 90), (200, 50))

# Funç?es principais do jogo (update e draw)

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
            
        # Verifica colis?o do herói com inimigos
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
                
        # Verifica se o herói tocou o objetivo (Fim!)
        if hero.colliderect(goal):
            print("NÍVEL CONCLUÍDO!")
            game_state = "menu" # Volta para o menu
            hero.pos = posicao_inicial # Reseta o herói
            hero.vy = 0


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
        
        # Desenha os bot?es
        screen.draw.filled_rect(start_button, "green")
        screen.draw.text("Começar o Jogo", 
                         center=start_button.center, 
                         fontsize=30, color="black")
        
        screen.draw.filled_rect(sound_button, "yellow")
        # Mostra o texto do bot?o de som (ligado ou desligado)
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
            
        goal.draw() # Desenha o objetivo (a porta/chave)
            
        hero.draw()  # Desenha o jogador

# Funç?o de clique do mouse (só funciona no menu)
def on_mouse_down(pos):
    global game_state, music_on
    
    # Só processa cliques se estivermos no menu
    if game_state == "menu":
        
        # Se clicou no bot?o "Começar"
        if start_button.collidepoint(pos):
            game_state = "game" # Muda o estado para 'game'
            # Toca a música AGORA, quando o jogo começa
            try:
                # Vamos tentar tocar o MP3 que voc? baixou
                music.play('music.mp3') 
                music.set_volume(0.2)
            except Exception as e:
                print(f"Aviso: N?o foi possível tocar a música: {e}")
                print("Verifique se 'music.mp3' está na pasta 'music/'")
        
        # Se clicou no bot?o "Sair"
        if quit_button.collidepoint(pos):
            sys.exit() # Fecha o jogo
            
        # Se clicou no bot?o "Música"
        if sound_button.collidepoint(pos):
            music_on = not music_on # Inverte o valor
            if music_on:
                music.unpause()
            else:
                music.pause()

# Inicia o jogo
pgzrun.go()