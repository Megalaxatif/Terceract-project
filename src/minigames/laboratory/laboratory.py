import math

import nn
import pygame

model = nn.NeuralNetwork("save.json")

pygame.init()
pygame.font.init()

background_colour = (255, 255, 255)
(width, height) = (812, 662)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pattern")
clock = pygame.time.Clock()
FPS = 3000

GRID_COLS = 4
GRID_ROWS = 4
CELL_SIZE = 128
BRUSH = 15

RESET_RECT = pygame.Rect(50, 550, 150, 80)
CHECK_RECT = pygame.Rect(300, 550, 150, 80)

smallfont = pygame.font.SysFont("Arial", 32)


class Grid:
    def __init__(self, size, screen_x, screen_y):
        self.size = size
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.grid = [[0.0 for _ in range(self.size)] for _ in range(self.size)]
        self.brush = BRUSH

    def reset(self):
        self.grid = [[0.0 for _ in range(self.size)] for _ in range(self.size)]

    def contains_screen_pos(self, pos):  # return if clicked on grid
        x, y = pos
        return (
            self.screen_x <= x < self.screen_x + self.size
            and self.screen_y <= y < self.screen_y + self.size
        )

    def screen_to_local(self, pos):
        x, y = pos
        return x - self.screen_x, y - self.screen_y

    def modify(self, local_x, local_y):
        r = self.brush / 2.0
        cx = local_x
        cy = local_y

        # to not get out of the grid
        x_min = max(0, int(cx - r - 1))
        x_max = min(self.size - 1, int(cx + r + 1))
        y_min = max(0, int(cy - r - 1))
        y_max = min(self.size - 1, int(cy + r + 1))

        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                dx = x + 0.5 - cx
                dy = y + 0.5 - cy
                d = math.sqrt(dx * dx + dy * dy)

                if d <= r:
                    # 1 at the center, 0 on the edge
                    val = 1.0 - (d / r)
                    if val > self.grid[y][x]:
                        self.grid[y][x] = val

    def draw_brush(self, local_x, local_y):
        self.modify(local_x, local_y)

    def bbox(self, threshold=0.05):
        min_x, min_y = self.size, self.size
        max_x, max_y = -1, -1

        for y in range(self.size):
            for x in range(self.size):
                if self.grid[y][x] > threshold:
                    if x < min_x:
                        min_x = x
                    if y < min_y:
                        min_y = y
                    if x > max_x:
                        max_x = x
                    if y > max_y:
                        max_y = y

        if max_x == -1:
            return None

        return min_x, min_y, max_x, max_y

    def resample_square(self, src, out_size):  # resize src to out_size size matrix
        src_h = len(src)
        src_w = len(src[0])

        if src_h == 0 or src_w == 0:
            return [[0.0 for _ in range(out_size)] for _ in range(out_size)]

        result = [[0.0 for _ in range(out_size)] for _ in range(out_size)]

        for oy in range(out_size):
            for ox in range(out_size):
                x0 = int(ox * src_w / out_size)
                x1 = int((ox + 1) * src_w / out_size)
                y0 = int(oy * src_h / out_size)
                y1 = int((oy + 1) * src_h / out_size)

                if x1 <= x0:
                    x1 = x0 + 1
                if y1 <= y0:
                    y1 = y0 + 1

                total = 0.0
                count = 0

                for yy in range(y0, min(y1, src_h)):
                    for xx in range(x0, min(x1, src_w)):
                        total += src[yy][xx]
                        count += 1

                result[oy][ox] = total / count if count > 0 else 0.0

        return result

    def draw_line_from_screen_pos(self, start_pos, end_pos):
        x0, y0 = self.screen_to_local(start_pos)
        x1, y1 = self.screen_to_local(end_pos)

        dx = x1 - x0
        dy = y1 - y0
        dist = math.hypot(dx, dy)

        if dist == 0:
            self.draw_brush(x0, y0)
            return

        step = max(1, self.brush / 4)
        steps = max(1, int(dist / step))

        for i in range(steps + 1):
            t = i / steps
            x = x0 + dx * t
            y = y0 + dy * t
            self.draw_brush(x, y)

    def to_28x28(self):
        box = self.bbox()
        if box is None:
            return [0.0] * (28 * 28)

        min_x, min_y, max_x, max_y = box

        # extract drawn content
        crop = []
        for y in range(min_y, max_y + 1):
            row = []
            for x in range(min_x, max_x + 1):
                row.append(self.grid[y][x])
            crop.append(row)

        crop_h = len(crop)
        crop_w = len(crop[0])

        if crop_h == 0 or crop_w == 0:
            return [0.0] * (28 * 28)

        # put drawing in square before reducing it
        side = max(crop_w, crop_h)
        square = [[0.0 for _ in range(side)] for _ in range(side)]

        offset_x = (side - crop_w) // 2
        offset_y = (side - crop_h) // 2

        for y in range(crop_h):
            for x in range(crop_w):
                square[offset_y + y][offset_x + x] = crop[y][x]

        # we reduce at 20x20
        reduced = self.resample_square(square, 20)

        # center on 28x28
        canvas = [[0.0 for _ in range(28)] for _ in range(28)]
        start_x = 4
        start_y = 4

        for y in range(20):
            for x in range(20):
                canvas[start_y + y][start_x + x] = reduced[y][x]

        # flatten
        result = []
        for y in range(28):
            for x in range(28):
                result.append(canvas[y][x])

        return result

    def ask(self):
        data = self.to_28x28()

        return model.predict(data)

    def update_from_screen_pos(self, pos):
        if not self.contains_screen_pos(pos):
            return

        local_x, local_y = self.screen_to_local(pos)
        self.draw_brush(local_x, local_y)

    def draw_border(self):
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (self.screen_x, self.screen_y, self.size, self.size),
            1,
        )

    def render(self):
        for y in range(self.size):
            for x in range(self.size):
                v = self.grid[y][x]
                if v > 0:
                    gray = int(255 * (1.0 - v))
                    pygame.draw.rect(
                        screen,
                        (gray, gray, gray),
                        (self.screen_x + x, self.screen_y + y, 1, 1),
                    )
        self.draw_border()


def create_grids():
    grids = []
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            grids.append(Grid(CELL_SIZE, x, y))
    return grids


def get_grid_at_pos(grids, pos):
    for grid in grids:
        if grid.contains_screen_pos(pos):
            return grid
    return None


def draw_buttons(mouse):
    text = smallfont.render("RESET", True, (0, 0, 0))
    color = (200, 200, 200) if RESET_RECT.collidepoint(mouse) else (100, 100, 100)
    pygame.draw.rect(screen, color, RESET_RECT)
    screen.blit(text, (RESET_RECT.x + 10, RESET_RECT.y + 20))

    text = smallfont.render("CHECK", True, (0, 0, 0))
    color = (200, 200, 200) if CHECK_RECT.collidepoint(mouse) else (100, 100, 100)
    pygame.draw.rect(screen, color, CHECK_RECT)
    screen.blit(text, (CHECK_RECT.x + 10, CHECK_RECT.y + 20))


def redraw_all(grids, mouse):
    screen.fill(background_colour)

    for grid in grids:
        grid.render()

    draw_buttons(mouse)
    pygame.display.update()


grids = create_grids()
running = True
clicked = False
active_grid = None
last_mouse_pos = None

redraw_all(grids, pygame.mouse.get_pos())

while running:
    clock.tick(FPS)
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
            last_mouse_pos = mouse

            if RESET_RECT.collidepoint(mouse):
                active_grid = None
                for grid in grids:
                    grid.reset()
                redraw_all(grids, mouse)

            elif CHECK_RECT.collidepoint(mouse):
                active_grid = None
                guesses = [grid.ask() for grid in grids]
                print("Guess final de chaque grille :", guesses)

            else:
                active_grid = get_grid_at_pos(grids, mouse)
                if active_grid is not None:
                    active_grid.draw_brush(*active_grid.screen_to_local(mouse))

        elif event.type == pygame.MOUSEBUTTONUP:
            clicked = False
            active_grid = None
            last_mouse_pos = None

        elif event.type == pygame.MOUSEMOTION and clicked:
            if active_grid is not None and last_mouse_pos is not None:
                active_grid.draw_line_from_screen_pos(last_mouse_pos, mouse)
            last_mouse_pos = mouse

    redraw_all(grids, mouse)

pygame.quit()
