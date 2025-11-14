import pgzrun

# Define a simple game window
WIDTH = 800
HEIGHT = 600

#title of the game
TITLE = "Teste Kodland"

#function to draw on the screen
def draw():
    screen.fill((0, 0, 0))  # Fill the screen with black
    screen.draw.text("Hello, Kodland!", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="white")


# Start the game
pgzrun.go()