import pgzrun

# Define as dimensões da tela
WIDTH = 800
HEIGHT = 600

# Titulo do jogo
TITLE = "Teste Kodland - Etapa 3: Pulo e Plataformas"

# Define a simple actor (sprite)
class Player(Actor):

    # O método __init__ é o 'construtor', é chamado quando criamos o objeto
    def __init__(self , image_file, start_pos ):
        # Avisa ao 'Actor' para carregar a imagem e posição
        # 'Super()' chama o construtor da classe pai (Actor)
        super().__init__(image_file, pos=start_pos)

        # Variáveis de física
        self.vy = 0  # Velocidade Vertical
        self.gravity = 1 # Força da Gravidade
        self.speed = 5 # Velocidade de Movimento Horizontal
        self.jump_strength = -15 # Força do Pulo (valor negativo para subir)
        self.on_ground = False # Indica se o jogador está no chão
    
    def update(self, platform_list):

        # Movimento lateral
        if keyboard.left:
            self.x -= self.speed
        if keyboard.right:
            self.x += self.speed

        # Pulo
        if keyboard.up and self.on_ground:
            self.vy = self.jump_strength
            self.on_ground = False # Sai do chão ao pular
        
        # Aplica a gravidade
        if not self.on_ground:
            self.vy += self.gravity
            self.y += self.vy

        # Verifica colisão com plataformas
        self.on_ground = False

        for plat in platform_list:
            # Verifica se está colidindo com a plataforma
            if self.colliderect(plat) and self.vy >= 0:
                # Colidiu com a plataforma, ajusta a posição
                self.bottom = plat.top
                self.vy = 0 # Zera a velocidade vertical
                self.on_ground = True # Está no chão
                break

# Definindo a posição inicial do jogador
posicao_inicial = (WIDTH // 2, HEIGHT // 2)

# Pgzero procura automaticamente por 'hero.png' na pasta 'images/'
hero = Player('hero.png', posicao_inicial)

# Armazena todas as plataformas do nosso nível
platforms = []

# criar um chão de 10 blocos na parte de baixo da tela
for i in range(10):
    
    x_pos = 50 + (i * 70)  # Espaçamento entre blocos
    y_pos = HEIGHT - 35     # Posição vertical do chão

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