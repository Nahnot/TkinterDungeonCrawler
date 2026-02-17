import platform

if platform.system() == "Darwin":
    macOS = True
else:
    macOS = False

import tkinter as tk
import tkinter.font as font

if macOS:
    from tkmacosx import Button
else:
    from tkinter import Button
import random
import tkinter.scrolledtext as scrolledtext

#import idlelib.tooltip as tt

from PIL import ImageTk

# TO DO: COMBAT

getstate = 1
GET_ROW = 0
GET_COL = 1

get_frame = 0
get_btn = 1

WIDTH = 1000
HEIGHT = 1000
HORIZONTAL_OFFSET = 0

window = tk.Tk()
window.configure(bg='black')
window.title("Land of Dardar")
window.geometry(f"{WIDTH}x{HEIGHT}+{HORIZONTAL_OFFSET}+0")
# window.state('zoomed')
# window.resizable(False, False)

super_small_font = font.Font(family="Courier", size=13)
small_font = font.Font(family="Courier", size=15)
large_font = font.Font(family="Courier", size=20)
very_large_font = font.Font(family="Courier", size=30)

big_left_frame = tk.Frame(window, bg='black')
big_right_frame = tk.Frame(window, bg='black')

big_left_frame.grid(row=0, column=0, sticky='ns')
big_right_frame.grid(row=0, column=1, sticky='ns')
big_right_frame.columnconfigure(0, weight=2)

equipment_frame = tk.Frame(big_left_frame, width=450, height=1080 / 2, bg='black')
stats_frame = tk.Frame(big_left_frame, width=450, height=1080 / 2, bg='black')
blank_frame = tk.Frame(big_left_frame, width=50, bg='black')

equipment_frame.grid(row=0, column=0, sticky='ns')
stats_frame.grid(row=1, column=0, sticky='ns')
blank_frame.grid(row=0, column=1, sticky='ns')

inventory_frame = tk.Frame(big_right_frame, width=500)
horizontal_blank_frame = tk.Frame(big_right_frame, height=100, bg='black')
right_vertical_blank_frame = tk.Frame(big_right_frame, width=50, bg='black')
dungeon_frame = tk.Frame(big_right_frame, bg='black')
log_frame = tk.Frame(big_right_frame, bg='black')

inventory_frame.grid(row=0, column=1, sticky='n')
horizontal_blank_frame.grid(row=1, column=1, sticky='ew')
dungeon_frame.grid(row=2, column=1, sticky='ns')
right_vertical_blank_frame.grid(row=0, column=2, sticky='ns')
log_frame.grid(row=2, column=3, sticky='nsew')

dummy_button = Button(window, text='ppp')

if not macOS:
    BTN_WIDTH = 4
    BTN_HEIGHT = 2
DUNGEON_BTN_WIDTH_IN_PIXELS = 48
DUNGEON_BTN_HEIGHT_IN_PIXELS = 48
INVENTORY_BTN_WIDTH_IN_PIXELS = 74
INVENTORY_BTN_HEIGHT_IN_PIXELS = 83

FRAME_SIZE_GAP = 2
BTN_PAD = FRAME_SIZE_GAP / 2

DUNGEON_FRAME_WIDTH = DUNGEON_BTN_WIDTH_IN_PIXELS + FRAME_SIZE_GAP
DUNGEON_FRAME_HEIGHT = DUNGEON_BTN_HEIGHT_IN_PIXELS + FRAME_SIZE_GAP
INVENTORY_FRAME_WIDTH = INVENTORY_BTN_WIDTH_IN_PIXELS + FRAME_SIZE_GAP
INVENTORY_FRAME_HEIGHT = INVENTORY_BTN_HEIGHT_IN_PIXELS + FRAME_SIZE_GAP
direction_map = {
    (-1, -1): 'up_left',
    (-1, 0): 'up',
    (-1, 1): 'up_right',
    (0, -1): 'left',
    (0, 1): 'right',
    (1, -1): 'down_left',
    (1, 0): 'down',
    (1, 1): 'down_right',
}

visible_octants_for_each_direction = {
    'up': [1, 0, 7, 6],
    'left': [7, 6, 5, 4],
    'down': [5, 4, 3, 2],
    'right': [3, 2, 1, 0]
}

orthogonal_directions = ['up', 'down', 'left', 'right']


class GameController:
    def __init__(self):
        self.testing = False
        # Item, entity, and object glyphs
        if True:
            self.turn = 'player'
            self.player = '@'
            self.sword = '⸸'
            self.wall = ('▀▀ ▀▀ \n'
                         ' ▀▀ ▀▀\n'
                         '▀▀ ▀▀ \n'
                         ' ▀▀ ▀▀\n'
                         '▀▀ ▀▀ \n'
                         ' ▀▀ ▀▀')
            self.chest = '▣'
            self.key = '⚷'
            self.door = '𓉞'
            self.bars = ('⛓⛓⛓⛓\n'
                         '⛓⛓⛓⛓\n'
                         '⛓⛓⛓⛓\n'
                         '⛓⛓⛓⛓')
            self.locked_bars = ('⛓⛓⛓⛓\n'
                                '⛓⛓⛓⛓\n'
                                '⛓⛓∅⛓\n'
                                '⛓⛓⛓⛓')
            self.exit = '✦'
            self.coin = '¤'
            self.zombie = 'Ψ'

        self.enable_darkness = True

        self.singular_interactable_items = [self.key, self.sword]
        self.enemies = [self.zombie]
        self.solid_objects = [self.wall, self.chest, self.exit, self.door, self.bars, self.locked_bars, self.player]
        self.solid_objects.extend(self.singular_interactable_items)
        self.solid_objects.extend(self.enemies)
        self.opaque_objects = [self.wall, self.door]

        self.default_color = '#f0f0f0'

        self.default_highlight_color = 'yellow'
        self.freeze_color = 'light blue'
        self.enemy_alert_color = 'red'
        self.attack_color = 'maroon'

        self.highlight_colors = [self.default_highlight_color, self.freeze_color, self.enemy_alert_color,
                                 self.attack_color]

        self.lighting_colors = {
            0: 'black',
            1: '#141414',
            2: '#2D2D2D',
            3: '#444444',
            4: '#646363',
            5: '#888686',
            6: '#AEADAD',
            7: '#D6D2D2',
            8: '#ECECEC',
            9: self.default_color
        }

        self.game_log = None
        self.game_log_text = ""
        self.make_log()

        self.turn_num = 0

    def create_frame(self, parent_frame):
        if self.enable_darkness:
            new_frame = tk.Frame(parent_frame, background='black')
        else:
            new_frame = tk.Frame(parent_frame, background=self.default_color)
        if parent_frame == inventory_frame:
            new_frame.configure(bg=self.default_color)
            new_frame.configure(width=INVENTORY_FRAME_WIDTH, height=INVENTORY_FRAME_HEIGHT)
        elif parent_frame == dungeon_frame:
            new_frame.configure(width=DUNGEON_FRAME_WIDTH, height=DUNGEON_FRAME_HEIGHT)
        new_frame.grid_propagate(False)
        return new_frame

    def create_button(self, tile_char, parent_frame, btn_type):
        """
       Create a single tile widget ONCE during build.
       Movement will only edit ['text'], never create/destroy tiles.
       """

        # Defaults
        text = ' '
        fg = 'black'
        if self.enable_darkness:
            bg = 'black'
        else:
            bg = self.default_color
        btn_font = super_small_font
        if btn_type == 'inventory':
            btn_font = large_font
            bg = self.default_color
            command = lambda: inv.select_item([parent_frame, btn])
        else:
            command = self.pass_action

        # Map dungeon glyphs to rendered text/colors
        match tile_char:
            case 'o':  # open floor
                text = ' '
            case 'p':  # player start
                text = self.player
            case 'z':
                text = self.zombie
            case 'w':
                text = self.wall
            case 'c':
                text = self.chest
                #fg = 'gold'
            case 'd':
                text = self.door
            case 'e':
                text = self.exit
            case 'b':
                text = self.bars
            case '𝘣':
                text = self.locked_bars
            case 'k':
                text = self.key
            case _:
                # anything else is treated as blank floor
                text = tile_char

        btn = Button(
            parent_frame,
            text=text,
            fg=fg,
            font=btn_font,
            activebackground=bg,
            activeforeground=fg,
            bg=bg,
            command=command,
        )

        if macOS:
            # noinspection PyArgumentList
            btn.configure(takefocus=0, focuscolor='', borderless=1)
            if btn_type == 'dungeon':
                btn.configure(width=DUNGEON_BTN_WIDTH_IN_PIXELS, height=DUNGEON_BTN_HEIGHT_IN_PIXELS)
            elif btn_type == 'inventory':
                btn.configure(width=INVENTORY_BTN_WIDTH_IN_PIXELS, height=INVENTORY_BTN_HEIGHT_IN_PIXELS)
        else:
            btn.grid_propagate(False)
            btn.grid(padx=BTN_PAD, pady=BTN_PAD)
            btn.configure(width=BTN_WIDTH, height=BTN_HEIGHT)

        """if btn_type == 'dungeon':
            btn.configure(relief='flat')"""

        return btn

    @staticmethod
    def advance_turn(player_action):
        for entity, speed in dungeon.ordered_speed_of_current_entities.items():
            if entity == player:
                match player_action:
                    case 'movement':
                        player.steps_to_take_after_pressing_wasd()
                    case 'interaction':
                        player.interact()
            else:
                entity.action()
                entity.prepare_action()

    def make_log(self):
        self.game_log = tk.scrolledtext.ScrolledText(log_frame,
                                                     width=29,
                                                     height=32,
                                                     state='disabled',
                                                     undo=True,
                                                     font=super_small_font,
                                                     wrap='word'
                                                     )
        self.game_log.grid(row=0, column=0)

    def update_log(self, event_type, event_objects):
        if event_type == 'item picked up':
            text = f"{event_objects} has been picked up!\n"
            first_word, other_text = text.split(' ', 1)
            text_list = [first_word, other_text]
            first_word.title()
            " ".join(text_list)
        elif event_type == 'combat':
            attacker = event_objects[0]
            attacked = event_objects[1]
            damage = event_objects[2]
            text = f"{attacker} hit {attacked} for {damage}!\n"
        self.game_log['state'] = 'normal'
        # noinspection PyUnboundLocalVariable
        self.game_log.insert('1.0', text)
        self.game_log['state'] = 'disabled'

    def pass_action(self):
        pass


class Dungeon:
    def __init__(self):
        self.level = 0

        self.lowest_light_level_in_current_level = 0

        self.current_enemies = {}

        self.current_entities = {}
        self.speed_of_current_entities = {}
        # The speed is now in descending order, meaning that higher speed entities have a higher index, meaning they go first
        self.ordered_speed_of_current_entities = {}

        # Rendering/structures
        if True:
            self.tiles_indexed_by_coords = {}
            self.coords_indexed_by_tiles = {}

            self.max_row = 0
            self.max_col = 0

            self.level_text = ''
            self.set_level_text()
            self.build_level()

    def set_level_text(self):
        # Max rows: 15
        # Max cols: 28
        # copy-paste able characters:
        # 𝘣
        self.finished_loading = False
        self.lowest_light_level_in_current_level = 0
        match self.level:
            case -9999:
                self.level_text = ("wwwwwwwwwwwwwwwwwwwwwwwwwww\n"
                                   "woooooooooooo\n"
                                   "wpoooooowoooo\n"
                                   "wooowooooooow\n"
                                   "wooooooooooow\n"
                                   "woooooooooooo\n"
                                   "woooooooooooo\n"
                                   "woooooooooooo\n"
                                   "woooooooooooo\n"
                                   "woooooooooooo\n"
                                   "wwwwwwwwwwwww\n"
                                   "wwwwwwwwwwwww\n"
                                   "wwwwwwwwwwwww\n"
                                   "wwwwwwwwwwwww\n")
            case -2:
                self.level_text = ("wwwwwwwwwwwwwwww\n"
                                   "woooooooooooooow\n"
                                   "wooooooowoooooow\n"
                                   "wooowooooozowoow\n"
                                   "woop⸸ooooooowoow\n"
                                   "woooooooooooooow\n"
                                   "wwwwwwwwwwwwwwww")
            case 0:
                self.level_text = ("wwwwwwwwwwwwwwwwwwwwwwwwwwww\n"
                                   "woooooooooooooooooooooowwwww\n"
                                   "woooooooooooooooooooooobooow\n"
                                   "wb𝘣bwbobwbbowbbbwbbbwoobooow\n"
                                   "wooowooowooowooowooowoobooow\n"
                                   "wopowooowooowooowooowoowwwww\n"
                                   "wokowooowooowooowooowoobooow\n"
                                   "wwwwwwwwwwwwwwwwwwwwwoobooow\n"
                                   "wooowooowooowooowooowoobooow\n"
                                   "wooowooowooowooowooowoowwwww\n"
                                   "woozwooowzoowooowooowoobooow\n"
                                   "wobowooowboowooowoobwoobooow\n"
                                   "eoooooooooooooooooooooobooow\n"
                                   "eoooooooooooooooooooooowwwww\n"
                                   "wwwwwwwwwwwwwwwwwwwwwwwwwwww\n")
            case 1:
                if not game.testing:
                    player.vision_radius = 2
                self.level_text = ("wwwwwwwwwwwwwww\n"
                                   "wwwwwwwpwwwwwww\n"
                                   "woooooo⸸oooooow\n"
                                   "wwzwowwbwwwowww\n"
                                   "wwooowwewwwooow\n"
                                   "woowwwwwwwwowow\n"
                                   "wowwoooooooowow\n"
                                   "wowwwwwwowwooow\n"
                                   "wowoooowowwwoww\n"
                                   "wooowwoooooo⚷ww\n"
                                   "wwwwwwwwwwwwwww")
            case 2:
                self.level_text = ("wwwwwwwwwwww\n"
                                   "p⸸oooowwwwww\n"
                                   "woocoooozooe\n"
                                   "wooooowwwwww\n"
                                   "wwwwwwwwwwww")
            case _:
                window.destroy()

    def build_level(self):
        # Clear old widgets
        self.tiles_indexed_by_coords.clear()
        self.coords_indexed_by_tiles.clear()
        self.current_enemies.clear()

        row = 0
        col = 0
        idx = 0
        self.max_row = 0
        self.max_col = 0
        enemy_idx = 0

        for ch in self.level_text:
            if ch == '\n':
                row += 1
                col = 0
                continue

            new_frame = game.create_frame(dungeon_frame)
            new_frame.grid(row=row, column=col, sticky='nsew')
            btn = game.create_button(ch, new_frame, 'dungeon')
            btn.grid(row=row, column=col, sticky='nsew')

            #self.index_by_rows_and_cols[(row, col)] = idx

            self.tiles_indexed_by_coords[(row, col)] = (new_frame, btn)
            self.coords_indexed_by_tiles[new_frame, btn] = (row, col)

            if btn['text'] in game.enemies:
                self.current_enemies[enemy_idx] = (btn['text'], row, col)
                enemy_idx += 1

            self.max_row = max(self.max_row, row)
            self.max_col = max(self.max_col, col)

            col += 1
            idx += 1

    def find_new_location(self, entity, entity_coords, prev_entity_coords, direction):
        match direction:
            case 'up':
                entity_coords[GET_ROW] -= 1
            case 'left':
                entity_coords[GET_COL] -= 1
            case 'down':
                entity_coords[GET_ROW] += 1
            case 'right':
                entity_coords[GET_COL] += 1
            case _:
                return None

        # Clamp to bounds
        entity_coords[GET_ROW] = max(0, min(entity_coords[GET_ROW], self.max_row))
        entity_coords[GET_COL] = max(0, min(entity_coords[GET_COL], self.max_col))

        new_tile = self.tiles_indexed_by_coords[tuple(entity_coords)][get_btn]

        blocked = new_tile['text'] == game.player or new_tile['text'] in game.enemies or new_tile[
            'text'] in game.singular_interactable_items or new_tile['text'] in game.solid_objects
        if blocked or new_tile is None:
            if entity == game.player:
                player.changed_location = False
            return prev_entity_coords

        return entity_coords

    def go_to_new_location(self, entity, entity_coords, prev_entity_coords):
        new_tile = self.tiles_indexed_by_coords[tuple(entity_coords)][get_btn]
        prev_tile = self.tiles_indexed_by_coords[tuple(prev_entity_coords)][get_btn]
        prev_tile['text'] = ' '
        new_tile['text'] = entity

    def locate_important_objects_and_entities(self):
        for i, (enemy_type, row, col) in self.current_enemies.items():
            if enemy_type == game.zombie:
                self.current_enemies[i] = Zombie(enemy_type, row, col)
                self.current_entities[i] = self.current_enemies[i]
                self.speed_of_current_entities[self.current_enemies[i]] = self.current_enemies[i].speed
        dungeon.ordered_speed_of_current_entities = {key: val for key, val in
                                                     sorted(dungeon.speed_of_current_entities.items(),
                                                            key=lambda item: item[1], reverse=True)}
        print(dungeon.ordered_speed_of_current_entities)

    def next_level(self):
        self.level += 1
        #print(self.tiles)
        for coords, (frame, btn) in dungeon.tiles_indexed_by_coords.items():
            frame.destroy()
            btn.destroy()

        self.set_level_text()
        self.build_level()
        player.init_every_level()
        dungeon.locate_important_objects_and_entities()
        #chest.figure_out_their_locations()
        self.finished_loading = True


class Inventory:
    def __init__(self):
        self.inventory = {}
        self.empty = ' '
        self.weapon_selected = False
        row = 0
        col = 0
        for i in range(1, 11):
            new_frame = game.create_frame(inventory_frame)
            btn = game.create_button(' ', new_frame, 'inventory')
            self.inventory[i - 1] = [new_frame, btn]
            self.inventory[i - 1][get_frame].grid(row=row, column=col, sticky='nsew')
            self.inventory[i - 1][get_btn].grid(row=row, column=col, sticky='nsew')
            col += 1
            if i % 5 == 0 and i != 0:
                row += 1
                col = 0

        #print(f'inventory: {self.inventory}')
        self.selected_item_slot = self.inventory[0]
        self.prev_selected_item_slot = self.inventory[1]
        self.select_item(self.selected_item_slot)

    def pick_up_item(self, item):
        for i, slot in self.inventory.items():
            if slot[get_btn]['text'] == ' ':
                #print('item picked up')
                slot[get_btn]['text'] = item
                print(f'text: {slot[get_btn]['fg']}')
                game.update_log('item picked up', item)
                self.influence_player_highlight()
                break

    def destroy_item(self, item):
        for i, slot in self.inventory.items():
            if slot[get_btn]['text'] == item:
                #print('item destroyed')
                slot[get_btn].config(text=' ')
                break

    def select_item(self, slot):
        self.prev_selected_item_slot = self.selected_item_slot
        self.selected_item_slot = slot

        self.inventory_highlighting()

        if dungeon.finished_loading:
            self.influence_player_highlight()

    def inventory_highlighting(self):
        if self.prev_selected_item_slot != self.selected_item_slot:
            self.prev_selected_item_slot[get_frame].configure(background=game.default_color)
            self.selected_item_slot[get_frame].configure(background=game.default_highlight_color)
        else:
            if self.selected_item_slot[get_frame]['bg'] == game.default_color:
                self.selected_item_slot[get_frame].configure(background=game.default_highlight_color)
            else:
                self.selected_item_slot[get_frame].configure(background=game.default_color)

    def register_inventory_number(self, num):
        if num == '0':
            num = '10'
        self.select_item(self.inventory[int(num) - 1])

    def influence_player_highlight(self):
        if self.selected_item_slot[get_btn]['text'] == game.sword:
            self.weapon_selected = True
        else:
            self.weapon_selected = False


class Player:
    def __init__(self):
        self.coords = []
        self.highlight_direction = 'right'
        self.prev_highlight_direction = 'left'
        self.vision_direction = 'right'
        self.prev_vision_direction = 'left'

        self.highlight_color = game.default_highlight_color
        self.changed_location = False

        self.max_hp = 10
        self.hp = self.max_hp
        self.speed = 10
        self.damage = 1
        if not game.testing:
            self.vision_radius = 1
        else:
            self.vision_radius = 5

        self.highlighting_diagonally_adjacent_tile = False  # an entity can only attack diagonals
        self.attack_mode = False

        self.init_every_level()

    def init_every_level(self):
        self.rendered_light_levels = {}
        self.prev_light_levels = {}
        for coords, (frame, btn) in dungeon.tiles_indexed_by_coords.items():
            self.rendered_light_levels[(frame, btn)] = 0
            if btn['text'] == game.player:
                self.coords = list(coords)
                self.tile_itself = (frame, btn)

        dungeon.current_entities[len(dungeon.current_entities)] = self
        dungeon.speed_of_current_entities[self] = self.speed
        self.prev_coords = self.coords.copy()
        self.highlighted_coords = self.coords.copy()
        self.highlighted_tile = dungeon.tiles_indexed_by_coords[tuple(self.coords)]
        self.prev_highlighted_coords = None
        self.change_vision = True

        self.determine_vision_direction()
        self.render_vision()
        self.determine_highlighted_button()
        self.apply_highlight_to_button()

    def determine_vision_direction(self):
        self.change_vision = True
        self.prev_vision_direction = self.vision_direction
        if '_right' in self.highlight_direction and self.prev_vision_direction == 'left':
            self.vision_direction = 'right'
        elif '_left' in self.highlight_direction and self.prev_vision_direction == 'right':
            self.vision_direction = 'left'
        elif 'up_' in self.highlight_direction and self.prev_vision_direction == 'down':
            self.vision_direction = 'up'
        elif 'down_' in self.highlight_direction and self.prev_vision_direction == 'up':
            self.vision_direction = 'down'
        elif self.highlight_direction in orthogonal_directions:
            self.vision_direction = self.highlight_direction

    def determine_highlighted_button(self):
        print(f'is weap selected?: {inv.weapon_selected} and {self.attack_mode}')
        if inv.weapon_selected and self.attack_mode:
            self.highlight_color = game.attack_color
        else:
            self.highlight_color = game.default_highlight_color

        self.prev_highlighted_coords = self.highlighted_coords.copy()
        self.highlighted_coords = self.coords.copy()

        match self.highlight_direction:
            case 'up_left':
                self.highlighted_coords[GET_ROW] -= 1
                self.highlighted_coords[GET_COL] -= 1
            case 'up':
                self.highlighted_coords[GET_ROW] -= 1
            case 'up_right':
                self.highlighted_coords[GET_ROW] -= 1
                self.highlighted_coords[GET_COL] += 1
            case 'left':
                self.highlighted_coords[GET_COL] -= 1
            case 'right':
                self.highlighted_coords[GET_COL] += 1
            case 'down_left':
                self.highlighted_coords[GET_ROW] += 1
                self.highlighted_coords[GET_COL] -= 1
            case 'down':
                self.highlighted_coords[GET_ROW] += 1
            case 'down_right':
                self.highlighted_coords[GET_ROW] += 1
                self.highlighted_coords[GET_COL] += 1
            case 'self':
                pass
            case _:
                return

        self.prev_highlighted_tile = self.highlighted_tile[:]
        self.highlighted_tile = dungeon.tiles_indexed_by_coords[tuple(self.highlighted_coords)]

    def force_diagonal_highlight_direction(self):
        self.prev_highlight_direction = self.highlight_direction
        match self.prev_highlight_direction:
            case 'up':
                self.highlight_direction = 'up_left'
            case 'right':
                self.highlight_direction = 'up_right'
            case 'down':
                self.highlight_direction = 'down_right'
            case 'left':
                self.highlight_direction = 'down_left'

    def apply_highlight_to_button(self):
        self.highlighted_tile[get_frame].configure(bg=self.highlight_color)

    def erase_highlight_from_prev_btn(self):
        light_level = self.rendered_light_levels[self.prev_highlighted_tile]
        self.prev_highlighted_tile[get_frame].configure(bg=game.lighting_colors[light_level])

    def interact(self):
        #('interaction')
        interacted_tile = dungeon.tiles_indexed_by_coords[tuple(self.highlighted_coords)]
        if self.rendered_light_levels[tuple(interacted_tile)] != 0:
            interacted_btn = interacted_tile[get_btn]
            interacted_spot = interacted_btn['text']
            print(f'interacted_spot: {interacted_spot}')
            if interacted_spot == game.chest:
                pass
                #print('chest interaction')
                #chest.open(self.btn_highlighted_coords)
            elif (interacted_spot == game.locked_bars or interacted_spot == game.door) and inv.selected_item_slot[get_btn]['text'] == game.key:
                #print('bars interaction')
                interacted_btn.config(text=' ')
                inv.destroy_item(game.key)
            elif interacted_spot == game.exit:
                #print('exited room')
                dungeon.next_level()
            elif interacted_spot in game.singular_interactable_items:
                for item in game.singular_interactable_items:
                    if item == interacted_spot:
                        inv.pick_up_item(item)
                        interacted_btn.config(text=' ')
            elif interacted_spot in game.enemies and self.attack_mode:
                for enemy in dungeon.current_enemies.values():
                    if enemy.tile_itself == interacted_tile:
                        Combat(attacker=self, attacked=enemy)

    def parse_key_press(self, key):

        if key in ['w', 'a', 's', 'd']:
            match key:
                case 'w':
                    self.movement_direction = 'up'
                case 'a':
                    self.movement_direction = 'left'
                case 's':
                    self.movement_direction = 'down'
                case 'd':
                    self.movement_direction = 'right'

            if '_' in self.highlight_direction and inv.weapon_selected:
                self.attack_mode = True
            else:
                self.attack_mode = False

            self.prev_coords = self.coords.copy()
            self.coords = dungeon.find_new_location(game.player, self.coords, self.prev_coords, self.movement_direction)
            self.tile_itself = dungeon.tiles_indexed_by_coords[tuple(self.coords)]
            if self.prev_coords == self.coords:
                self.changed_location = False
            else:
                self.changed_location = True
                self.determine_vision_direction()
                self.render_vision()
                self.determine_highlighted_button()
                game.advance_turn('movement')

        elif key in 'uiojklm' or key in ['comma', 'period']:
            self.prev_highlight_direction = self.highlight_direction
            match key:
                case 'u':
                    self.highlight_direction = 'up_left'
                case 'i':
                    self.highlight_direction = 'up'
                case 'o':
                    self.highlight_direction = 'up_right'
                case 'j':
                    self.highlight_direction = 'left'
                case 'l':
                    self.highlight_direction = 'right'
                case 'm':
                    self.highlight_direction = 'down_left'
                case 'comma':
                    self.highlight_direction = 'down'
                case 'period':
                    self.highlight_direction = 'down_right'

            if '_' in self.highlight_direction and inv.weapon_selected:
                self.attack_mode = True
            else:
                self.attack_mode = False
            self.steps_to_take_after_pressing_looking_keys()

        elif key == 'space':
            game.advance_turn('interaction')
        elif key in '0123456789':
            inv.register_inventory_number(key)

    def steps_to_take_after_pressing_wasd(self):
        if not self.change_vision:
            self.change_vision = True
        dungeon.go_to_new_location(game.player, self.coords, self.prev_coords)
        self.erase_highlight_from_prev_btn()
        self.apply_highlight_to_button()

    def steps_to_take_after_pressing_looking_keys(self):

        self.determine_vision_direction()
        self.change_vision = False

        if self.prev_highlight_direction != self.highlight_direction:
            self.determine_highlighted_button()
        if self.prev_vision_direction != self.vision_direction:
            self.change_vision = True
            self.render_vision()

        if self.prev_highlight_direction != self.highlight_direction:
            self.erase_highlight_from_prev_btn()

        for enemy in dungeon.current_enemies.values():
            enemy.steps_to_highlight_button()

        if self.prev_highlight_direction != self.highlight_direction:
            self.apply_highlight_to_button()

    def determine_light_levels_of_tiles(self):

        self.light_levels_by_tile = {}

        player_row, player_col = self.coords

        self.light_levels_by_tile[self.tile_itself] = self.vision_radius

        # \7|0/
        # 6\|/1
        #---|---
        # 5/|\2
        # /4|3\
        for octant in visible_octants_for_each_direction[self.vision_direction]:
            vision.cast_light_in_octant(self, player_row, player_col, self.vision_radius, octant)

        return self.light_levels_by_tile

    def render_vision(self):
        self.prev_rendered_light_levels = self.rendered_light_levels.copy()

        if self.change_vision:
            new_light_levels = self.determine_light_levels_of_tiles()

        print(new_light_levels)

        if self.change_vision:
            for (frame, btn), new_light_level in new_light_levels.items():
                old_light_level = self.prev_rendered_light_levels[(frame, btn)]

                if new_light_level == old_light_level:
                    continue

                tile_color = game.lighting_colors[new_light_level]

                frame.configure(bg=tile_color)
                btn.configure(bg=tile_color, fg='black')

                self.rendered_light_levels[(frame, btn)] = new_light_level

            for (frame, btn), _ in self.prev_light_levels.items():
                if (frame, btn) not in new_light_levels:
                    tile_color = game.lighting_colors[0]
                    frame.configure(bg=tile_color)
                    btn.configure(bg=tile_color, fg='black')

                    self.rendered_light_levels[(frame, btn)] = 0

        self.prev_light_levels = new_light_levels.copy()

    def kill_self(self):
        pass


class Enemy:
    def __init__(self, enemy_type, row, col):
        self.coords = [row, col]
        self.prev_coords = self.coords.copy()
        self.tile_itself = dungeon.tiles_indexed_by_coords[tuple(self.coords.copy())]

        self.highlighted_coords = self.coords.copy()
        self.prev_highlighted_coords = None
        self.highlight_color = game.default_highlight_color
        self.prev_highlighted_tile = None
        self.highlighted_tile = dungeon.tiles_indexed_by_coords[tuple(self.highlighted_coords)]

        self.enemy_type = enemy_type

        self.state = 'idle'
        self.prev_state = 'idle'
        self.prev_prev_state = 'idle'

        self.highlight_direction = 'right'
        self.prev_highlight_direction = 'right'
        self.do_highlight = False

        self.vision_direction = 'right'
        self.prev_vision_direction = 'right'

        self.is_visible_to_player = False
        self.prev_visible_to_player = False
        self.sees_player = False
        self.prev_saw_player = False

        self.rendered_light_levels = {}

    def can_see_player(self):
        self.determine_vision_direction()
        current_light_levels = self.determine_light_levels_of_tiles()
        #print(self.actual_vision_direction)
        return player.tile_itself in current_light_levels

    def is_orthogonally_adjacent_to_player(self):
        enemy_row, enemy_col = self.coords
        player_row, player_col = player.coords
        return abs(enemy_row - player_row) <= 1 and abs(enemy_col - player_col) <= 1 and not (
                abs(enemy_row - player_row) == 1 and abs(enemy_col - player_col) == 1)

    def is_diagonally_adjacent_to_player(self):
        enemy_row, enemy_col = self.coords
        player_row, player_col = player.coords
        return abs(enemy_row - player_row) == 1 and abs(enemy_col - player_col) == 1

    def check_self_visibility_and_highlight_status(self):
        self.prev_visible_to_player = self.is_visible_to_player
        if player.rendered_light_levels.get(self.tile_itself, 0) != 0:
            self.is_visible_to_player = True
            self.do_highlight = True
        else:
            self.is_visible_to_player = False
            self.do_highlight = False

    def move_towards_player(self):
        entity_row, entity_col = self.coords
        player_row, player_col = player.coords

        if abs(player_row - entity_row) > abs(player_col - entity_col):
            self.highlight_direction = 'down' if player_row > entity_row else 'up'
        else:
            self.highlight_direction = 'right' if player_col > entity_col else 'left'

    def determine_highlight_color(self):
        match self.state:
            case 'idle':
                self.highlight_color = game.default_highlight_color
            case 'aggro':
                self.highlight_color = game.enemy_alert_color
            case 'pursuit':
                self.highlight_color = game.enemy_alert_color
            case 'attack':
                self.highlight_color = game.attack_color
            case 'freeze':
                self.highlight_color = game.freeze_color

    def determine_highlighted_button(self):
        self.prev_highlighted_coords = self.highlighted_coords.copy()
        self.highlighted_coords = self.coords.copy()

        match self.highlight_direction:
            case 'up_left':
                self.highlighted_coords[GET_ROW] -= 1
                self.highlighted_coords[GET_COL] -= 1
            case 'up':
                self.highlighted_coords[GET_ROW] -= 1
            case 'up_right':
                self.highlighted_coords[GET_ROW] -= 1
                self.highlighted_coords[GET_COL] += 1
            case 'left':
                self.highlighted_coords[GET_COL] -= 1
            case 'right':
                self.highlighted_coords[GET_COL] += 1
            case 'down_left':
                self.highlighted_coords[GET_ROW] += 1
                self.highlighted_coords[GET_COL] -= 1
            case 'down':
                self.highlighted_coords[GET_ROW] += 1
            case 'down_right':
                self.highlighted_coords[GET_ROW] += 1
                self.highlighted_coords[GET_COL] += 1
            case 'self':
                pass
            case _:
                return

        self.prev_highlighted_tile = self.highlighted_tile[:]
        self.highlighted_tile = dungeon.tiles_indexed_by_coords[tuple(self.highlighted_coords)]

    def apply_highlight_to_button(self):
        if self.highlighted_tile != player.highlighted_tile:
            frame, btn = self.highlighted_tile
            frame.configure(bg=self.highlight_color)

    def erase_highlight_from_prev_btn(self):
        if not (
                self.prev_highlighted_tile == player.prev_highlighted_tile or self.highlighted_tile == player.prev_highlighted_tile or self.prev_highlighted_tile == player.highlighted_tile or self.highlighted_tile == player.highlighted_tile):
            light_level = player.rendered_light_levels.get(self.prev_highlighted_tile, 0)
            self.prev_highlighted_tile[get_frame].configure(bg=game.lighting_colors[light_level])
            print(self.prev_coords, player.rendered_light_levels.get(self.prev_highlighted_tile, 0))

    def steps_to_highlight_button(self):

        self.check_self_visibility_and_highlight_status()
        #print(f'is enemy visible to player: {self.is_visible_to_player}')

        self.determine_highlighted_button()
        if self.is_visible_to_player or (self.prev_visible_to_player and not self.is_visible_to_player) or (
                player.rendered_light_levels[self.prev_highlighted_tile] == 0 and self.prev_visible_to_player):
            self.erase_highlight_from_prev_btn()

        if self.do_highlight:
            self.determine_highlight_color()
            self.apply_highlight_to_button()

    def determine_vision_direction(self):
        self.prev_vision_direction = self.vision_direction
        if '_right' in self.highlight_direction and self.prev_vision_direction == 'left':
            self.vision_direction = 'right'
        elif '_left' in self.highlight_direction and self.prev_vision_direction == 'right':
            self.vision_direction = 'left'
        elif 'up_' in self.highlight_direction and self.prev_vision_direction == 'down':
            self.vision_direction = 'up'
        elif 'down_' in self.highlight_direction and self.prev_vision_direction == 'up':
            self.vision_direction = 'down'
        elif self.highlight_direction in orthogonal_directions:
            self.vision_direction = self.highlight_direction

    def determine_light_levels_of_tiles(self):

        self.light_levels_by_tile = {}

        enemy_row, enemy_col = self.coords

        self.light_levels_by_tile[self.tile_itself] = self.vision_radius + 1

        # \7|0/
        # 6\|/1
        #---|---
        # 5/|\2
        # /4|3\
        for octant in visible_octants_for_each_direction[self.vision_direction]:
            vision.cast_light_in_octant(self, enemy_row, enemy_col, self.vision_radius, octant)

        return self.light_levels_by_tile

    def kill_self(self):
        self.tile_itself[get_btn].config(text=' ')
        for i, enemy in dungeon.current_enemies.items():
            if enemy.coords == self.coords:
                highlighted_tile = dungeon.tiles_indexed_by_coords[tuple(self.highlighted_coords)]
                highlighted_tile[get_frame].configure(
                    bg=game.lighting_colors[player.rendered_light_levels[tuple(highlighted_tile)]])
                del dungeon.current_enemies[i]
                break


class Zombie(Enemy):
    def __init__(self, enemy_type, row, col):
        self.max_hp = 10
        self.hp = self.max_hp
        self.vision_radius = 4
        self.movement_length = 1
        self.damage = 1
        self.speed = 5

        self.vision_pattern_type = 'zombie_vision'

        self.parent = Enemy(enemy_type, row, col)
        super().__init__(enemy_type, row, col)

        #zombie specific vars
        self.turns_moving_in_same_direction = 0
        self.max_turns_moving_in_same_direction = 2

        self.prepare_action()

    def update_state(self):
        self.prev_prev_state = self.prev_state
        self.prev_state = self.state
        self.prev_saw_player = self.sees_player
        self.sees_player = self.can_see_player()
        #print(f'can enemy see player: {self.sees_player}')
        if self.prev_state != 'freeze':
            self.state = 'freeze'
        else:
            if self.is_diagonally_adjacent_to_player():
                self.state = 'attack'
            elif not self.sees_player and (self.prev_saw_player or self.prev_prev_state == 'pursuit') and (
                    self.prev_state == 'aggro' or self.prev_state == 'freeze'):
                self.state = 'pursuit'
            else:
                if self.sees_player:
                    self.state = 'aggro'
                else:
                    if self.prev_state != 'pursuit':
                        self.state = 'idle'

        #print(f'state: {self.state}')

    def prepare_action(self):
        self.update_state()

        match self.state:
            case 'idle':
                self.wander()
            case 'aggro':
                self.move_towards_player()
            case 'pursuit':
                if dungeon.tiles_indexed_by_coords[tuple(self.highlighted_coords)][get_btn]['text'] == game.wall:
                    self.state = 'freeze'
            case 'attack':
                self.prepare_to_attack_player()
            case 'freeze':
                pass

        self.steps_to_highlight_button()

    def action(self):
        if self.state == 'idle' or self.state == 'aggro' or self.state == 'pursuit':
            self.prev_coords = self.coords.copy()
            self.coords = dungeon.find_new_location(
                self.enemy_type,
                self.coords,
                self.prev_coords,
                self.vision_direction
            )
            dungeon.go_to_new_location(game.zombie, self.coords, self.prev_coords)
            self.tile_itself = dungeon.tiles_indexed_by_coords[tuple(self.coords)]
        elif self.state == 'attack':
            self.attack_player()

        # If state = freeze, do nothing

    def wander(self):
        if self.turns_moving_in_same_direction >= self.max_turns_moving_in_same_direction:
            self.prev_highlight_direction = self.highlight_direction
            self.highlight_direction = random.choice(orthogonal_directions)
            self.turns_moving_in_same_direction = 0
        else:
            self.turns_moving_in_same_direction += 1

    def prepare_to_attack_player(self):
        # Figure out attack direction
        enemy_row, enemy_col = self.coords
        player_row, player_col = player.coords
        #print(f'player coords during prepare attack: {player.coords}')

        row_delta = player_row - enemy_row
        col_delta = player_col - enemy_col

        # Normalize to -1, 0, 1
        row_step = max(-1, min(1, row_delta))
        col_step = max(-1, min(1, col_delta))

        self.highlight_direction = direction_map[(row_step, col_step)]

    def attack_player(self):
        if self.highlighted_tile[get_btn]['text'] == game.player:
            Combat(attacker=self, attacked=player)


class Combat:
    def __init__(self, attacker, attacked):
        attacked.hp -= attacker.damage
        if isinstance(attacker, Enemy):
            game.update_log('combat', [attacker.enemy_type, 'you', attacker.damage])
        else:
            game.update_log('combat', ['You', attacked.enemy_type, attacker.damage])

        if attacked.hp <= 0:
            attacked.kill_self()


"""class Chest:
    def __init__(self):
        self.chests_in_level = {}
        self.figure_out_their_locations()
        self.contents_all_chests = {
            2: [game.key, game.sword]
        }

    def figure_out_their_locations(self):
        self.chests_in_level.clear()
        chest_ind = 0
        for idx, wgt in dungeon.tiles.items():
            btn = wgt[get_btn]
            if btn['text'] == game.chest:
                self.chests_in_level[chest_ind] = [dungeon.coords[idx], 'closed']
                chest_ind += 1
        #print(self.chests_in_level)

    def open(self, coords):
        try:
            chest_index = list(self.chests_in_level.values()).index([coords, 'closed'])
            btn_index = list(dungeon.coords.values()).index(coords)
            self.chests_in_level[chest_index][getstate] = 'looted'
            dungeon.tiles[btn_index][get_btn].config(fg='maroon')

            # Gets specific item/s from contents of all chest dict first
            #print(self.contents_all_chests[dungeon.level])
            for item in self.contents_all_chests[dungeon.level]:
                inv.pick_up_item(item)
        except ValueError:
            pass
            #print('chest looted')
            # print(f"Inventory slot {index}: {inv.inventory[index]['text']}\nButton: {inv.inventory[index]}")"""


class Shadowcasting:
    def cast_light_in_octant(self, entity, entity_row, entity_col, radius, octant):
        shadowed_intervals = []

        for depth in range(1, radius + 1):
            for lateral in range(0, depth + 1):

                # Slopes for this tile
                left_slope = (lateral - 0.5) / (depth + 0.5)
                right_slope = (lateral + 0.5) / (depth - 0.5)

                # Check if tile is fully shadowed
                in_shadow = False
                for shadow_start, shadow_end in shadowed_intervals:
                    if shadow_start <= left_slope and right_slope <= shadow_end:
                        in_shadow = True
                        break

                if in_shadow:
                    continue

                tile_row, tile_col = self.transform_octant(
                    entity_row, entity_col, depth, lateral, octant
                )

                tile = dungeon.tiles_indexed_by_coords.get((tile_row, tile_col))
                if tile is None:
                    continue

                distance = depth
                if distance <= radius:
                    light_level = int(radius - distance + 1)
                    entity.light_levels_by_tile[tile] = max(
                        entity.light_levels_by_tile.get(tile, 0),
                        light_level
                    )

                # If tile blocks light, add a shadow interval
                if tile[get_btn]["text"] in game.opaque_objects:
                    self._add_shadow(shadowed_intervals, left_slope, right_slope)

            # Early exit: full shadow
            if shadowed_intervals == [(-1.0, 1.0)]:
                break

    @staticmethod
    def _add_shadow(shadows, start, end):
        new_shadows = []
        inserted = False

        for s, e in shadows:
            if e < start:
                new_shadows.append((s, e))
            elif end < s:
                if not inserted:
                    new_shadows.append((start, end))
                    inserted = True
                new_shadows.append((s, e))
            else:
                start = min(start, s)
                end = max(end, e)

        if not inserted:
            new_shadows.append((start, end))

        shadows.clear()
        shadows.extend(new_shadows)

    @staticmethod
    def transform_octant(entity_row, entity_col, depth, lateral, octant):
        match octant:
            case 0:  # N
                return entity_row - depth, entity_col + lateral
            case 1:  # NE
                return entity_row - lateral, entity_col + depth
            case 2:  # E
                return entity_row + lateral, entity_col + depth
            case 3:  # SE
                return entity_row + depth, entity_col + lateral
            case 4:  # S
                return entity_row + depth, entity_col - lateral
            case 5:  # SW
                return entity_row + lateral, entity_col - depth
            case 6:  # W
                return entity_row - lateral, entity_col - depth
            case 7:  # NW
                return entity_row - depth, entity_col - lateral


game = GameController()
vision = Shadowcasting()
dungeon = Dungeon()
inv = Inventory()
player = Player()
dungeon.locate_important_objects_and_entities()
dungeon.finished_loading = True


#chest = Chest()


# --- Input handling ---
def take_keyboard_input(event):
    key = event.keysym
    if not key:
        return
    if key.isalnum():
        key = key.lower()
    #print(key)
    player.parse_key_press(key)


window.bind('<KeyPress>', take_keyboard_input)
# noinspection PyTypeChecker
window.after(50, lambda: window.focus_force())
#print(inv.inventory[0][get_btn].winfo_reqwidth())
#print(inv.inventory[0][get_btn].winfo_reqheight())
window.mainloop()
