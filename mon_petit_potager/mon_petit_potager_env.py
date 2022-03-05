from typing import List

import matplotlib.pyplot as plt
import numpy as np
from gym import Env, spaces

VEGGIES = {
    0: "Tomato",
    1: "Green bean",
    2: "Cucumber",
    3: "Potato",
    4: "Beet",
    5: "Carrot",
    6: "Cabbage",
}

HATE_LOVE_MATRIX = [
    [+1, -1, -1, -1, -1, +1, -1],
    [-1, +1, +1, +1, +1, +1, +1],
    [-1, +1, +1, -1, 0, 0, 0],
    [-1, +1, -1, +1, 0, -1, +1],
    [-1, +1, 0, 0, +1, -1, 0],
    [+1, +1, 0, -1, -1, +1, 0],
    [-1, +1, 0, +1, 0, 0, +1],
]


class MonPetitPotagerEnv(Env):
    def __init__(self, targets: List[int]):
        super(MonPetitPotagerEnv, self).__init__()

        self.n_x, self.n_y = 100, 100
        self.n_veggies = len(VEGGIES)

        assert self.n_veggies > 1

        # Define a dict observation space with all variables normalized between [-1, 1]
        self.observation_space = spaces.Dict(
            {
                "image": spaces.Box(
                    low=-1.0,
                    high=1.0,
                    shape=(
                        self.n_x,
                        self.n_y,
                    ),
                    dtype=np.float32,
                ),
                "perfo": spaces.Box(
                    low=-1.0,
                    high=1.0,
                    shape=(self.n_veggies,),
                    dtype=np.float32,
                ),
            }
        )

        # Define an action space ranging from 0 to 4
        self.action_space = spaces.Discrete(
            self.n_x * self.n_y * self.n_veggies,
        )

        print(self.observation_space["image"].shape)

        self.one = np.ones(self.observation_space["image"].shape)

        # Create a canvas to render the environment images upon
        self.garden = None
        self.scores = None

        self.targets = targets

    def reset(self):
        print(self.observation_space["image"].shape)

        # Reset the Canvas
        self.garden = np.random.randint(
            self.n_veggies, size=self.observation_space["image"].shape
        )

        # print(f"Garden initialized: {self.garden}")

        self.count_veggies = np.bincount(np.reshape(self.garden, -1))
        self.total_veggies = np.sum(self.count_veggies)

        # print(f"We are having {self.total_veggies} VEGGIES: {self.count_veggies}")

        # Reset the reward
        self.ep_return = 0

        obs = {
            "image": 2 * self.garden / (self.n_veggies - 1) - self.one,
            "perfo": self.targets - self.count_veggies / self.total_veggies,
        }

        happyness_level = 0
        for i in range(self.n_x):
            for j in range(self.n_y):
                neighbours = []
                if i > 0:
                    neighbours.append((i - 1, j))
                if i < self.n_x - 1:
                    neighbours.append((i + 1, j))
                if j > 0:
                    neighbours.append((i, j - 1))
                if j < self.n_y - 1:
                    neighbours.append((i, j + 1))
                for k, l in neighbours:
                    happyness_level += HATE_LOVE_MATRIX[self.garden[i, j]][
                        self.garden[k, l]
                    ]

        print(f"Happyness level: {happyness_level}")

        # return the observation
        return obs

    def render(self, mode="human"):
        assert mode in [
            "human",
            "rgb_array",
        ], 'Invalid mode, must be either "human" or "rgb_array"'

        if mode == "human":
            plt.clf()
            plt.tick_params(
                left=False,
                right=False,
                labelleft=False,
                labelbottom=False,
                bottom=False,
            )
            plt.imshow(self.garden)
            plt.pause(0.05)
            plt.draw()
        elif mode == "rgb_array":
            return self.garden

    def close(self):
        plt.close()

    def step(self, action):
        # Flag that marks the termination of an episode
        done = False

        # Assert that it is a valid action
        assert self.action_space.contains(action), "Invalid Action"

        surface = self.n_x * self.n_y

        # Action decoding
        new_veggie = action // surface
        ij = action % surface

        i = ij // self.n_x
        j = ij % self.n_x

        # print(f"Planting {VEGGIES[new_veggie]} at {i}, {j}")

        old_veggie = self.garden[i, j]

        delta_happyness_level = 0
        neighbours = []
        if i > 0:
            neighbours.append((i - 1, j))
        if i < self.n_x - 1:
            neighbours.append((i + 1, j))
        if j > 0:
            neighbours.append((i, j - 1))
        if j < self.n_y - 1:
            neighbours.append((i, j + 1))
        for k, l in neighbours:
            delta_happyness_level += (
                HATE_LOVE_MATRIX[new_veggie][self.garden[k, l]]
                - HATE_LOVE_MATRIX[old_veggie][self.garden[k, l]]
            )

        self.garden[i, j] = new_veggie

        self.count_veggies[new_veggie] += 1
        self.count_veggies[old_veggie] -= 1

        # print(f"Delta happyness level: {delta_happyness_level}")

        # Reward for executing a step.
        reward = delta_happyness_level - np.sum(
            np.abs(self.targets - self.count_veggies / self.total_veggies)
        )

        obs = {
            "image": 2 * self.garden / (self.n_veggies - 1) - self.one,
            "perfo": self.targets - self.count_veggies / self.total_veggies,
        }

        return obs, reward, done, {}
