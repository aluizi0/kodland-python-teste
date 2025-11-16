import pgzrun
import time
import random # Adicionando a biblioteca random (permitida)

# Define as dimensões da tela
WIDTH = 800
HEIGHT = 600

# Titulo do jogo
TITLE = "Teste Kodland - Etapa 5: Inimigos"

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
        
        # Aplica a gravidade
        self.vy += self.gravity
        self.y += self.vy

        # Verifica colisão com plataformas
        self.on_ground = False

        for plat in platform_list:
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

    # Cria o ator da plataforma e adiciona na lista
    plat = Actor('platform.png', pos=(x_pos, y_pos))
    platforms.append(plat)

plat_flutuante = Actor('platform.png', pos=(WIDTH / 2, HEIGHT / 2))
platforms.append(plat_flutuante)

# Armazena todos os inimigos
enemies = []

# Cria um inimigo e o posiciona em cima do chão
enemy_pos = (200, HEIGHT - 70) 
enemy1 = Enemy(enemy_pos)
enemies.append(enemy1)

# Lógica do jogo
def update():
    # Atualiza o jogador, passando a lista de plataformas para colisão
    hero.update(platforms)
    
    # Atualiza todos os inimigos
    for enemy in enemies:
        enemy.update()
        
    # Verifica colisão do herói com inimigos
    if hero.collidelist(enemies) != -1:
        # Se colidiu, "reinicia" o herói
        hero.pos = posicao_inicial
        hero.vy = 0 # Zera a velocidade de queda
        
    # Verifica se o herói caiu para fora da tela
    if hero.top > HEIGHT:
        # Se caiu, "reinicia" o herói
        hero.pos = posicao_inicial
        hero.vy = 0 # Zera a velocidade de queda

# Desenhando elementos na tela
def draw():
    screen.fill((210, 240, 255)) # Cor de fundo (céu azul claro)
    
    for plat in platforms:
        plat.draw()  # Desenha cada plataforma
    
    # Desenha todos os inimigos
    for enemy in enemies:
        enemy.draw()
        
    hero.draw()  # Desenha o jogador

# Inicia o jogo
pgzrun.go()