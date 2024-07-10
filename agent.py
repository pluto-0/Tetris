import torch
import random
import numpy as np
from logic import Board, possible_moves, make_random_piece, get_metrics
from collections import deque
from model import Model, Trainer

MAX_MEM = 100000
BATCH_SIZE = 5000
LR = .001


class Agent:
    def __init__(self, board):
        self.board = board
        self.games = 0
        self.epsilon = 0
        self.gamma = .9
        self.memory = deque(maxlen=MAX_MEM)
        self.model = Model(13, 256, 128, 1)
        self.trainer = Trainer(self.model, lr=LR, gamma=self.gamma)
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        #states, actions, rewards, next_states, dones = zip(*mini_sample)
        for entry in mini_sample:
            state, action, reward, next_state, done = entry
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_move(self, possible):
        self.epsilon = 80 - self.games
        if random.randint(0, 200) < self.epsilon:
            return random.choice(list(possible.keys()))
        best_output = float('-inf')
        for move in possible:
            board = possible[move]
            metrics = get_metrics(board.state)
            metrics.append(board.score - self.board.score)
            input_tensor = torch.tensor(metrics, dtype=torch.float)
            pred = self.model(input_tensor)
            if pred > best_output:
                best_output = pred
                best_move = move
        return move
            
        '''
        state0 = torch.tensor(np.array(get_metrics(self.board.state)), dtype=torch.float)
        prediction = self.model(state0)
        move = torch.argmax(prediction).item()
        return list(possible.keys())[move]
        '''
    
    def train(self, piece):
        old_state = get_metrics(self.board.state)
        old_score = self.board.score

        move_options = possible_moves(piece, self.board)
        move = self.get_move(move_options)
        done = not self.board.update()

        new_score = self.board.score
        new_state = get_metrics(self.board.state)
        old_state.append(new_score - old_score)
        new_state.append(new_score - old_score)
        reward = get_reward(move_options[move].state, old_score, new_score)
        self.remember(old_state, move, reward, new_state, done)
        self.train_short_memory(old_state, move, reward, new_state, done)
        if done:
            self.train_long_memory()
        return move

def get_reward(board_state, old_score, new_score):
    metrics = get_metrics(board_state)
    return -metrics[0] - metrics[1] - metrics[2] + 10 * (new_score - old_score)

''' 
def translate_state(state):
    ans = []
    for row in state:
        col = []
        for thing in row:
            if thing is None:
                col.append(0)
            else:
                col.append(thing)
        ans.append(col)
    return ans
'''