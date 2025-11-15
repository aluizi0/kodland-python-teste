import pgzrun

# Define as dimensões da tela
WIDTH = 800
HEIGHT = 600

# Titulo do jogo
TITLE = "Teste Kodland: Classes-Etapa 2"

# Define a simple actor (sprite)
class Player(Actor):

    # O método __init__ é o 'construtor', é chamado quando criamos o objeto
    def __init__(self , image_file, start_pos ):
        # Avisa ao 'Actor' para carregar a imagem e posição
        # 'Super()' chama o construtor da classe pai (Actor)
        super().__init__(image_file, pos=start_pos)

        # Variáveis de física (pertencem só ao player)
        self.vy = 0  # Velocidade Vertical
        self.gravity = 1 # Força da Gravidade

# Definindo a posição inicial do jogador
posicao_inicial = (WIDTH // 2, HEIGHT // 2)

# Pgzero procura automaticamente por 'hero.png' na pasta 'images/'
hero = Player('hero.png', posicao_inicial)

# Lógica do jogo
def update():
    # Aplicando a gravidade
    hero.vy += hero.gravity
    hero.y += hero.vy

    # Travar o jogador na tela('chão')
    if hero.bottom > HEIGHT:
        hero.bottom = HEIGHT
        hero.vy = 0 # Zera a velocidade ao tocar o chão

# Desenhando elementos na tela
def draw():
    screen.fill((210, 240, 255)) # Cor de fundo (céu azul claro)
    hero.draw() # Desenha o jogador

# Inicia o jogo
pgzrun.go()