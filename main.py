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

# from PIL import ImageTk

# TO DO: COMBAT

if not macOS:
    BTN_WIDTH = 3
    BTN_HEIGHT = 3
else:
    BTN_WIDTH = 73
    BTN_HEIGHT = 73

getstate = 1
GET_ROW = 0
GET_COL = 1

getframe = 0
getbtn = 1

WIDTH = 1000
HEIGHT = 1080
HORIZONTAL_OFFSET = 0

window = tk.Tk()
window.configure(bg='black')
window.title("Land of Dardar")
window.geometry(f"{WIDTH}x{HEIGHT}+{HORIZONTAL_OFFSET}+0")
# window.state('zoomed')
# window.resizable(False, False)

super_small_font = font.Font(family="Courier", size=15)
small_font = font.Font(family="Courier", size=18)
large_font = font.Font(family="Courier", size=20)
very_large_font = font.Font(family="Courier", size=30)

inventory_frame = tk.Frame(window, width=500, bg='black')
blank_frame = tk.Frame(window, height=100, bg='black')
blank_frame_two = tk.Frame(window, width=100, bg='black')
dungeon_frame = tk.Frame(window, bg='black')
log_frame = tk.Frame(window, bg='black')

inventory_frame.grid(row=0, column=0, sticky='ns')
blank_frame.grid(row=1, column=0, sticky='ew')
dungeon_frame.grid(row=2, column=0, sticky='nsew')
blank_frame_two.grid(row=0, column=1, sticky='nsew')
log_frame.grid(row=2, column=2, sticky='nsew')

dummy_button = Button(window, text='ppp')

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

orthogonal_directions = ['up', 'down', 'left', 'right']


class GameController:
    def __init__(self):
        # Item, entity, and object glyphs
        if True:
            self.turn = 'player'
            self.player = ('\n'
                           ' @ \n'
                           '/|\\\n'
                           '/ \\\n')
            self.sword = '⸸'
            self.wall = ('▀▀ ▀▀ \n'
                         ' ▀▀ ▀▀\n'
                         '▀▀ ▀▀ \n'
                         ' ▀▀ ▀▀\n'
                         '▀▀ ▀▀ \n'
                         ' ▀▀ ▀▀')
            self.chest = '▣'
            self.key = '⚷'
            self.door = '\U0001F6AA'
            self.bars = ('\U000026D3\U000026D3\U000026D3\U000026D3\n'
                         '\U000026D3\U000026D3\U000026D3\U000026D3\n'
                         '\U000026D3\U000026D3\U000026D3\U000026D3\n'
                         '\U000026D3\U000026D3\U000026D3\U000026D3')
            self.exit = '✦'
            self.coin = '¤'
            self.zombie = 'Ψ'

        self.enemies = [self.zombie]

        self.enable_darkness = True

        self.testing = False

        self.interactable_singular_items = [self.key, self.sword]
        self.solid_objects = [self.wall, self.chest, self.exit, self.door, self.bars, self.interactable_singular_items,
                              self.enemies, self.player]

        self.original_bg = {
            self.wall: '#141414'
        }

        self.default_color = '#f0f0f0'
        self.default_highlight_color = 'yellow'
        self.freeze_color = 'light blue'
        self.enemy_alert_color = 'red'
        self.attack_color = 'maroon'

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
        font = large_font
        if btn_type == 'inventory':
            font = very_large_font
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
            case _:
                # anything else is treated as blank floor
                text = tile_char

        btn = Button(
            parent_frame,
            text=text,
            fg=fg,
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            font=font,
            activebackground=bg,
            activeforeground=fg,
            bg=bg,
            command=command
        )

        if macOS:
            # noinspection PyArgumentList
            btn.configure(takefocus=0, focuscolor='', borderless=1)

        return btn

    def advance_turn(self):
        if self.turn == 'player':
            self.turn = 'enemy'
            print(f'player coords while advancing turn: {player.coords}')
            for enemy in dungeon.current_enemies.values():
                enemy.action()
                enemy.prepare_action()
            self.turn = 'player'

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
        self.game_log.insert('1.0', text)
        self.game_log['state'] = 'disabled'

    def pass_action(self):
        pass


class Dungeon:
    def __init__(self):
        self.level = 0

        self.lowest_light_level_in_current_level = 0

        self.current_enemies = {}

        # Rendering/structures
        if True:
            self.tiles_indexed_by_coords = {}
            self.coords_indexed_by_tiles = {}

            self.max_row = 0
            self.max_col = 0

            self.dungeon_text = ''
            self.set_dungeon_text()
            self.build_level()

    def set_dungeon_text(self):
        self.finished_loading = False
        self.lowest_light_level_in_current_level = 0
        match self.level:
            case -2:
                self.dungeon_text = ("wwwwwwwwwwwwwwww\n"
                                     "woooooooooooooow\n"
                                     "wooooooowoooooow\n"
                                     "wooowooooozowoow\n"
                                     "woop⸸ooooooowoow\n"
                                     "woooooooooooooow\n"
                                     "wwwwwwwwwwwwwwww")
            case 0:
                self.dungeon_text = ("wwwwwwwwwwwwwwww\n"
                                     "wooooooooooooo⚷w\n"
                                     "wwbwwwowwwowwoww\n"
                                     "wooowooowooowoww\n"
                                     "wopowooowooowbww\n"
                                     "wo⚷owooowoooweww\n"
                                     "wwwwwwwwwwwwwwww")
            case 1:
                if not game.testing:
                    player.current_vision_pattern = 'player_vision_ver_2'
                self.dungeon_text = ("wwwwwwwwwwwwwww\n"
                                     "wwwwwwwpwwwwwww\n"
                                     "woooooo⸸oooooow\n"
                                     "wwowowwbwwwowww\n"
                                     "wwooowwewwwooow\n"
                                     "woowwwwwwwwowow\n"
                                     "wowwoooooooowow\n"
                                     "wowwwwwwowwozow\n"
                                     "wowoooowowwwoww\n"
                                     "wooowwoooooo⚷ww\n"
                                     "wwwwwwwwwwwwwww")
            case 2:
                self.dungeon_text = ("wwwwwwwwwwww\n"
                                     "pooooowwwwww\n"
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

        for ch in self.dungeon_text:
            if ch == '\n':
                row += 1
                col = 0
                continue

            new_frame = game.create_frame(dungeon_frame)
            new_frame.grid(row=row, column=col, sticky='nsew')
            btn = game.create_button(ch, new_frame, 'dungeon')
            btn.grid(row=row, column=col, sticky='nsew')

            #self.index_by_rows_and_cols[(row, col)] = idx

            self.tiles_indexed_by_coords[(row, col)] = [new_frame, btn]
            self.coords_indexed_by_tiles[new_frame, btn] = (row, col)

            if btn['text'] in game.enemies:
                self.current_enemies[enemy_idx] = (btn['text'], row, col)
                enemy_idx += 1

            self.max_row = max(self.max_row, row)
            self.max_col = max(self.max_col, col)

            col += 1
            idx += 1

    def find_new_location(self, entity, entity_coords, entity_prev_coords, direction):

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

        new_tile = self.tiles_indexed_by_coords[tuple(entity_coords)][getbtn]
        prev_tile = self.tiles_indexed_by_coords[tuple(entity_prev_coords)][getbtn]

        blocked = new_tile['text'] == game.player or new_tile['text'] in game.enemies or new_tile['text'] in game.interactable_singular_items or new_tile['text'] in game.solid_objects
        if blocked or new_tile is None:
            if entity == game.player:
                player.changed_location = False
            return entity_prev_coords

        prev_tile['text'] = ' '
        new_tile['text'] = entity

        return entity_coords

    def locate_important_objects_and_entities(self):
        for i, (enemy_type, row, col) in self.current_enemies.items():
            if enemy_type == game.zombie:
                self.current_enemies[i] = Enemy(enemy_type, row, col, 10, 4, 1)
        self.finished_loading = True

    def next_level(self):
        self.level += 1
        #print(self.tiles)
        for coords, (frame, btn) in dungeon.tiles_indexed_by_coords.items():
            frame.destroy()
            btn.destroy()

        self.set_dungeon_text()
        self.build_level()
        player.init_every_level()
        dungeon.locate_important_objects_and_entities()
        #chest.figure_out_their_locations()


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
            self.inventory[i - 1][getframe].grid(row=row, column=col)
            self.inventory[i - 1][getbtn].grid(row=row, column=col)
            col += 1
            if i % 5 == 0 and i != 0:
                row += 1
                col = 0

        #print(f'inventory: {self.inventory}')
        self.selected_item_slot = self.inventory[0]
        self.prev_selected_item_slot = self.inventory[0]
        self.inventory_highlighting(game.default_highlight_color)

    def equip_item(self, item):
        for i, slot in self.inventory.items():
            if slot[getbtn]['text'] == ' ':
                print('item equipped')
                slot[getbtn].config(text=item)
                game.update_log('item picked up', item)
                break

    def destroy_item(self, item):
        for i, slot in self.inventory.items():
            if slot[getbtn]['text'] == item:
                print('item destroyed')
                slot[getbtn].config(text=' ')
                break

    def select_item(self, slot):
        if macOS:
            slot[getbtn].config(state='active')
        else:
            slot[getbtn].config(default='active')

        self.prev_selected_item_slot = self.selected_item_slot
        self.selected_item_slot = slot

        if macOS:
            self.prev_selected_item_slot[getbtn].config(state='normal')
        else:
            self.prev_selected_item_slot[getbtn].config(default='normal')

        if self.selected_item_slot[getbtn]['text'] == game.sword:
            self.weapon_selected = True
        else:
            self.weapon_selected = False

        if self.weapon_selected:
            color = game.attack_color
        else:
            color = game.default_highlight_color

        self.inventory_highlighting(color)
        player.determine_highlighted_button()

    def inventory_highlighting(self, color):
        self.prev_selected_item_slot[getframe].configure(background=game.default_color)
        self.selected_item_slot[getframe].configure(background=color)

    def register_inventory_number(self, num):
        if num == '0':
            num = '10'
        selected_btn = self.inventory[int(num) - 1]
        self.select_item(selected_btn)


class Player:
    def __init__(self):
        self.coords = []
        self.highlight_direction = 'right'
        self.prev_highlight_direction = 'right'
        self.actual_vision_direction = 'right'
        self.prev_actual_vision_direction = 'right'

        self.highlight_color = game.default_highlight_color
        self.changed_location = False
        self.player_info = {'hp': 10, 'max_hp': 10, 'speed': 5}
        self.current_vision_pattern = "player_vision_ver_1"

        self.max_hp = 15
        self.hp = self.max_hp
        self.speed = 5

        self.init_every_level()

    def init_every_level(self):
        for coords, tile in dungeon.tiles_indexed_by_coords.items():
            if tile[getbtn]['text'] == game.player:
                self.coords = list(coords)
                self.tile_info = tile
        self.prev_coords = self.coords.copy()
        self.highlighted_coords = self.coords.copy()
        self.prev_highlighted_coords = None
        self.rendered_light_levels = {}
        self.update_player_vision()

    def update_player_vision(self):
        self.determine_highlighted_button()
        if game.enable_darkness:
            self.determine_vision_direction()
            self.render_vision()
        self.apply_highlight_to_button()

    def determine_vision_direction(self):
        self.prev_actual_vision_direction = self.actual_vision_direction
        if '_right' in self.highlight_direction and self.prev_actual_vision_direction == 'left':
            self.actual_vision_direction = 'right'
        elif '_left' in self.highlight_direction and self.prev_actual_vision_direction == 'right':
            self.actual_vision_direction = 'left'
        elif 'up_' in self.highlight_direction and self.prev_actual_vision_direction == 'down':
            self.actual_vision_direction = 'up'
        elif 'down_' in self.highlight_direction and self.prev_actual_vision_direction == 'up':
            self.actual_vision_direction = 'down'
        elif self.highlight_direction in orthogonal_directions:
            self.actual_vision_direction = self.highlight_direction

    def determine_highlighted_button(self):
        if inv.weapon_selected:
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

    def apply_highlight_to_button(self):
        highlight_tile = dungeon.tiles_indexed_by_coords[tuple(self.highlighted_coords)]
        highlight_tile[getframe].configure(bg=self.highlight_color)

    def interact(self):
        print('interaction')
        interacted_btn = dungeon.tiles_indexed_by_coords[tuple(self.highlighted_coords)][getbtn]
        interacted_spot = interacted_btn['text']
        print(f'interacted_spot: {interacted_spot}')
        if interacted_spot == game.chest:
            print('chest interaction')
            #chest.open(self.btn_highlighted_coords)
        elif (interacted_spot == game.bars or interacted_spot == game.door) and inv.selected_item_slot[getbtn]['text'] == game.key:
            print('bars interaction')
            interacted_btn.config(text=' ')
            inv.destroy_item(game.key)
        elif interacted_spot == game.exit:
            print('exited room')
            dungeon.next_level()
        elif interacted_spot in game.interactable_singular_items:
            for item in game.interactable_singular_items:
                if item == interacted_spot:
                    inv.equip_item(item)
                    interacted_btn.config(text=' ')
        elif interacted_spot in game.enemies and inv.weapon_selected:
            self.attack_enemy()

        game.advance_turn()

    def attack_enemy(self):
        for enemy in dungeon.current_enemies.values():
            if enemy.tile_info == dungeon.tiles_indexed_by_coords[tuple(self.highlighted_coords)]:
                damage = 1
                enemy.hp -= damage
                game.update_log('combat', ['You', enemy.enemy_type, damage])

                if enemy.hp <= 0:
                    enemy.kill_self()
                break

    def parse_key_press(self, key):
        if key in 'wasd':
            match key:
                case 'w':
                    movement_direction = 'up'
                case 'a':
                    movement_direction = 'left'
                case 's':
                    movement_direction = 'down'
                case 'd':
                    movement_direction = 'right'

            self.prev_coords = self.coords.copy()
            self.coords = dungeon.find_new_location(game.player, self.coords, self.prev_coords, movement_direction)
            if self.prev_coords == self.coords:
                self.changed_location = False
            else:
                self.changed_location = True

            if self.changed_location:
                self.update_player_vision()
                game.advance_turn()

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
            self.update_player_vision()
            for enemy in dungeon.current_enemies.values():
                enemy.steps_to_highlight_button()
        elif key == 'space':
            self.interact()
        elif key in '0123456789':
            inv.register_inventory_number(key)

    def determine_light_levels_of_tiles(self):

        light_levels_by_tile = {}

        player_row, player_col = self.coords
        vision_pattern = vision.patterns[self.current_vision_pattern][self.actual_vision_direction]

        def has_wall_at(row, col):
            tile = dungeon.tiles_indexed_by_coords.get((row, col))
            if tile is None:
                return False
            return tile[getbtn]['text'] == game.wall

        for light_level, offsets in vision_pattern.items():
            for row_offset, col_offset in offsets:
                target_row = player_row + row_offset
                target_col = player_col + col_offset

                steps = max(abs(row_offset), abs(col_offset))
                blocked = False

                for step in range(1, steps + 1):
                    check_row = player_row + round(row_offset * step / steps)
                    check_col = player_col + round(col_offset * step / steps)

                    if not (abs(row_offset) == abs(col_offset) == steps == 1):
                        if has_wall_at(check_row, check_col):
                            # allow the wall tile itself
                            if step != steps:
                                blocked = True
                            break
                    else:
                        #wall_row = player_row + row_offset
                        #wall_col = player_col + col_offset

                        block_row = player_row + row_offset
                        block_col = player_col

                        block_row_2 = player_row
                        block_col_2 = player_col + col_offset
                        if has_wall_at(block_row, block_col) and has_wall_at(block_row_2, block_col_2):
                            blocked = True
                            break

                if blocked:
                    continue

                tile = dungeon.tiles_indexed_by_coords.get((target_row, target_col))
                if tile is None:
                    continue

                tile_key = tuple(tile)
                light_levels_by_tile[tile_key] = max(light_levels_by_tile.get(tile_key, 0), light_level)

        return light_levels_by_tile

    def render_vision(self):
        new_light_levels = self.determine_light_levels_of_tiles()

        for coords, (frame, btn) in dungeon.tiles_indexed_by_coords.items():
            tile_key = (frame, btn)

            new_light_level = new_light_levels.setdefault(tile_key, dungeon.lowest_light_level_in_current_level)
            old_light_level = self.rendered_light_levels.setdefault(tile_key, dungeon.lowest_light_level_in_current_level)

            bypass = False

            if coords == tuple(self.prev_highlighted_coords):
                bypass = True

            if dungeon.finished_loading:
                for enemy in dungeon.current_enemies.values():
                    if coords == tuple(enemy.highlighted_coords) or coords == tuple(enemy.prev_highlighted_coords):
                        bypass = True

            if new_light_level == old_light_level and not bypass:
                continue

            # ─── TILE COLOR (lighting owns this) ───
            if new_light_level == 0:
                tile_color = 'black'
            elif btn['text'] == game.wall:
                tile_color = game.original_bg[game.wall]
            else:
                tile_color = game.lighting_colors[new_light_level]

            frame.configure(bg=tile_color)
            btn.configure(bg=tile_color, fg='black')

            self.rendered_light_levels[tile_key] = new_light_level


class Enemy:
    def __init__(self, enemy_type, row, col, max_hp, vision_range, movement_length):
        self.coords = [row, col]
        self.prev_coords = self.coords.copy()
        self.tile_info = dungeon.tiles_indexed_by_coords[tuple(self.coords.copy())]

        self.highlighted_coords = self.coords.copy()
        self.highlight_color = game.default_highlight_color
        self.prev_highlighted_coords = None

        self.enemy_type = enemy_type
        self.hp = max_hp
        self.max_hp = max_hp
        self.movement_length = movement_length

        self.state = 'freeze'
        self.prev_state = 'freeze'
        self.prev_prev_state = 'freeze'

        self.highlight_direction = 'right'
        self.prev_highlight_direction = 'right'
        self.do_highlight = False

        self.actual_vision_direction = 'right'
        self.prev_actual_vision_direction = 'right'

        self.vision_range = vision_range
        self.is_visible_to_player = False

        self.rendered_light_levels = self.determine_light_levels_of_tiles()

        #zombie specific vars
        self.turns_moving_in_same_direction = 2
        self.max_turns_moving_in_same_direction = 2
        self.sees_player = False

        self.prepare_action()

    def can_see_player(self):
        self.determine_vision_direction()
        self.rendered_light_levels = self.determine_light_levels_of_tiles()
        for (frame, btn), light_level in self.rendered_light_levels.items():
            if light_level == 0:
                continue
            if btn['text'] == game.player:
                return True
        return False

    def is_orthogonally_adjacent_to_player(self):
        enemy_row, enemy_col = self.coords
        player_row, player_col = player.coords
        return abs(enemy_row - player_row) <= 1 and abs(enemy_col - player_col) <= 1 and not (abs(enemy_row - player_row) == 1 and abs(enemy_col - player_col) == 1)

    def is_diagonally_adjacent_to_player(self):
        enemy_row, enemy_col = self.coords
        player_row, player_col = player.coords
        return abs(enemy_row - player_row) == 1 and abs(enemy_col - player_col) == 1

    def update_state(self):
        self.prev_prev_state = self.prev_state
        self.prev_state = self.state
        self.prev_saw_player = self.sees_player
        self.sees_player = self.can_see_player()
        print(f'can enemy see player: {self.sees_player}')
        if not self.sees_player and (self.prev_saw_player or self.prev_prev_state == 'pursuit') and (self.prev_state == 'aggro' or self.prev_state == 'freeze'):
            self.state = 'pursuit'
        else:
            if self.prev_state == 'freeze':
                if self.is_diagonally_adjacent_to_player():
                    self.state = 'attack'
                else:
                    if self.sees_player:
                        self.state = 'aggro'
                    else:
                        if self.prev_state != 'pursuit':
                            self.state = 'idle'
            elif self.prev_state != 'freeze':
                self.state = 'freeze'

        print(f'state: {self.state}', f'prev_prev_state: {self.prev_prev_state}')

    def check_self_visibility_and_highlight_status(self):
        if player.rendered_light_levels.get(tuple(self.tile_info)) != 0:
            self.is_visible_to_player = True
            self.do_highlight = True
        else:
            self.is_visible_to_player = False
            self.do_highlight = False

    def prepare_action(self):
        self.update_state()

        match self.state:
            case 'idle':
                self.wander()
            case 'aggro':
                self.move_towards_player()
            case 'pursuit':
                if dungeon.tiles_indexed_by_coords[tuple(self.highlighted_coords)][getbtn]['text'] == game.wall:
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
                self.actual_vision_direction
            )
            self.tile_info = dungeon.tiles_indexed_by_coords[tuple(self.coords)]
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

    def move_towards_player(self):
        entity_row, entity_col = self.coords
        player_row, player_col = player.coords

        if abs(player_row - entity_row) > abs(player_col - entity_col):
            self.highlight_direction = 'down' if player_row > entity_row else 'up'
        else:
            self.highlight_direction = 'right' if player_col > entity_col else 'left'

    def prepare_to_attack_player(self):
        # Figure out attack direction
        enemy_row, enemy_col = self.coords
        player_row, player_col = player.coords
        print(f'player coords during prepare attack: {player.coords}')

        row_delta = player_row - enemy_row
        col_delta = player_col - enemy_col

        # Normalize to -1, 0, 1
        row_step = max(-1, min(1, row_delta))
        col_step = max(-1, min(1, col_delta))

        self.highlight_direction = direction_map[(row_step, col_step)]

    def attack_player(self):
        if dungeon.tiles_indexed_by_coords[tuple(self.highlighted_coords)][getbtn]['text'] == game.player:
            damage = 1
            player.hp -= damage
            game.update_log('combat', [self.enemy_type, 'you', damage])

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

    def apply_highlight_to_button(self):
        highlight_tile = dungeon.tiles_indexed_by_coords[tuple(self.highlighted_coords)]
        highlight_tile[getframe].configure(bg=self.highlight_color)

    def steps_to_highlight_button(self):
        self.check_self_visibility_and_highlight_status()

        print(self.is_visible_to_player)

        self.determine_highlighted_button()

        if self.do_highlight:
            self.determine_highlight_color()
            self.apply_highlight_to_button()

    def determine_vision_direction(self):
        self.prev_actual_vision_direction = self.actual_vision_direction
        if '_right' in self.highlight_direction and self.prev_actual_vision_direction == 'left':
            self.actual_vision_direction = 'right'
        elif '_left' in self.highlight_direction and self.prev_actual_vision_direction == 'right':
            self.actual_vision_direction = 'left'
        elif 'up_' in self.highlight_direction and self.prev_actual_vision_direction == 'down':
            self.actual_vision_direction = 'up'
        elif 'down_' in self.highlight_direction and self.prev_actual_vision_direction == 'up':
            self.actual_vision_direction = 'down'
        elif self.highlight_direction in orthogonal_directions:
            self.actual_vision_direction = self.highlight_direction

    def determine_light_levels_of_tiles(self):

        light_levels_by_tile = {}

        enemy_row, enemy_col = self.coords
        vision_pattern = vision.patterns['zombie_vision'][self.actual_vision_direction]

        def has_wall_at(row, col):
            tile = dungeon.tiles_indexed_by_coords.get((row, col))
            if tile is None:
                return False
            return tile[getbtn]['text'] == game.wall

        for light_level, offsets in vision_pattern.items():
            for row_offset, col_offset in offsets:
                target_row = enemy_row + row_offset
                target_col = enemy_col + col_offset

                steps = max(abs(row_offset), abs(col_offset))
                blocked = False

                for step in range(1, steps + 1):
                    check_row = enemy_row + round(row_offset * step / steps)
                    check_col = enemy_col + round(col_offset * step / steps)

                    if step != steps and has_wall_at(check_row, check_col):
                        blocked = True
                        break

                if blocked:
                    continue

                tile = dungeon.tiles_indexed_by_coords.get((target_row, target_col))
                if tile is None:
                    continue

                tile_key = tuple(tile)
                light_levels_by_tile[tile_key] = max(light_levels_by_tile.get(tile_key, 0), light_level)

        return light_levels_by_tile

    def kill_self(self):
        self.tile_info[getbtn].config(text=' ')
        for i, enemy in dungeon.current_enemies.items():
            if enemy.coords == self.coords:
                highlighted_tile = dungeon.tiles_indexed_by_coords[tuple(self.highlighted_coords)]
                highlighted_tile[getframe].configure(bg=game.lighting_colors[player.rendered_light_levels[tuple(highlighted_tile)]])
                del dungeon.current_enemies[i]
                break


class Combat:
    def __init__(self):
        pass


class Chest:
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
            btn = wgt[getbtn]
            if btn['text'] == game.chest:
                self.chests_in_level[chest_ind] = [dungeon.coords[idx], 'closed']
                chest_ind += 1
        print(self.chests_in_level)

    def open(self, coords):
        try:
            chest_index = list(self.chests_in_level.values()).index([coords, 'closed'])
            btn_index = list(dungeon.coords.values()).index(coords)
            self.chests_in_level[chest_index][getstate] = 'looted'
            dungeon.tiles[btn_index][getbtn].config(fg='maroon')

            # Gets specific item/s from contents of all chest dict first
            print(self.contents_all_chests[dungeon.level])
            for item in self.contents_all_chests[dungeon.level]:
                inv.equip_item(item)
        except ValueError:
            print('chest looted')
            # print(f"Inventory slot {index}: {inv.inventory[index]['text']}\nButton: {inv.inventory[index]}")


class VisionPatternCreator:
    def __init__(self):
        self.patterns = {}
        self.row_and_col_offset_limits_per_orthogonal_direction_including_peripheral_vision = {
            'up': (1, 10000),
            'left': (10000, 1),
            'down': (-1, 10000),
            'right': (10000, -1)
        }
        self.row_and_col_offset_limits_per_orthogonal_direction_without_peripheral_vision = {
            'up': (0, 10000),
            'left': (10000, 0),
            'down': (0, 10000),
            'right': (10000, 0)
        }
        self.vision_range = 1
        self.current_row_and_col_limit_dict = self.row_and_col_offset_limits_per_orthogonal_direction_including_peripheral_vision
        self.create_player_vision_pattern_versions()
        self.create_enemy_vision_patterns()

    def the_pattern_forge(self, vision_pattern, base_light_level):
        self.patterns[vision_pattern] = {}
        for direction, (row_offset_limit, col_offset_limit) in self.current_row_and_col_limit_dict.items():
            current_dict = self.patterns[vision_pattern][direction] = {}
            for row_offset in range(-self.vision_range, self.vision_range + 1):
                for col_offset in range(-self.vision_range, self.vision_range + 1):
                    current_light_level = base_light_level - max(abs(row_offset), abs(col_offset))
                    if (row_offset < row_offset_limit and direction == 'up') or (row_offset > row_offset_limit and direction == 'down') or (col_offset < col_offset_limit and direction == 'left') or (col_offset > col_offset_limit and direction == 'right') or (row_offset == col_offset == 0):
                        current_dict.setdefault(current_light_level, []).append((row_offset, col_offset))

    def create_player_vision_pattern_versions(self):
        max_versions = 7
        for version in range(1, max_versions + 1):
            self.the_pattern_forge(f'player_vision_ver_{version}', 2+(version-1))
            #print(self.patterns[f'player_vision_ver_{version}'])
            self.vision_range += 1

    def create_enemy_vision_patterns(self):
        self.vision_range = 4
        self.the_pattern_forge('zombie_vision', 5)
        print(self.patterns[f'zombie_vision'])


game = GameController()
vision = VisionPatternCreator()
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
window.after(50, lambda: window.focus_force())
window.mainloop()
