import gym
from gym.spaces import Discrete
from gym.utils import seeding

class GuessTheNumber(gym.Env):
    """
    Description:
        The agent is required to guess a randomly picked number, the only feedback received is if the selected number higher than the target number.
    Observation: 
        Type: Discrete(1)
        Num	Observation                 
        0   Last guess too low
        1   Last guess too high
                
    Actions:
        Type: Discrete(100)
        Num	Action
        n	Predict the value n
        
    Reward:
        Reward is 1 when you guess the correct number 
                 -1 for every incorrect guess
                 -10 if it takes more than 100 guesses
    Starting State:
        Value is set to "0" - "last guess too low" as a default
    Episode Termination:
        The agent is allowed up to 100 guesses (they may submit at most 100 guesses) before the episode terminates.
        agent correctly guesses the number
    """

    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.MAX_SIZE = 100
        self.MAX_EPISODE_STEPS = 100

        self.CORRECT_REWARD = 1
        self.INCORRECT_PUNISHMENT = 1
        self.TIMEOUT_PUNISHMENT = 10

        self.action_space = Discrete(self.MAX_SIZE) # (0, 99]
        self.observation_space = Discrete(2) # (0, 1]
        self.targetNumber = None
        self.episode_steps = 0
        self.seed()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action), f'{action} ({type(action)}) invalid'
        done = False
        
        if action == self.targetNumber:
            done = True
            reward = self.CORRECT_REWARD
            observation = 1
        elif action > self.targetNumber:
            reward = -self.INCORRECT_PUNISHMENT
            observation = 1
        elif action < self.targetNumber:
            reward = -self.INCORRECT_PUNISHMENT
            observation = 1

        if self.episode_steps >= self.MAX_EPISODE_STEPS:
            # Gone over
            done = True
            reward = -self.TIMEOUT_PUNISHMENT

        self.episode_steps += 1

        return observation, reward, done, {}

    def reset(self):
        self.episode_steps = 0
        self.targetNumber = self.np_random.randint(low=0, high=self.MAX_SIZE)
        return 0