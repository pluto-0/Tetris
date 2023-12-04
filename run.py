from dqn_agent import DQNAgent
import tetris
from tetris import Piece, Board, make_random_piece, possible_states, drop_down, find_full_rows
from datetime import datetime
from statistics import mean, median
import random
from logs import CustomTensorBoard
from tqdm import tqdm
import extra
from extra import game, clock

def dqn():
    env = Board()
    episodes = 200
    max_steps = 50000
    epsilon_stop_episode = 1500
    mem_size = 20000
    discount = 0.95
    batch_size = 512
    epochs = 1
    render_every = 50
    log_every = 50
    replay_start_size = 2000
    train_every = 1
    n_neurons = [32, 32]
    render_delay = None
    activations = ['relu', 'relu', 'linear']

    agent = DQNAgent(env.get_state_size(),
                     n_neurons=n_neurons, activations=activations,
                     epsilon_stop_episode=epsilon_stop_episode, mem_size=mem_size,
                     discount=discount, replay_start_size=replay_start_size)

    log_dir = f'logs/tetris-nn={"-".join(map(str, n_neurons))}-mem={mem_size}-bs={batch_size}-e={epochs}-{datetime.now().strftime("%Y%m%d-%H%M%S")}'
    log = CustomTensorBoard(log_dir=log_dir)

    scores = []
    score_increases = {0:0, 1: 800, 2: 1200, 3: 1800, 4: 2000}

    for episode in tqdm(range(episodes), desc="Training Episodes"):
        current_state = env.reset()
        piece = make_random_piece(env)
        next_piece = make_random_piece(env)
        print(f'Initial State: {current_state}')
        done = False
        steps = 0
        render = render_every and episode % render_every == 0

        while not done and (not max_steps or steps < max_steps):
            next_states = possible_states(piece,env)
            best_state = agent.best_state(next_states.values())
            best_action = next((action for action, state in next_states.items() if state == best_state), None)
            print("best state is:  ", best_state)
            print("best action is:  ",best_action)
            if best_action is not None:
                # print(best_state)
                # print(best_action)
                print(best_state[0])
                if best_state[0]>0:
                    clock()
                reward, done = score_increases[best_state[0]], not finish(env)[0]
                print(reward,done)
                agent.add_to_memory(current_state, next_states[best_action], reward, done)
                current_state = next_states[best_action]
                piece, next_piece, env =game(piece,next_piece,env,best_action)
                steps += 1

        scores.append(env.score)

        if episode % train_every == 0:
            agent.train(batch_size=batch_size, epochs=epochs)

        if log_every and episode and episode % log_every == 0:
            avg_score = mean(scores[-log_every:])
            min_score = min(scores[-log_every:])
            max_score = max(scores[-log_every:])
            log.log(episode, avg_score=avg_score, min_score=min_score, max_score=max_score)

if __name__ == "__main__":
    dqn()
