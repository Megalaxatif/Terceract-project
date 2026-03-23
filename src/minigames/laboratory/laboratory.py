import math
import pygame
import json
import numpy as np

# neural network part
class Layer:
    def __init__(self, weights, biases):
        self.weights = np.array(weights, dtype=float).T
        self.biases = np.array(biases, dtype=float)

    def forward(self, x):
        return np.dot(x, self.weights) + self.biases


def relu(x):
    return np.maximum(0, x)


def softmax(x):
    x = x - np.max(x, axis=1, keepdims=True)
    exp_x = np.exp(x)
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)


class NeuralNetwork:
    def __init__(self, json_path):
        with open(json_path, "r") as f: # import a pre trained weights and biases (made by us from scratch with no lib)
            data = json.load(f)

        self.hidden1 = self._load_layer(data, "hidden1")
        self.hidden2 = self._load_layer(data, "hidden2")
        self.output = self._load_layer(data, "output")

    def _load_layer(self, data, name):
        if name not in data:
            raise ValueError(f"Layer '{name}' not found")
        return Layer(data[name]["weights"], data[name]["biases"])

    def forward(self, x):
        x = np.array(x, dtype=np.float32).reshape(1, -1)
        x = relu(self.hidden1.forward(x))
        x = relu(self.hidden2.forward(x))
        x = softmax(self.output.forward(x))
        return x

    def predict(self, x):
        probs = self.forward(x)
        index = np.argmax(probs, axis=1)[0]
        return str(int(index))

# end of neural network part

pygame.init()
pygame.font.init()

background_colour = (255, 255, 255)

BASE_WIDTH = 1080
BASE_HEIGHT = 720
FPS = 60

GRID_COLS = 4
GRID_ROWS = 4
CELL_SIZE = 128
BRUSH = 20

expected_outputs = ["1", ".", ".", ".",
                    ".", "4", ".", "5",
                    ".", "8", "0", ".",
                    ".", ".", ".", "2"] # answer of the laboratory


class Grid: # one of the 16 grids
    def __init__(self, size, screen_x, screen_y, model):
        self.size = size
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.grid = [[0.0 for _ in range(self.size)] for _ in range(self.size)]
        self.brush = BRUSH # the size of the pen we draw with
        self.model = model # the neural network

    def reset(self): # reset the grid by putting 0s everywhere
        self.grid = [[0.0 for _ in range(self.size)] for _ in range(self.size)]

    def contains_screen_pos(self, pos): # check if the pos is in the grid
        x, y = pos
        return (
            self.screen_x <= x < self.screen_x + self.size
            and self.screen_y <= y < self.screen_y + self.size
        )

    def screen_to_local(self, pos): # convert global coordinates to local ones
        x, y = pos
        return x - self.screen_x, y - self.screen_y

    def modify(self, local_x, local_y): # if we click on the grid, it changes the grid values
        # here it just modifies the matrix, not the visual part
        r = self.brush / 2.0 # radius
        cx = local_x # center x
        cy = local_y # center y

        x_min = max(0, int(cx - r - 1)) # max and min to ensure to not go out of the grid
        x_max = min(self.size - 1, int(cx + r + 1))
        y_min = max(0, int(cy - r - 1))
        y_max = min(self.size - 1, int(cy + r + 1))

        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                dx = x + 0.5 - cx # 0.5 to be at the center of the pixel
                dy = y + 0.5 - cy
                d = math.sqrt(dx * dx + dy * dy) # compute the euclidian distance

                if d <= r:
                    val = 1.0 - (d / r) # 1 at the center, 0 on the edge
                    if val > self.grid[y][x]: # just keep the highest value
                        self.grid[y][x] = val # apply this value in grid

    def draw_brush(self, local_x, local_y): # just a wrapper
        self.modify(local_x, local_y)

    def bbox(self, threshold=0.05): # get the bounding box (already used somewhere else in the code)
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

    def resample_square(self, src, out_size): # makes a matrix src x src to a matrix out_size x out_size
        src_h = len(src)
        src_w = len(src[0])

        if src_h == 0 or src_w == 0:
            return [[0.0 for _ in range(out_size)] for _ in range(out_size)]

        result = [[0.0 for _ in range(out_size)] for _ in range(out_size)] # start with filling with 0s

        for oy in range(out_size):
            for ox in range(out_size):
                x0 = int(ox * src_w / out_size) # to get the points to have a little square which will be only one square in the output matrix
                x1 = int((ox + 1) * src_w / out_size)   
                y0 = int(oy * src_h / out_size)         
                y1 = int((oy + 1) * src_h / out_size)   

                if x1 <= x0: # to ensure to have a non zero value
                    x1 = x0 + 1
                if y1 <= y0:
                    y1 = y0 + 1

                total = 0.0
                count = 0

                for yy in range(y0, min(y1, src_h)): # make the sum of each value of the little square
                    for xx in range(x0, min(x1, src_w)):
                        total += src[yy][xx]
                        count += 1

                result[oy][ox] = total / count if count > 0 else 0.0 # put the average in one value of the output matrix

        return result

    def draw_line_from_screen_pos(self, start_pos, end_pos): # draws a line if we draw too fast
        x0, y0 = self.screen_to_local(start_pos)
        x1, y1 = self.screen_to_local(end_pos)

        dx = x1 - x0
        dy = y1 - y0
        dist = math.hypot(dx, dy) # gives the euclidian distance of dx, dy

        if dist == 0: # handling edge case
            self.draw_brush(x0, y0)
            return

        step = max(1, self.brush / 8) # size of a step
        steps = max(1, int(dist / step)) # how many steps

        for i in range(steps + 1): # draw the line
            t = i / steps
            x = x0 + dx * t
            y = y0 + dy * t
            self.draw_brush(x, y)

    def to_28x28(self): # convert a matrix to a 28 by 28 one, we are not using resample_square because we center the pixels here
        box = self.bbox() # we only extract the important data
        if box is None: # if nothing is drawn we ignore the grid
            return None

        min_x, min_y, max_x, max_y = box 

        crop = []
        for y in range(min_y, max_y + 1): # put the important data in the grid
            row = []
            for x in range(min_x, max_x + 1):
                row.append(self.grid[y][x])
            crop.append(row)

        crop_h = len(crop)
        crop_w = len(crop[0])

        if crop_h == 0 or crop_w == 0: # edge case handling
            return None

        side = max(crop_w, crop_h) # get the longest side to create a square of this size
        square = [[0.0 for _ in range(side)] for _ in range(side)] # init this square

        offset_x = (side - crop_w) // 2 # the values needed to move x and y to fit in the square
        offset_y = (side - crop_h) // 2

        for y in range(crop_h): # center the image
            for x in range(crop_w):
                square[offset_y + y][offset_x + x] = crop[y][x]

        reduced = self.resample_square(square, 20) # convert our square to a 20x20 one

        result = [[0.0 for _ in range(28)] for _ in range(28)] # init the result
        start_x = 4
        start_y = 4

        for y in range(20): # put the data of the 20x20 square at the center of the result
            for x in range(20):
                result[start_y + y][start_x + x] = reduced[y][x]

        return result

    def ask(self): # from a matrix, it guesses a result
        data = self.to_28x28()

        if not data: # if the square is empty, we put a dot
            return "."

        return self.model.predict(data) # we use our pre trained model

    def draw_border(self, screen, draw_x, draw_y, draw_size_x, draw_size_y):
        pygame.draw.rect(
            screen,
            (0, 0, 0), # color
            (draw_x, draw_y, draw_size_x, draw_size_y), # coordinate of our grid
            1 # thickness of the border
        )

    def render(self, screen, delta): # display black values for each drawn pixels
        draw_x = int(self.screen_x * delta) # apply deltas to handle window size changes
        draw_y = int(self.screen_y * delta) # whole area size
        draw_size_x = int(self.size * delta) # grid area size
        draw_size_y = int(self.size * delta)

        pixel_w = max(1, math.ceil(delta)) # size of a pixel
        pixel_h = max(1, math.ceil(delta))

        for y in range(self.size):
            for x in range(self.size):
                v = self.grid[y][x]
                if v > 0: # only modify if non white
                    gray = int(255 * (1.0 - v)) # add gray to simulate a real pen
                    pygame.draw.rect( # display with rectangles
                        screen,
                        (gray, gray, gray),
                        (
                            draw_x + int(x * delta),
                            draw_y + int(y * delta),
                            pixel_w,
                            pixel_h,
                        ),
                    )

        self.draw_border(screen, draw_x, draw_y, draw_size_x, draw_size_y)


class Laboratory:
    def __init__(self, game_context):
        self.game_context = game_context
        self.model = NeuralNetwork("minigames/laboratory/save.json")
        self.name = "pattern"
        
        self.width = BASE_WIDTH
        self.height = BASE_HEIGHT
        self.screen = self.game_context.screen
        pygame.display.set_caption("Pattern")
        self.clock = pygame.time.Clock()

        self.running = True
        self.clicked = False
        self.active_grid = None
        self.last_mouse_pos = None
        self.send_message = ""

        self.smallfont = pygame.font.SysFont("Arial", 32)

        self.grids = self.create_grids()
        self.outputs = ["."] * len(self.grids)

    def create_grids(self): # create the 16 grids (just for the init of the class)
        grids = []
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                grids.append(Grid(CELL_SIZE, x, y, self.model))
        return grids

    def get_grid_at_pos(self, pos): # to know on which grid we are drawing
        for grid in self.grids:
            if grid.contains_screen_pos(pos):
                return grid
        return None

    def get_delta(self): # compute deltas
        self.width, self.height = self.screen.get_size()
        delta_x = self.width / BASE_WIDTH
        delta_y = self.height / BASE_HEIGHT
        return min(delta_x, delta_y)

    def get_reset_rect(self, delta):
        return pygame.Rect(
            0,
            int(550 * delta),
            int(160 * delta),
            int(80 * delta),
        )

    def get_decrypt_rect(self, delta):
        return pygame.Rect(
            int(176 * delta),
            int(550 * delta),
            int(160 * delta),
            int(80 * delta),
        )

    def get_send_rect(self, delta):
        return pygame.Rect(
            int(352 * delta),
            int(550 * delta),
            int(160 * delta),
            int(80 * delta),
        )
        
    def get_back_rect(self, delta):
        return pygame.Rect(
            int(176 * delta),
            int(646 * delta),
            int(160 * delta),
            int(80 * delta),
        )

    def draw_button(self, rect, label, mouse, font): # label is text
        color = (200, 200, 200) if rect.collidepoint(mouse) else (100, 100, 100)
        pygame.draw.rect(self.screen, color, rect)

        text = font.render(label, True, (0, 0, 0))
        text_rect = text.get_rect(center=rect.center)
        self.screen.blit(text, text_rect)

    def draw_outputs(self, delta):
        font = pygame.font.SysFont("Arial", max(12, int(32 * delta)))

        for i, grid in enumerate(self.grids):
            if i >= len(self.outputs):
                continue

            text = font.render(str(self.outputs[i]), True, (0, 0, 0))
            text_x = int((grid.screen_x + 5 * grid.size + 8) * delta)
            text_y = int((grid.screen_y + grid.size // 2) * delta - text.get_height() // 2)
            self.screen.blit(text, (text_x, text_y))

    def draw_buttons(self, mouse, delta):
        font = pygame.font.SysFont("Arial", max(12, int(32 * delta)))

        reset_rect = self.get_reset_rect(delta)
        decrypt_rect = self.get_decrypt_rect(delta)
        send_rect = self.get_send_rect(delta)
        back_rect = self.get_back_rect(delta)

        self.draw_button(reset_rect, "RESET", mouse, font)
        self.draw_button(decrypt_rect, "DECRYPT", mouse, font)
        self.draw_button(send_rect, "SEND", mouse, font)
        self.draw_button(back_rect, "GO BACK", mouse, font)

        if self.send_message: # the final message 
            result_text = font.render(self.send_message, True, (0, 0, 0))
            self.screen.blit(result_text, (int(650 * delta), int(570 * delta)))

    def redraw_all(self, mouse, delta):
        self.screen.fill(background_colour)

        for grid in self.grids:
            grid.render(self.screen, delta)

        self.draw_outputs(delta)
        self.draw_buttons(mouse, delta)

    def handle_mouse_down(self, mouse, base_mouse, delta):
        self.clicked = True
        self.last_mouse_pos = base_mouse

        reset_rect = self.get_reset_rect(delta)
        decrypt_rect = self.get_decrypt_rect(delta)
        send_rect = self.get_send_rect(delta)
        back_rect = self.get_back_rect(delta)

        if reset_rect.collidepoint(mouse):
            self.active_grid = None
            for grid in self.grids:
                grid.reset()
            self.outputs = ["."] * len(self.grids)
            self.send_message = ""

        elif decrypt_rect.collidepoint(mouse):
            self.active_grid = None
            self.outputs = [grid.ask() for grid in self.grids]

        elif send_rect.collidepoint(mouse):
            if self.outputs == expected_outputs:
                self.send_message = "PASSWORD: hope"
            else:
                self.send_message = "ACCESS DENIED"
                
        elif back_rect.collidepoint(mouse):
            self.game_context.current_mini_game = "game"

        else:
            self.active_grid = self.get_grid_at_pos(base_mouse)
            if self.active_grid is not None:
                self.active_grid.draw_brush(*self.active_grid.screen_to_local(base_mouse))

    def handle_mouse_up(self):
        self.clicked = False
        self.active_grid = None
        self.last_mouse_pos = None

    def handle_mouse_motion(self, base_mouse):
        if self.clicked and self.active_grid is not None and self.last_mouse_pos is not None:
            self.active_grid.draw_line_from_screen_pos(self.last_mouse_pos, base_mouse)
        self.last_mouse_pos = base_mouse


    def handle_left_click(self, event):
        mouse = pygame.mouse.get_pos()
        delta = self.game_context.delta
        base_mouse = (mouse[0] / delta, mouse[1] / delta)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(mouse, base_mouse, delta)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up()

        elif event.type == pygame.MOUSEMOTION:
            self.handle_mouse_motion(base_mouse)

    def update(self):
        mouse = pygame.mouse.get_pos()
        self.redraw_all(mouse, self.game_context.delta)