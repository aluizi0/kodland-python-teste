import pgzrun
import time

# Define as dimensões da tela
WIDTH = 800
HEIGHT = 600

# Titulo do jogo
TITLE = "Teste Kodland - Etapa 4: Animação Simples"

# Define a simple actor (sprite)
class Player(Actor):

    # O método __init__ é o 'construtor', é chamado quando criamos o objeto
    def __init__(self, start_pos): # ATUALIZADO: Não precisa mais de 'image_file'
        # --- Carrega os frames de animação ---
        self.idle_frame = 'hero.png'      # Imagem de parado
        self.walk_frame = 'hero_walk.png' # Imagem de andando

        # Avisa ao 'Actor' para carregar a imagem e posição
        # 'Super()' chama o construtor da classe pai (Actor)
        # ATUALIZADO: Inicia com o frame 'idle'
        super().__init__(self.idle_frame, pos=start_pos)

        # Variáveis de física
        self.vy = 0  # Velocidade Vertical
        self.gravity = 1 # Força da Gravidade
        self.speed = 5 # Velocidade de Movimento Horizontal
        self.jump_strength = -15 # Força do Pulo (valor negativo para subir)
        self.on_ground = False # Indica se o jogador está no chão
        
        # --- Variáveis de Animação (NOVAS) ---
        self.animation_timer = time.time() # Timer para controlar a animação
        self.is_walking = False   # Flag para saber se está andando
        # self.flip_x FOI REMOVIDO

    # --- Nova Função de Animação ---
    def update_animation(self):
        # Se não estiver andando, usa a imagem de parado
        if not self.is_walking:
            self.image = self.idle_frame
            return # Para a função aqui

        # Se estiver andando, "pisca" entre as duas imagens
        # Isso cria a ilusão de animação ciclicamente (Requisito do Teste)
        now = time.time()
        if int(now * 10) % 2 == 0: # Alterna 5x por segundo
            self.image = self.walk_frame
        else:
            self.image = self.idle_frame
            
        # A lógica de 'angle' (que virava de cabeça para baixo) FOI REMOVIDA

    # ATUALIZADO: A lógica de 'update' agora controla a animação
    def update(self, platform_list):
        # Reseta o flag de 'andando' a cada frame
        self.is_walking = False 

        # Movimento lateral
        if keyboard.left:
            self.x -= self.speed
            self.is_walking = True # ATUALIZADO
            # self.flip_x FOI REMOVIDO
        if keyboard.right:
            self.x += self.speed
            self.is_walking = True # ATUALIZADO
            # self.flip_x FOI REMOVIDO

        # Pulo
        if keyboard.up and self.on_ground:
            self.vy = self.jump_strength
            self.on_ground = False # Sai do chão ao pular
        
        # Aplica a gravidade (ATUALIZADO: Física correta, gravidade sempre aplica)
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
        
        # --- ATUALIZAÇÃO FINAL ---
        # Chama a função de animação no final de toda a lógica
        self.update_animation()

# Definindo a posição inicial do jogador
posicao_inicial = (WIDTH // 2, HEIGHT // 2-100)

# Pgzero procura automaticamente por 'hero.png' na pasta 'images/'
# ATUALIZADO: O construtor mudou, não passamos mais a imagem aqui
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

# Lógica do jogo
def update():
    # Atualiza o jogador, passando a lista de plataformas para colisão
    hero.update(platforms)

# Desenhando elementos na tela
def draw():
    screen.fill((210, 240, 255)) # Cor de fundo (céu azul claro)
    
    for plat in platforms:
        plat.draw()  # Desenha cada plataforma
    
    hero.draw()  # Desenha o jogador

# Inicia o jogo
pgzrun.go()