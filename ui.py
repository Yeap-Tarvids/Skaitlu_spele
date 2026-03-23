from typing import Callable
import pygame as pg
import math
import base_code as spele
import Alfa_beta as AB

TITLE = "Mākslīgais Intelekts - 20. komanda"
WIDTH = 1280
HEIGHT = 720
WINDOWS_SIZE = (WIDTH, HEIGHT)
SEQ_LENGTH = 15
AI_MOVE = False

def lighten_color(color: pg.Color):
    intensity = 0.7
    r, g, b = color.r + (255 - color.r) * intensity, color.g + (255 - color.g) * intensity, color.b + (255 - color.b) * intensity
    return pg.Color(int(r), int(g), int(b))

class Button:
    def __init__(self, center: tuple, width: int =100, height: int =50, color: str | pg.Color | tuple[int, int, int] ="red", border_radius: int = 0, func: Callable | None = None, text: str =''):
        self.center_pivot = center
        self.width = width
        self.height = height
        self.color = pg.Color(color)
        self.hover_color = lighten_color(self.color)
        self.render_color = self.color
        self.func = func
        self.rect = pg.Rect(center[0]-(width//2),center[1]-(height//2), width, height)
        self.border_radius = border_radius
        self.text = text
        self.text_surface = pg.font.SysFont('Comic Sans MS', min(int(self.height*0.5), int(self.width*0.5))).render(text, True, "#000000")
    
    def draw(self, screen: pg.Surface):
        pg.draw.rect(screen, self.render_color, self.rect, border_radius=self.border_radius)
        screen.blit(self.text_surface, (self.center_pivot[0]-(self.text_surface.get_width()//2), self.center_pivot[1]-(self.text_surface.get_height()//2)))

    def mouse_over(self, mouse_pos: tuple[int, int]):
        return self.rect.collidepoint(mouse_pos)
    
    def call_back(self):
        if self.func:
            return self.func()
    
class Label:
    def __init__(self, center: tuple[int, int], text: str, font_size: int = 12, color: pg.Color = "#000000"):
        self.center_pivot = center
        self.text = text
        self.font_size = font_size
        self.color = color
        self.text_surface = pg.font.SysFont('Comic Sans MS', self.font_size).render(self.text, True, self.color)
    
    def draw(self, screen: pg.Surface):
        screen.blit(self.text_surface, (self.center_pivot[0]-(self.text_surface.get_width()//2), self.center_pivot[1]-(self.text_surface.get_height()//2)))

    def updateText(self, text):
        self.text = text
        self.text_surface = pg.font.SysFont('Comic Sans MS', self.font_size).render(self.text, True, self.color)

def setAIMove():
    global AI_MOVE
    AI_MOVE = not AI_MOVE

def main():

    pg.init()

    display = pg.display
    screen = display.set_mode(WINDOWS_SIZE)
    display.set_caption(TITLE)
    clock = pg.time.Clock()
    running = True
    
    game = spele.GameState(spele.generateVirkne(SEQ_LENGTH))

    def restart():
        nonlocal game
        game = spele.GameState(spele.generateVirkne(SEQ_LENGTH))
        nonlocal msg_box_text
        msg_box_text = ''

    def inc_length():
        global SEQ_LENGTH
        if SEQ_LENGTH >= 25:
            SEQ_LENGTH = 25
            return
        SEQ_LENGTH += 1

    def dec_length():
        global SEQ_LENGTH
        if SEQ_LENGTH <= 15:
            SEQ_LENGTH = 15
            return
        SEQ_LENGTH -= 1

    def pair_click(pair_index):
        game.sumPair(pair_index)
        setAIMove()

    center = (WINDOWS_SIZE[0]/2, WINDOWS_SIZE[1]/2)

    buttons = []
    labels = []

    seq_button_width = 80
    seq_button_height = 80
    pad_amount = int(seq_button_width * 0.1)
    padding = int(seq_button_width+pad_amount)
    
    msg_box_text = ''

    while running:
        if AI_MOVE:
            bestPair = AB.best_move(game)
            pair = game.virkne[(bestPair-1)*2:(bestPair-1)*2+2]
            pair_click(bestPair)
            msg_box_text = f'Dators izvēlējās {bestPair} pāri ({pair})'

        
        labels.clear()
        buttons.clear()

        punkti = Label(
            (center[0], center[0]-550),
            f'Punkti: {game.punkti}',
            40
        )

        banka = Label(
            (center[0], center[0]-500),
            f'Banka: {game.banka}' ,
            20
        )
        
        msg_box = Label(
            center,
            msg_box_text,
            30
        )

        length_label = Label(
            (center[0], center[1]+300),
            f'Virknes garums: {SEQ_LENGTH}',
            30
        )

        labels.append(punkti)
        labels.append(banka)
        labels.append(msg_box)
        labels.append(length_label)
    

        dec_color = "#e66b6b"
        inc_color = "#e66b6b"

        match SEQ_LENGTH:
            case 15:
                dec_color = "#747474"
            case 25:
                inc_color = "#747474"

        inc_button = Button(
            (center[0]+length_label.text_surface.get_width()//2+50, center[1]+300),
            50,
            50,
            inc_color,
            5,
            inc_length,
            '+'
        )

        dec_button = Button(
            (center[0]-length_label.text_surface.get_width()//2-50, center[1]+300),
            50,
            50,
            dec_color,
            5,
            dec_length,
            '-'
        )

        buttons.append(inc_button)
        buttons.append(dec_button)
        buttons.append(
            Button(
                (center[0], center[1]+100),
                600,
                100,
                "#f2fbff", 
                func = restart, 
                text="Jauna spēle", 
                border_radius=5
                )
            )
        buttons.append(
            Button(
                (60, 680),
                100, 
                50, 
                "#d6253d", 
                5, 
                func = (lambda: pg.event.post(pg.event.Event(pg.QUIT))), 
                text="Iziet"
                )
            )

        pair_amount = math.ceil(len(game.get_virkne())/2)
        seq_bounding_box = ((padding*pair_amount)-(pad_amount*pair_amount), seq_button_height)
        


        for i in range(pair_amount):
            buttons.append(
                Button(
                    ((center[0]-seq_bounding_box[0]//2)+padding*i, center[1]-100-seq_bounding_box[1]//2), 
                    seq_button_width, 
                    seq_button_height, 
                    "#93ff4b",
                    5,
                    (lambda pair_index=i+1: pair_click(pair_index)), 
                    "".join(map(str, game.get_virkne()[2*i:2*(i+1)]))
                    )
                )

        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    running = False
                case pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                
                        mouse_pos = pg.mouse.get_pos()

                        for b in buttons:
                            if b.mouse_over(mouse_pos):
                                b.call_back()
                case pg.KEYDOWN:
                    pass
                case _:
                    pass

        if game.Has_finished():

            match game.winCon():
                case 1:
                    msg_box.updateText('Uzvarēja cilvēks!')
                    screen.fill("#b6ffb4")
                case 0:
                    msg_box.updateText('Neizšķirts')
                    screen.fill("#fff4b4")
                case -1:
                    msg_box.updateText('Uzvarēja dators!')
                    screen.fill("#ffb4b4")
        else:
            screen.fill("#f8f6e6")

        for l in labels:
            l.draw(screen)

        for b in buttons:
            if b.mouse_over(pg.mouse.get_pos()):
                b.render_color =  b.hover_color
            else:
                b.render_color = b.color
            b.draw(screen)
        
        display.flip()

        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    main()