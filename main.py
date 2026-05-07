import platform
import sys
import tkinter

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

#import tktooltip

#import idlelib.tooltip as tt

from PIL import ImageTk

# TO DO: COMBAT

getstate = 1
GET_ROW = 0
GET_COL = 1

get_frame = 0
get_btn = 1

WIDTH = 1920
HEIGHT = 1080
HORIZONTAL_OFFSET = 0
VERTICAL_OFFSET = 0

window = tk.Tk()
window.configure(bg='black')
window.title("Land of Dardar")
window.geometry(f"{WIDTH}x{HEIGHT}+{HORIZONTAL_OFFSET}+{VERTICAL_OFFSET}")
# window.state('zoomed')
# window.resizable(False, False)

super_small_font = font.Font(family="Courier", size=13-2)
small_font = font.Font(family="Courier", size=15-3)
medium_font = font.Font(family="Courier", size=17-3)
large_font = font.Font(family="Courier", size=20)
very_large_font = font.Font(family="Courier", size=30-2)
bold_large_font = font.Font(family="Courier", size=20-2, weight='bold')

big_left_frame = tk.Frame(window, bg='black')
big_right_frame = tk.Frame(window, bg='black')

big_left_frame.grid(row=0, column=0, sticky='ns')
big_right_frame.grid(row=0, column=1, sticky='ns')

#equipment_frame = tk.Frame(big_left_frame, width=450, height=1080 / 2, bg='black')
stats_frame = tk.Frame(big_left_frame, bg='black')
big_left_frame_horizontal_blank_frame = tk.Frame(big_left_frame, width=50, bg='black')

#equipment_frame.grid(row=0, column=0, sticky='ns')
stats_frame.grid(row=0, column=0)
big_left_frame_horizontal_blank_frame.grid(row=0, column=1, sticky='ew')

stats_header = tk.Label(stats_frame, text='Stats:', font=bold_large_font, bg='black', fg='white')
stats_vertical_blank_frame = tk.Frame(stats_frame, height=200, bg='black')
stats_horizontal_blank_frame = tk.Frame(stats_frame, width=50, bg='black')
stats_hp_text = tk.Label(stats_frame, text='HP: XX/XX', font=medium_font, bg='black', fg='white', width=16, anchor='w')
stats_damage_text = tk.Label(stats_frame, text='Damage: XX-XX', font=medium_font, bg='black', fg='white', width=16, anchor='w')
stats_speed_text = tk.Label(stats_frame, text='Speed: XX', font=medium_font, bg='black', fg='white', width=16, anchor='w')
stats_crit_chance_text = tk.Label(stats_frame, text='Crit Chance: XX%', font=medium_font, bg='black', fg='white', width=16, anchor='w')
stats_crit_multiplier_text = tk.Label(stats_frame, text='Crit Mult: XXx', font=medium_font, bg='black', fg='white', width=16, anchor='w')
stats_miss_chance_text = tk.Label(stats_frame, text='Miss Chance: XX%', font=medium_font, bg='black', fg='white', width=16, anchor='w')
stats_text_list = [stats_hp_text, stats_damage_text, stats_speed_text, stats_crit_chance_text, stats_crit_multiplier_text, stats_miss_chance_text]

stats_horizontal_blank_frame.grid(row=0, column=0, rowspan=100, sticky='ew')
stats_vertical_blank_frame.grid(row=0, column=2, sticky='ew')
stats_header.grid(row=1, column=1, sticky='ew')
stats_hp_text.grid(row=2, column=1)
stats_damage_text.grid(row=3, column=1)
stats_speed_text.grid(row=4, column=1)
stats_crit_chance_text.grid(row=5, column=1)
stats_crit_multiplier_text.grid(row=6, column=1)
stats_miss_chance_text.grid(row=7, column=1)

for text in stats_text_list:
    text.grid_propagate(False)

inventory_frame = tk.Frame(big_right_frame, width=500, bg='black')
horizontal_blank_frame = tk.Frame(big_right_frame, height=50, bg='black')
right_vertical_blank_frame = tk.Frame(big_right_frame, width=50, bg='black')
dungeon_frame = tk.Frame(big_right_frame, bg='black')
log_frame = tk.Frame(big_right_frame, bg='black')

inventory_frame.grid(row=0, column=1, sticky='n')
horizontal_blank_frame.grid(row=1, column=1, sticky='ew')
dungeon_frame.grid(row=2, column=1, sticky='ns')
right_vertical_blank_frame.grid(row=0, column=2, sticky='ns')
log_frame.grid(row=2, column=3, sticky='nsew')

dummy_button = Button(window, text='ppp')
dummy_frame = tk.Frame(window)
dummy_slot = (dummy_frame, dummy_button)

empty_img = tk.PhotoImage(width=1, height=1)

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
horizontal_directions = ['left', 'right']
vertical_directions = ['up', 'down']


class GameController:
    def __init__(self):
        self.testing = True
        # Item, entity, and object glyphs
        if True:
            self.turn = 'player'
            self.player = '@'
            self.dagger = '⸸'
            self.shortsword = '⊰═]二フ'
            self.whip = '𓍯𓂃𓂃'
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
                                '⛓⛓∅⛓\n'
                                '⛓⛓⛓⛓\n'
                                '⛓⛓⛓⛓')
            self.broken_bars = ('⛓ ⛓⛓\n'
                                '   ⛓\n'
                                '⛓⛓  \n'
                                ' ⛓ ⛓')
            self.exit_arrows = ['⏶', '⏴', '⏵', '⏷']
            self.direction_arrows = {
                'up_left': '↖',
                'up': '↑',
                'up_right': '↗',
                'left': '←',
                'down_left': '↙',
                'down': '↓',
                'down_right': '↘',
                'right': '→',
            }
            self.star = '✦'
            self.coin = '¤'
            self.zombie = 'Ψ'
            self.rock = '●'
            self.big_rock = '⬤'
            self.small_health_potion = '⚗'

        self.enable_darkness = True

        self.singular_interactable_items = [self.key, self.small_health_potion]
        self.enemies = [self.zombie]
        self.entities = [self.player, self.zombie]
        self.weapons = [self.dagger, self.shortsword, self.whip]
        self.singular_interactable_items.extend(self.weapons)

        # solid and opaque objects
        if True:
            self.solid_objects = [self.wall, self.chest, self.door, self.bars, self.locked_bars, self.rock, self.big_rock]
            self.solid_objects.extend(self.singular_interactable_items)
            self.solid_objects.extend(self.exit_arrows)
            self.solid_non_entities = self.solid_objects.copy()
            self.solid_objects.extend(self.entities)
            self.opaque_objects = [self.wall, self.door]
            #print(self.solid_objects)

        self.default_color = '#f0f0f0'

        self.default_highlight_color = 'yellow'
        self.freeze_color = 'light blue'
        self.enemy_alert_color = 'red'
        self.attack_color = 'maroon'

        self.highlight_colors = [self.default_highlight_color, self.freeze_color, self.enemy_alert_color,
                                 self.attack_color]

        self.lighting_colors = {
            -1: '#101010',
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

        self.entered_new_level = False
        self.updated_game_log_this_turn = False

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

        # Defaults
        btn_text = ' '
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
            case '-':
                btn_text = ' '
            case '@':
                btn_text = self.player
            case 'z':
                btn_text = self.zombie
            case 'w':
                btn_text = self.wall
            case 'c':
                btn_text = self.chest
                #fg = 'gold'
            case 'd':
                btn_text = self.door
            case 'b':
                btn_text = self.bars
            case '𝖇':
                btn_text = self.locked_bars
            case '𝘣':
                btn_text = self.broken_bars
            case 'k':
                btn_text = self.key
            case 'r':
                btn_text = self.rock
            case 'R':
                btn_text = self.big_rock
            case 'p':
                btn_text = self.small_health_potion
                #fg = 'red'
            case 's':
                btn_text = self.shortsword
            case '~':
                btn_text = self.whip
            case _:
                btn_text = tile_char

        btn = Button(
            parent_frame,
            text=btn_text,
            fg=fg,
            font=btn_font,
            activebackground=bg,
            activeforeground=fg,
            bg=bg,
            command=command
        )

        if macOS:
            # noinspection PyArgumentList
            btn.configure(takefocus=0, focuscolor='', borderless=1, focusthickness=0)
            if btn_type == 'dungeon':
                btn.configure(width=DUNGEON_BTN_WIDTH_IN_PIXELS, height=DUNGEON_BTN_HEIGHT_IN_PIXELS)
            """elif btn_type == 'inventory':
                btn.configure(width=INVENTORY_BTN_WIDTH_IN_PIXELS, height=INVENTORY_BTN_HEIGHT_IN_PIXELS)"""
        else:
            btn.grid(padx=BTN_PAD, pady=BTN_PAD, sticky='nsew')
            btn.configure(width=BTN_WIDTH, height=BTN_HEIGHT)


        btn.grid_propagate(False)

        """if btn_type == 'dungeon':
            btn.configure(relief='flat')"""

        return btn

    def advance_turn(self, player_action):
        game.updated_game_log_this_turn = False
        for entity, speed in dungeon.ordered_speed_of_current_entities.items():
            if entity == player:
                match player_action:
                    case 'movement':
                        player.steps_to_take_after_pressing_wasd()
                    case 'interaction':
                        player.interact()
                        if self.entered_new_level:
                            self.entered_new_level = False
                            break
            else:
                if entity.is_alive:
                    entity.action()
                    entity.prepare_action()
        # player.vision_changed = False
        for repetition in range(len(dungeon.dead_enemies_this_turn)):
            self.erase_entity()
        player.render_vision()
        player.erase_highlight_from_prev_btn()
        for enemy in dungeon.current_enemies.values():
            enemy.steps_to_highlight_button()
            if player.attack_mode and enemy.coords in player.highlighted_coords_list:
                player.miss_chance = (enemy.speed / player.speed) * 10
                game.update_player_stats(['miss chance'])
        player.apply_highlight_to_button()

        game.update_log('add turn division', None)

    def make_log(self):
        self.game_log = tk.scrolledtext.ScrolledText(log_frame,
                                                     width=26,
                                                     height=32,
                                                     state='disabled',
                                                     undo=True,
                                                     font=super_small_font,
                                                     wrap='word'
                                                     )
        self.game_log.grid(row=0, column=0)

    def update_log(self, event_type, event_objects):
        if event_type == 'item picked up':
            if event_objects == game.small_health_potion:
                event_objects = 'Small Health Potion'
            log_text = f"{event_objects} has been picked up!\n"
            """first_word, other_text = text.split(' ', 1)
            text_list = [first_word, other_text]
            first_word.title()
            " ".join(text_list)
            print(text_list)"""
        elif event_type == 'combat':
            attacker, attacked, damage = event_objects
            log_text = f"{attacker} hit {attacked} for {damage} damage!\n"
        elif event_type == 'missed attack':
            attacker, attacked = event_objects
            log_text = f"{attacker} missed {attacked}!\n"
        elif event_type == 'killed entity':
            attacker, attacked = event_objects
            log_text = f"{attacker} {random.choice(['murdered', 'killed', 'exsanguinated', 'slayed', 'dispatched', 'took care of', 'executed', 'slaughtered', 'felled', 'took out', 'annihilated', 'blotted out', 'removed', 'terminated', 'exterminated', 'neutralized', 'liquidated', 'erased', 'obliterated', 'wasted'])} {attacked}!\n"
        elif event_type == 'add turn division':
            if self.updated_game_log_this_turn:
                print('division time!!')
                log_text = '\n'
                print(self.game_log['width'])
                for char in range(int(self.game_log['width'])):
                    log_text += '-'
                log_text += '\n\n'
            else: log_text = ''
        self.game_log['state'] = 'normal'
        # noinspection PyUnboundLocalVariable
        self.game_log.insert('1.0', log_text)
        self.game_log['state'] = 'disabled'
        self.updated_game_log_this_turn = True

    def pass_action(self):
        pass

    @staticmethod
    def erase_entity():
        for key, enemy in dungeon.dead_enemies_this_turn.items():
            highlighted_tile = dungeon.tiles_indexed_by_coords[tuple(enemy.highlighted_coords)]
            highlighted_tile[get_frame].configure(bg=game.lighting_colors[player.rendered_light_levels[tuple(highlighted_tile)]])
            enemy_index = next((key for key, val in dungeon.current_enemies.items() if val == enemy), None)
            del dungeon.speed_of_current_entities[enemy]
            del dungeon.ordered_speed_of_current_entities[enemy]
            del dungeon.current_enemies[enemy_index]
            del dungeon.current_entities[enemy_index]
            del dungeon.dead_enemies_this_turn[key]
            break

    @staticmethod
    def update_player_stats(list_of_updates):
        for update in list_of_updates:
            match update:
                case 'hp':
                    stats_hp_text['text'] = f'HP: {player.hp}/{player.max_hp}'
                case 'damage':
                    minimum_damage = weapons.damage_extremes[player.weapon_equipped][0]
                    maximum_damage = weapons.damage_extremes[player.weapon_equipped][-1]
                    if minimum_damage != maximum_damage:
                        stats_damage_text['text'] = f'Damage: {minimum_damage}-{maximum_damage}'
                    else:
                        stats_damage_text['text'] = f'Damage: {minimum_damage}'
                case 'speed':
                    stats_speed_text['text'] = f'Speed: {player.speed}'
                case 'crit chance':
                    stats_crit_chance_text['text'] = f'Crit Chance: {player.crit_chance}%'
                case 'crit multiplier':
                    stats_crit_multiplier_text['text'] = f'Crit Mult: {player.crit_multiplier}x'
                case 'miss chance':
                    stats_miss_chance_text['text'] = f'Miss Chance: {player.miss_chance}%'

    def add_arrow_equivalent_to_looking_dir(self, entity, entity_tile, highlight_direction):
        entity_tile[get_btn]['text'] = entity
        arrow_used = self.direction_arrows[highlight_direction]
        entity_tile[get_btn]['text'] += f'\n{arrow_used}'


class Dungeon:
    def __init__(self):
        self.level = 2

        self.lowest_light_level_in_current_level = 0

        self.current_enemies = {}

        self.current_entities = {}
        self.speed_of_current_entities = {}
        # The speed is now in descending order, meaning that higher speed entities have a higher index, meaning they go first
        self.ordered_speed_of_current_entities = {}
        self.dead_enemies_this_turn = {}

        self.entity_dicts = {'current_enemies': self.current_enemies,
                             'current_entities': self.current_entities,
                             'speed_of_current_entities': self.speed_of_current_entities,
                             'ordered_speed_of_current_entities': self.ordered_speed_of_current_entities}

        self.finished_loading = False

        # Rendering/structures
        if True:
            self.tiles_indexed_by_coords = {}
            self.coords_indexed_by_tiles = {}
            self.tile_contents_indexed_by_coords = {}

            self.max_row = 0
            self.max_col = 0

            self.level_text = ''
            self.set_level_text()
            self.build_level()

    def set_level_text(self):
        # Max rows: 15
        # Max cols: 28
        # copy-paste able characters:
        # 𝖇 ⏴ ⏶ ⏵ ⏷ ⸸
        self.lowest_light_level_in_current_level = 0
        match self.level:
            case -9999:
                self.level_text = ("wwwwwwwwwwwwwwwwwwwwwwwwwww\n"
                                   "w------------\n"
                                   "w-------w--@-\n"
                                   "w---w-------w\n"
                                   "w-----------w\n"
                                   "w------------\n"
                                   "w------------\n"
                                   "w------------\n"
                                   "w------------\n"
                                   "w------------\n"
                                   "wwwwwwwwwwwww\n"
                                   "wwwwwwwwwwwww\n"
                                   "wwwwwwwwwwwww\n"
                                   "wwwwwwwwwwwww\n")
            case -2:
                self.level_text = ("wwwwwwwwwwwwwwww\n"
                                   "w--------------w\n"
                                   "w-------w------w\n"
                                   "w---w-----z-w--w\n"
                                   "w--@⸸-------w--w\n"
                                   "w--------------w\n"
                                   "wwwwwwwwwwwwwwww")
            case 1:
                self.level_text = ("wwwwwwwwwwwwwwwwwwwwwwwwwww\n"
                                   "--Rr-R-------R-r----R-wwwww\n"
                                   "---------------------rb---w\n"
                                   "wwwwb-bwbb-wb𝖇bw-bbw--b---w\n"
                                   "---w---w---wr--w---w--b---w\n"
                                   "---w---w---w-krw-p-w-Rwwwww\n"
                                   "---w---w--pw@--w---w--b---w\n"
                                   "wwwwwwwwwwwwwwwwwwww-rb---w\n"
                                   "---w---w--pw---w---w--b---w\n"
                                   "---w-R-w---wR--w---w--wwwww\n"
                                   "---w---wz-rw--rwRr-w--b---w\n"
                                   "wwww---wb--w---w--bw--b---w\n"
                                   "⏴-------r-------------b---w\n"
                                   "⏴-----------R---R-----wwwww\n"
                                   "wwwwwwwwwwwwwwwwwwwwwwwwwww\n")
            case 2:
                if not game.testing:
                    player.vision_radius = 3
                self.level_text = ("wwwwwwwwwwwwwwwwwwwwwwwwwww\n"
                                   "wwwwwwwwwwwww@wwwwwwwwwwwww\n"
                                   "wwwwwww-----~⸸s-----wwwwwww\n"
                                   "wwwwwww-w-w-w𝖇ww-ww-wwwwwww\n"
                                   "wwwwwww-----w⏷w---w-wwwwwww\n"
                                   "wwwwwwww-ww-www-w---wwwwwww\n"
                                   "wwwwwwww--------ww-wwwwwwww\n"
                                   "wwwwwww--w-wwww----wwwwwwww\n"
                                   "wwwwwww-ww----w----wwwwwwww\n"
                                   "wwwwwww----ww-----wwwwwwwww\n"
                                   "wwwwwwwwwwwwwww-zzwwwwwwwww\n"
                                   "wwwwwwwwwwwwwwwzz-wwwwwwwww\n"
                                   "wwwwwwwwwwwwwww-kzwwwwwwwww\n"
                                   "wwwwwwwwwwwwwwwwwwwwwwwwwww\n")
            case 9999:
                self.level_text = ("wwwwwwwwwwww\n"
                                   "p⸸----wwwwww\n"
                                   "w--c----z--e\n"
                                   "w-----wwwwww\n"
                                   "wwwwwwwwwwww")
            case _:
                window.destroy()
                sys.exit(0)

    def build_level(self):
        # Clear old widgets
        self.tiles_indexed_by_coords.clear()
        self.coords_indexed_by_tiles.clear()
        self.tile_contents_indexed_by_coords.clear()
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

        if new_tile is not None:
            if self.tile_is_blocked(new_tile, game.solid_objects):
                if entity == game.player:
                    player.changed_location = False
                return prev_entity_coords

        return entity_coords

    @staticmethod
    def tile_is_blocked(the_btn, objects_to_check):
        return any(obj in the_btn['text'] for obj in objects_to_check)

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

    def next_level(self):
        self.finished_loading = False
        game.entered_new_level = True
        self.level += 1
        #print(self.tiles)
        for coords, (frame, btn) in self.tiles_indexed_by_coords.items():
            frame.destroy()
            btn.destroy()

        for entity_dict in self.entity_dicts.values():
            entity_dict.clear()

        self.tiles_indexed_by_coords.clear()

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
        self.weapon_just_selected = False
        self.prev_inv_number_pressed = 10
        self.inv_number_pressed = 1
        row = 0
        col = 0
        for i in range(1, 11):
            new_frame = game.create_frame(inventory_frame)
            new_btn = game.create_button(' ', new_frame, 'inventory')
            self.inventory[i - 1] = [new_frame, new_btn]
            new_frame.grid(row=row, column=col, sticky='nsew')
            new_frame.grid_rowconfigure(row, weight=1)
            new_frame.grid_columnconfigure(col, weight=1)
            new_frame.grid_propagate(False)
            new_btn.grid(row=row, column=col, sticky='nsew')
            new_btn.grid_propagate(False)
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
                game.update_log('item picked up', item)
                if item == game.small_health_potion:
                    self.change_inventory_slot_fg(slot, item)
                if item in [game.shortsword]:
                    slot[get_btn]['font'] = small_font
                if item in game.weapons:
                    self.influence_player_highlight()
                break

    def destroy_selected_item(self):
        slot = self.selected_item_slot
        item = slot[get_btn]['text']
        if item == game.small_health_potion:
            self.change_inventory_slot_fg(self.selected_item_slot, 'destroyed')
        slot[get_btn]['text'] = ' '

    def select_item(self, slot):
        self.prev_selected_item_slot = self.selected_item_slot
        self.selected_item_slot = slot

        self.prev_inv_number_pressed = self.inv_number_pressed
        self.inv_number_pressed = next((key for key, value in self.inventory.items() if value == self.selected_item_slot), None)

        #print(self.selected_item_slot)
        """for slot_ind, slot in self.inventory.items():
            if slot == self.selected_item_slot:
                #print(slot_ind)"""

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
            if self.prev_inv_number_pressed == self.inv_number_pressed:
                self.selected_item_slot = dummy_slot

    def register_inventory_number(self, num):
        self.prev_inv_number_pressed = self.inv_number_pressed
        if num == '0':
            num = '10'
        self.inv_number_pressed = num
        self.select_item(self.inventory[int(num) - 1])

    def influence_player_highlight(self):
        print(self.selected_item_slot)
        selected_item = self.selected_item_slot[get_btn]['text']
        if selected_item in game.weapons:
            self.weapon_selected = True
            self.weapon_just_selected = True
            player.weapon_equipped = selected_item
        else:
            self.weapon_selected = False
            player.weapon_equipped = None

        player.highlight_range, player.crit_chance, player.crit_multiplier, player.speed = weapons.adjust_stats(selected_item)

        game.update_player_stats(['damage', 'crit chance', 'crit multiplier', 'speed', 'miss_chance'])

        player.steps_to_take_after_pressing_looking_keys()

        self.weapon_just_selected = False

    @staticmethod
    def change_inventory_slot_fg(slot, item):
        match item:
            case game.small_health_potion:
                slot[get_btn]['fg'] = 'red'
            case _:
                slot[get_btn]['fg'] = 'black'


class Player:
    def __init__(self):
        self.coords = []
        self.highlight_direction = 'up'
        self.prev_highlight_direction = 'left'
        self.vision_direction = 'up'
        self.prev_vision_direction = 'left'

        self.highlight_color = game.default_highlight_color
        self.highlight_range = 1

        self.changed_location = False
        self.vision_changed = True

        self.max_hp = 15
        self.hp = self.max_hp
        self.normal_speed = 10
        self.speed = self.normal_speed
        self.damage = 0
        self.crit_chance = 0
        self.crit_multiplier = 0
        # This 20 means 20%
        self.miss_chance = 0
        if not game.testing:
            self.vision_radius = 2
        else:
            self.vision_radius = 3

        self.weapon_equipped = None

        self.highlighting_diagonally_adjacent_tile = False  # an entity can only attack diagonals
        self.attack_mode = False

        self.init_every_level()

    def init_every_level(self):
        self.rendered_light_levels = {}
        self.prev_light_levels = {}
        #print(dungeon.tiles_indexed_by_coords)
        for coords, (frame, btn) in dungeon.tiles_indexed_by_coords.items():
            self.rendered_light_levels[(frame, btn)] = 0
            if btn['text'] == game.player:
                self.coords = list(coords)
                self.tile_itself = (frame, btn)

        dungeon.current_entities[len(dungeon.current_entities)] = self
        dungeon.speed_of_current_entities[self] = self.speed
        self.prev_coords = self.coords.copy()
        self.highlighted_coords_list = []
        self.prev_highlighted_coords_list = []
        self.highlighted_tile_list = []
        self.prev_highlighted_tile_list = []

        self.determine_vision_direction()
        self.render_vision()
        self.determine_highlighted_buttons()
        self.apply_highlight_to_button()
        game.add_arrow_equivalent_to_looking_dir(game.player, self.tile_itself, self.highlight_direction)

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

    def determine_highlighted_buttons(self):
        #print(f'is weap selected?: {inv.weapon_selected} and {self.attack_mode}')

        self.determine_highlighted_color()

        self.prev_highlighted_coords_list = self.highlighted_coords_list.copy()
        self.prev_highlighted_tile_list = self.highlighted_tile_list.copy()
        self.highlighted_coords_list.clear()
        self.highlighted_tile_list.clear()

        self.current_highlighted_coords = self.coords.copy()
        for i in range(self.highlight_range):
            match self.highlight_direction:
                case 'up_left':
                    self.current_highlighted_coords[GET_ROW] -= 1
                    self.current_highlighted_coords[GET_COL] -= 1
                case 'up':
                    self.current_highlighted_coords[GET_ROW] -= 1
                case 'up_right':
                    self.current_highlighted_coords[GET_ROW] -= 1
                    self.current_highlighted_coords[GET_COL] += 1
                case 'left':
                    self.current_highlighted_coords[GET_COL] -= 1
                case 'right':
                    self.current_highlighted_coords[GET_COL] += 1
                case 'down_left':
                    self.current_highlighted_coords[GET_ROW] += 1
                    self.current_highlighted_coords[GET_COL] -= 1
                case 'down':
                    self.current_highlighted_coords[GET_ROW] += 1
                case 'down_right':
                    self.current_highlighted_coords[GET_ROW] += 1
                    self.current_highlighted_coords[GET_COL] += 1
                case 'self':
                    pass
                case _:
                    return

            if tuple(self.current_highlighted_coords) in dungeon.tiles_indexed_by_coords:
                highlighted_tile = dungeon.tiles_indexed_by_coords[tuple(self.current_highlighted_coords)]
                self.highlighted_tile_list.append(highlighted_tile)
                #print(self.current_highlighted_coords)
                self.highlighted_coords_list.append(self.current_highlighted_coords.copy())

            #print(f'highlighted_tile_list: {self.highlighted_tile_list}, prev_highlighted_tile_list: {self.prev_highlighted_tile_list}')
            #print(f'highlighted_coords_list: {self.highlighted_coords_list}, prev_highlighted_coords_list: {self.prev_highlighted_coords_list}')

    def determine_highlighted_color(self):
        #print(self.highlight_direction)
        if self.attack_mode and inv.weapon_selected:
            self.highlight_color = game.attack_color
        else:
            self.highlight_color = game.default_highlight_color

    def apply_highlight_to_button(self):
        #print(self.highlighted_coords_list)
        for highlighted_tile in self.highlighted_tile_list:
            if highlighted_tile is not None:
                #print('highlighted!')
                highlighted_tile[get_frame].configure(bg=self.highlight_color)

    def erase_highlight_from_prev_btn(self):
        for prev_highlighted_tile in self.prev_highlighted_tile_list:
            if prev_highlighted_tile is not None:
                light_level = self.rendered_light_levels[prev_highlighted_tile]
                if light_level == 0:
                    light_level = -1
                prev_highlighted_tile[get_frame].configure(bg=game.lighting_colors[light_level])

    def interact(self):
        #('interaction')
        interacted_tile_number = 0
        prev_interacted_btn = None
        prev_interacted_spots_list = []
        prev_interacted_btns_list = []
        for highlighted_coords in self.highlighted_coords_list:
            interacted_tile = dungeon.tiles_indexed_by_coords[tuple(highlighted_coords)]
            interacted_btn = interacted_tile[get_btn]
            interacted_spot = interacted_btn['text']
            interacted_tile_number += 1
            print(f'interacted_spot: {interacted_spot}')
            if tuple(interacted_tile) in self.rendered_light_levels:
                #print(f'is blocked?: {any(dungeon.tile_is_blocked(btn) for btn in prev_interacted_btns_list)}')
                if not self.attack_mode:
                    if interacted_spot == game.chest:
                        pass
                        #print('chest interaction')
                        #chest.open(self.btn_highlighted_coords)
                    elif (interacted_spot == game.locked_bars or interacted_spot == game.door) and \
                            inv.selected_item_slot[get_btn]['text'] == game.key:
                        #print('locked bars interaction')
                        interacted_btn.config(text=' ')
                        inv.destroy_selected_item()
                    elif interacted_spot in game.exit_arrows:
                        #print('exited room')
                        dungeon.next_level()
                    elif interacted_spot in game.singular_interactable_items:
                        for item in game.singular_interactable_items:
                            if item == game.small_health_potion:
                                interacted_btn['fg'] = 'black'
                            if item == interacted_spot:
                                inv.pick_up_item(item)
                                interacted_btn.config(text=' ')
                                break
                elif any(enemy in interacted_spot for enemy in game.enemies) and self.attack_mode:
                    if prev_interacted_btn is not None and self.highlight_range > 1 and any(dungeon.tile_is_blocked(btn, game.solid_non_entities) and btn['text'] not in game.enemies for btn in prev_interacted_btns_list):
                        print('no interaction')
                    else:
                        for enemy in dungeon.current_enemies.values():
                            if enemy.tile_itself == interacted_tile:
                                distance_to_enemy = interacted_tile_number
                                self.damage = weapons.calculate_its_damage(inv.selected_item_slot[get_btn]['text'], distance_to_enemy)
                                print('player attack')
                                Combat(attacker=self, attacked=enemy)
                                break
            if self.highlight_range > 1:
                prev_interacted_btn = interacted_btn
                prev_interacted_spot = interacted_spot
                prev_interacted_btns_list.append(prev_interacted_btn)
                prev_interacted_spots_list.append(prev_interacted_spot)

    def consume_item(self):
        if inv.selected_item_slot[get_btn]['text'] == game.small_health_potion:
            # print('potion drunk')
            self.hp += 5
            game.update_player_stats(['hp'])
            inv.destroy_selected_item()
            """if self.hp > self.max_hp:
                self.hp = self.max_hp"""

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
                self.determine_highlighted_buttons()
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

            self.steps_to_take_after_pressing_looking_keys()

        elif key == 'e':
            self.consume_item()
            game.advance_turn('interaction')

        elif key == 'space':
            game.advance_turn('interaction')
        elif key in '0123456789':
            inv.register_inventory_number(key)

    def steps_to_take_after_pressing_wasd(self):
        dungeon.go_to_new_location(game.player, self.coords, self.prev_coords)
        game.add_arrow_equivalent_to_looking_dir(game.player, self.tile_itself, self.highlight_direction)

    def steps_to_take_after_pressing_looking_keys(self):
        if '_' in self.highlight_direction and inv.weapon_selected:
            self.attack_mode = True
        else:
            self.attack_mode = False

        self.determine_vision_direction()

        if not self.attack_mode:
            self.highlight_range = 1
        else:
            self.highlight_range = weapons.weapon_range

        if inv.weapon_just_selected:
            self.determine_highlighted_buttons()
            self.erase_highlight_from_prev_btn()
            self.apply_highlight_to_button()
            return

        if self.prev_highlight_direction != self.highlight_direction:
            self.determine_highlighted_buttons()
        if self.prev_vision_direction != self.vision_direction:
            self.render_vision()

        if self.prev_highlight_direction != self.highlight_direction:
            self.erase_highlight_from_prev_btn()

        for enemy in dungeon.current_enemies.values():
            enemy.steps_to_highlight_button()
            if self.attack_mode and enemy.coords in self.highlighted_coords_list:
                self.miss_chance = (enemy.speed / self.speed) * 10
                game.update_player_stats(['miss chance'])

        self.apply_highlight_to_button()
        if self.prev_highlight_direction != self.highlight_direction:
            game.add_arrow_equivalent_to_looking_dir(game.player, self.tile_itself, self.highlight_direction)

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

        new_light_levels = self.determine_light_levels_of_tiles()

        if self.vision_changed:
            for (frame, btn), new_light_level in new_light_levels.items():
                old_light_level = self.prev_rendered_light_levels[(frame, btn)]

                if new_light_level == old_light_level:
                    continue

                tile_color = game.lighting_colors[new_light_level]

                frame.configure(bg=tile_color)
                if btn['text'] != game.small_health_potion:
                    btn.configure(bg=tile_color, fg='black')
                else:
                    btn.configure(bg=tile_color, fg='red')

                self.rendered_light_levels[(frame, btn)] = new_light_level

            for (frame, btn), _ in self.prev_light_levels.items():
                if (frame, btn) not in new_light_levels:
                    tile_color = game.lighting_colors[0]
                    frame['bg'] = btn['bg'] = btn['fg'] = tile_color

                    self.rendered_light_levels[(frame, btn)] = 0
        else:
            self.rendered_light_levels = new_light_levels.copy()

        self.prev_light_levels = new_light_levels.copy()

        self.vision_changed = True

    def kill_self(self):
        pass


class Enemy:
    def __init__(self, enemy_type, row, col):
        self.coords = [row, col]
        self.prev_coords = self.coords.copy()
        self.last_rendered_coords = self.coords.copy()
        self.potential_coords = []
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

        self.is_alive = True

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
        if player.rendered_light_levels.get(self.tile_itself, 0) > 0:
            self.is_visible_to_player = True
            self.do_highlight = True
        else:
            self.is_visible_to_player = False
            self.do_highlight = False

    def look_towards_player(self):
        entity_row, entity_col = self.coords
        player_row, player_col = player.coords

        player_more_vertical = abs(player_row - entity_row) > abs(player_col - entity_col)

        if player_more_vertical:
            initial_temp_dir = 'down' if player_row > entity_row else 'up'
        else:
            initial_temp_dir = 'right' if player_col > entity_col else 'left'

        self.figure_out_potential_coords(initial_temp_dir)
        temp_row, temp_col = self.potential_coords
        tile_btn = dungeon.tiles_indexed_by_coords[(temp_row, temp_col)][get_btn]
        #print(f'temp: {initial_temp_dir}, {tile_btn['text']}')
        if not dungeon.tile_is_blocked(tile_btn, game.solid_objects):
            self.highlight_direction = initial_temp_dir
            return
        else:
            if player_more_vertical:
                temp_directions = horizontal_directions.copy()
            else:
                temp_directions = vertical_directions.copy()

            random.shuffle(temp_directions)

            for temp_dir in temp_directions:
                #print(f'tempy: {temp_dir}')
                self.figure_out_potential_coords(temp_dir)
                temp_row, temp_col = self.potential_coords
                if (temp_row, temp_col) not in dungeon.tiles_indexed_by_coords:
                    continue
                tile_btn = dungeon.tiles_indexed_by_coords[(temp_row, temp_col)][get_btn]
                if not dungeon.tile_is_blocked(tile_btn, game.solid_objects):
                    self.highlight_direction = temp_dir
                    #print('yay')
                    return
        return

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

    def figure_out_potential_coords(self, temp_direction):
        self.potential_coords = self.coords.copy()

        match temp_direction:
            case 'up_left':
                self.potential_coords[GET_ROW] -= 1
                self.potential_coords[GET_COL] -= 1
            case 'up':
                self.potential_coords[GET_ROW] -= 1
            case 'up_right':
                self.potential_coords[GET_ROW] -= 1
                self.potential_coords[GET_COL] += 1
            case 'left':
                self.potential_coords[GET_COL] -= 1
            case 'right':
                self.potential_coords[GET_COL] += 1
            case 'down_left':
                self.potential_coords[GET_ROW] += 1
                self.potential_coords[GET_COL] -= 1
            case 'down':
                self.potential_coords[GET_ROW] += 1
            case 'down_right':
                self.potential_coords[GET_ROW] += 1
                self.potential_coords[GET_COL] += 1
            case 'self':
                pass
            case _:
                return

    def apply_highlight_to_button(self):
        frame, btn = self.highlighted_tile
        frame.configure(bg=self.highlight_color)

    def erase_highlight_from_prev_btn(self):
        light_level = player.rendered_light_levels.get(self.prev_highlighted_tile, 0)
        if light_level == 0:
            light_level = -1
        self.prev_highlighted_tile[get_frame].configure(bg=game.lighting_colors[light_level])
        #print(self.prev_coords, player.rendered_light_levels.get(self.prev_highlighted_tile, 0))

    def steps_to_highlight_button(self):
        self.check_self_visibility_and_highlight_status()
        #print(f'is enemy visible to player: {self.is_visible_to_player}')

        self.determine_highlighted_button()
        self.erase_highlight_from_prev_btn()

        if self.do_highlight:
            self.determine_highlight_color()
            self.apply_highlight_to_button()

        game.add_arrow_equivalent_to_looking_dir(self.enemy_type, self.tile_itself, self.highlight_direction)

        self.potential_coords = []

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
        self.is_alive = False
        dungeon.dead_enemies_this_turn[len(dungeon.dead_enemies_this_turn)] = self


class Zombie(Enemy):
    def __init__(self, enemy_type, row, col):
        self.max_hp = 10
        self.hp = self.max_hp
        self.vision_radius = 4
        self.movement_length = 1
        self.damage_range = [1, 2, 3]
        self.damage = None
        self.speed = 2
        self.crit_chance = 10
        self.crit_multiplier = 1.5
        self.miss_chance = None

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
            if self.is_orthogonally_adjacent_to_player():
                self.state = 'aggro'
            elif self.is_diagonally_adjacent_to_player():
                self.state = 'attack'
            else:
                if self.sees_player:
                    self.state = 'aggro'
                else:
                    if self.prev_state != 'pursuit':
                        self.state = 'idle'

        #print(f'state: {self.state}')

    def prepare_action(self):
        self.update_state()
        #print(f'state: {self.state}')

        match self.state:
            case 'idle':
                self.wander()
            case 'aggro':
                if not self.is_orthogonally_adjacent_to_player():
                    self.look_towards_player()
                else:
                    self.prepare_sidestep()
            case 'attack':
                self.prepare_to_attack_player()

            # If state = freeze, do nothing

    def action(self):
        self.determine_vision_direction()
        #print(f'statey: {self.state}')
        if self.state == 'idle' or self.state == 'aggro':
            self.prev_coords = self.coords.copy()
            self.coords = dungeon.find_new_location(
                self.enemy_type,
                self.coords,
                self.prev_coords,
                self.vision_direction
            )
            self.tile_itself = dungeon.tiles_indexed_by_coords[tuple(self.coords)]
            dungeon.go_to_new_location(game.zombie, self.coords, self.prev_coords)
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

    def prepare_sidestep(self):
        entity_row, entity_col = self.coords
        player_row, player_col = player.coords

        # Determine which axis is "primary"
        player_more_vertical = abs(player_row - entity_row) > abs(player_col - entity_col)

        if player_more_vertical:
            sidestep_dirs = horizontal_directions[:]  # try left/right first
            fallback_dirs = vertical_directions[:]  # then up/down
        else:
            sidestep_dirs = vertical_directions[:]  # try up/down first
            fallback_dirs = horizontal_directions[:]  # then left/right

        # Try sidestep directions first
        random.shuffle(sidestep_dirs)
        for temp_dir in sidestep_dirs:
            self.figure_out_potential_coords(temp_dir)

            row, col = self.potential_coords

            # bounds check
            if (row, col) not in dungeon.tiles_indexed_by_coords:
                continue

            tile_btn = dungeon.tiles_indexed_by_coords[(row, col)][get_btn]

            if not dungeon.tile_is_blocked(tile_btn, game.solid_objects):
                self.highlight_direction = temp_dir
                return

        # If sidestep fails, try fallback directions
        random.shuffle(fallback_dirs)
        for temp_dir in fallback_dirs:
            self.figure_out_potential_coords(temp_dir)

            row, col = self.potential_coords

            if (row, col) not in dungeon.tiles_indexed_by_coords:
                continue

            tile_btn = dungeon.tiles_indexed_by_coords[(row, col)][get_btn]

            if not dungeon.tile_is_blocked(tile_btn, game.solid_objects):
                self.highlight_direction = temp_dir
                return

        # If totally trapped, just don't change direction
        return

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
        if self.highlighted_coords == player.coords:
            print('enemy attack')
            self.damage = random.choice(self.damage_range)
            self.miss_chance = (player.speed / self.speed) * 10
            Combat(attacker=self, attacked=player)


class Combat:
    def __init__(self, attacker, attacked):

        rng = random.randint(1, 101)
        rng2 = random.randint(1, 101)
        rng3 = random.randint(1, 101)
        chosen_rng = random.choice([rng, rng2, rng3])
        if attacker.miss_chance >= chosen_rng:
            if isinstance(attacker, Enemy):
                game.update_log('missed attack', [attacker.enemy_type, 'you'])
            else:
                game.update_log('missed attack', ['You', attacked.enemy_type])
            return

        attacker_damage = attacker.damage
        if attacker.crit_chance >= chosen_rng:
            attacker_damage *= attacker.crit_multiplier
        attacked.hp -= attacker_damage
        print(attacker, attacked)
        if isinstance(attacker, Enemy):
            game.update_log('combat', [attacker.enemy_type, 'you', attacker_damage])
            game.update_player_stats(['hp'])
        else:
            game.update_log('combat', ['You', attacked.enemy_type, attacker_damage])

        if attacked.hp <= 0:
            attacked.kill_self()
            if isinstance(attacker, Enemy):
                game.update_log('killed entity', [attacker.enemy_type, 'you'])
            else:
                game.update_log('killed entity', ['You', attacked.enemy_type])


class Weapons:
    def __init__(self):
        self.damage_dictionary = {
            game.dagger: [2, 3, 4],
            game.shortsword: [2, 3, 4],
            # Index of game.whip dict is enemy distance
            game.whip: {
                1: [1, 2],
                2: [3, 4],
                3: [6, 7, 8],
            },
            None: 0,
        }

        self.damage_extremes = {
            game.dagger: [self.damage_dictionary[game.dagger][0], self.damage_dictionary[game.dagger][-1]],
            game.shortsword: [self.damage_dictionary[game.shortsword][0], self.damage_dictionary[game.shortsword][-1]],
            game.whip: [self.damage_dictionary[game.whip][0+1][0], self.damage_dictionary[game.whip][next(reversed(self.damage_dictionary[game.whip]))][-1]],
            None: [0, 0],
        }

    def adjust_stats(self, weapon):
        match weapon:
            case game.dagger:
                self.weapon_range = 1
                self.crit_chance = 80
                self.crit_multiplier = 1.5
                self.speed = player.normal_speed
            case game.shortsword:
                self.weapon_range = 2
                self.crit_chance = 60
                self.crit_multiplier = 2
                self.speed = player.normal_speed - 2
            case game.whip:
                self.weapon_range = 3
                self.crit_chance = 50
                self.crit_multiplier = 2.5
                self.speed = player.normal_speed - 2
            case _:
                self.weapon_range = 1
                self.crit_chance = 0
                self.crit_multiplier = 0
                self.speed = player.normal_speed
                player.miss_chance = 0

        return self.weapon_range, self.crit_chance, self.crit_multiplier, self.speed

    def calculate_its_damage(self, item, enemy_distance):
        # print(enemy_distance)
        if item in self.damage_dictionary:
            match item:
                case game.whip:
                    self.damage = random.choice(self.damage_dictionary[item][enemy_distance])
                case None:
                    self.damage = 0
                case _:
                    self.damage = random.choice(self.damage_dictionary[item])

        return self.damage


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
                if tile[get_btn]['text'] in game.opaque_objects:
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
        return None


game = GameController()
vision = Shadowcasting()
dungeon = Dungeon()
inv = Inventory()
player = Player()
weapons = Weapons()
dungeon.locate_important_objects_and_entities()
game.update_player_stats(['hp', 'damage', 'speed', 'crit chance', 'crit multiplier', 'miss chance'])
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