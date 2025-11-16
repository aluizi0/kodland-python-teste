## kodland-python-teste

Este projeto é um jogo de plataforma 2D completo, desenvolvido como parte do processo seletivo para Tutor de Python na Kodland. O jogo foi escrito em Python usando a biblioteca Pygame Zero (`pgzero`) e cumpre todos os requisitos técnicos da avaliação.

## Requisitos Cumpridos

O projeto atende a 100% dos requisitos solicitados:

* **Bibliotecas:** Utiliza apenas `pgzero`, `time`, `sys` e `random`, com a exceção permitida de `pygame.Rect`.
* **Gênero:** É um jogo de plataforma 2D (`Platformer`).
* **Classes (OOP):** O código é estruturado em classes `Player` e `Enemy` que herdam de `Actor`.
* **Animação de Sprite:** O herói e os inimigos possuem animação cíclica (2 frames) para os estados "parado" e "andando", cumprindo a nota de não ser apenas uma troca de imagem.
* **Inimigos:** Há múltiplos inimigos (`Enemy`) que patrulham um território definido (`patrol_range`).
* **Menu Principal:** O jogo possui um `game_state` que gerencia o menu com três botões funcionais:
    * **Começar o Jogo:** Inicia o jogo.
    * **Música:** Liga e desliga a música de fundo.
    * **Sair:** Fecha a aplicação.
* **Sons e Música:** O jogo possui música de fundo (`music/`), sons de pulo e morte (`sounds/`).
* **Mecânica Lógica:** O jogo tem um início, um fim (objetivo), e mecânicas de "morte" (por colisão ou queda) que reiniciam o nível.

## Como Rodar o Projeto

Este projeto foi desenvolvido com Python 3.12 e Pygame Zero.

**1. Clone o Repositório:**
```bash
git clone [URL_DO_SEU_REPOSITORIO_AQUI]
cd kodland_teste
```

**2. Crie um Ambiente Virtual (Recomendado):**
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

**3. Instale as Dependências: (A única dependência é o pgzero, que já inclui o pygame.)**
```bash
pip install pgzero
```

**4. Execute o Jogo: O jogo deve ser executado usando o runner do pgzero para carregar corretamente os assets (músicas, sons e imagens).**
```bash
pgzrun jogo.py
```
