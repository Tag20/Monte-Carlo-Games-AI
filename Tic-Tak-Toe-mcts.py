from ursina import *
import random
import copy
import math

app = Ursina()

camera.orthographic = True
camera.fov = 4
camera.position = (1, 1)

player = Entity(name='O', color=color.azure)
cursor = Text(text='', color=player.color, origin=(0, 0), scale=4)
cursor.background = Entity(parent=camera.ui, model='quad', color=color.clear, scale=(2, 0.5))

bg = Entity(parent=scene, model='quad', texture='shore', scale=(16, 8), z=10, color=color.light_gray)
mouse.visible = True

board = [[None for x in range(3)] for y in range(3)]

# Initialize Board
for y in range(3):
    for x in range(3):
        b = Button(parent=scene, position=(x, y))
        board[x][y] = b

        def on_click(b=b):
            if player.name == 'O':  # Human player
                b.text = player.name
                b.color = player.color
                b.collision = False
                if check_for_victory():
                    return
                switch_turn()
                ai_move()

        b.on_click = on_click

def switch_turn():
    global player
    player.name = 'X' if player.name == 'O' else 'O'
    player.color = color.orange if player.name == 'X' else color.azure
    cursor.text = ''
    cursor.color = player.color

def check_for_victory():
    name = player.name
    won = (
        (board[0][0].text == name and board[1][0].text == name and board[2][0].text == name) or  # Bottom row
        (board[0][1].text == name and board[1][1].text == name and board[2][1].text == name) or  # Middle row
        (board[0][2].text == name and board[1][2].text == name and board[2][2].text == name) or  # Top row
        (board[0][0].text == name and board[0][1].text == name and board[0][2].text == name) or  # Left column
        (board[1][0].text == name and board[1][1].text == name and board[1][2].text == name) or  # Middle column
        (board[2][0].text == name and board[2][1].text == name and board[2][2].text == name) or  # Right column
        (board[0][0].text == name and board[1][1].text == name and board[2][2].text == name) or  # Diagonal /
        (board[0][2].text == name and board[1][1].text == name and board[2][0].text == name)  # Diagonal \
    )
    if won:
        print('Winner is:', name)
        destroy(cursor)
        mouse.visible = True
        Panel(z=1, scale=10, model='quad')
        t = Text(f'Player\n{name}\nwon!', scale=3, origin=(0, 0), background=True)
        t.create_background(padding=(.5, .25), radius=Text.size / 2)
        t.background.color = player.color.tint(-.2)
        return True
    return False

def get_available_moves():
    return [(x, y) for x in range(3) for y in range(3) if board[x][y].text == '']

def ai_move():
    if player.name == 'X':
        move = mcts_best_move()
        if move:
            x, y = move
            board[x][y].text = 'X'
            board[x][y].color = color.orange
            board[x][y].collision = False
            if not check_for_victory():
                switch_turn()

# Monte Carlo Tree Search
class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.wins = 0
        self.visits = 0
        self.children = []

    def best_child(self):
        return max(self.children, key=lambda child: child.wins / child.visits if child.visits > 0 else 0)

def simulate_game(board_state, player_symbol):
    available_moves = [(x, y) for x in range(3) for y in range(3) if board_state[x][y] == '']
    random.shuffle(available_moves)
    while available_moves:
        x, y = available_moves.pop()
        board_state[x][y] = player_symbol
        if check_winner(board_state, player_symbol):
            return 1 if player_symbol == 'X' else -1
        player_symbol = 'O' if player_symbol == 'X' else 'X'
    return 0

def check_winner(board_state, symbol):
    for row in range(3):
        if all(board_state[row][col] == symbol for col in range(3)):
            return True
    for col in range(3):
        if all(board_state[row][col] == symbol for row in range(3)):
            return True
    if all(board_state[i][i] == symbol for i in range(3)) or all(board_state[i][2 - i] == symbol for i in range(3)):
        return True
    return False

def mcts_best_move():
    root = Node([[board[x][y].text for y in range(3)] for x in range(3)])
    for _ in range(5000):
        node = root
        board_copy = copy.deepcopy(node.state)
        path = []
        while node.children:
            node = node.best_child()
            board_copy[node.move[0]][node.move[1]] = 'X'
            path.append(node)
        available_moves = get_available_moves()
        if available_moves:
            move = random.choice(available_moves)
            new_state = copy.deepcopy(board_copy)
            new_state[move[0]][move[1]] = 'X'
            child_node = Node(new_state, parent=node, move=move)
            node.children.append(child_node)
            path.append(child_node)
            result = simulate_game(new_state, 'O')
            for node in reversed(path):
                node.visits += 1
                node.wins += result
    return root.best_child().move

app.run()