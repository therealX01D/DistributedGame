import pygame
import pygame_gui
import Helpers
TRACK = pygame.image.load("imgs/track.png")
import Button as button


def take_username(txt):
    txt = str(txt)
    with open("username", "wb") as f:
        f.write(txt.encode())
def take_port(txt):
    txt = str(txt)
    with open("server_port", "wb") as f:
        f.write(txt.encode())


def get_user_name():
    pygame.init()
    pygame.font.init()
    MAIN_FONT = pygame.font.SysFont("sans-serif", 44)
    WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()

    text = MAIN_FONT.render(
        f"Enter Username", 1, (0, 0, 0))
    text_port = MAIN_FONT.render(
        f"Enter roomID", 1, (0, 0, 0))

    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("LOGIN Window | 1")
    pygame.display.update()
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    INPUT_HEIGHT = 50
    INPUT_WIDTH = 400
    text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((WIDTH/2-INPUT_WIDTH/2, HEIGHT/2-INPUT_HEIGHT/2-100),(INPUT_WIDTH, INPUT_HEIGHT)), manager=manager,
                                                     object_id='#main_text_entry')
    port_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((WIDTH/2-INPUT_WIDTH/2, HEIGHT/2-INPUT_HEIGHT/2 +100),(INPUT_WIDTH, INPUT_HEIGHT)), manager=manager,
                                                     object_id='#port_text_entry')
    start_img = pygame.image.load('imgs/start_btn.png').convert_alpha()
    startButton = button.Button(WIDTH-start_img.get_width()*0.5 - 10, HEIGHT -start_img.get_height()*0.5 -10, start_img,0.5)

    clock = pygame.time.Clock()
    done = False
    while True:
        UI_REFRESH_RATE = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            manager.process_events(event)

        manager.update(UI_REFRESH_RATE)
        SCREEN.fill("white")
        SCREEN.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() - 140))
        SCREEN.blit(text_port, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() +60))
        if startButton.draw(SCREEN):
            take_username(text_input.text)
            take_port(port_input.text)
            done = 1

        manager.draw_ui(SCREEN)

        pygame.display.update()
        if done:
            pygame.display.quit()
            break


