import argparse
import gym

from stable_baselines3.common.callbacks import EvalCallback

from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import PPO

from stable_baselines3.common.env_checker import check_env


from stable_baselines3.common.vec_env.util import (
    copy_obs_dict,
    dict_to_obs,
    obs_space_info,
)

import mon_petit_potager


parser = argparse.ArgumentParser(description="Script to train PPO agent")

parser.add_argument(
    "--step_train",
    type=int,
    default=1_000_000,
    help="average reward to be reached to increase random. Defaut 0 means no steptrain",
)

parser.add_argument(
    "--model_path",
    type=str,
    default="trained_models/ppo2_mpp",
    help="path to save the trained agent",
)

parser.add_argument(
    "--model_load", type=str, default="", help="path to load a trained model"
)
args = vars(parser.parse_args())

env = DummyVecEnv([lambda: gym.make("MonPetitPotager-v0") for i in range(1)])

eval_env = gym.make("MonPetitPotager-v0")
obs_space = eval_env.observation_space
keys, shapes, dtypes = obs_space_info(obs_space)
print(keys, shapes, dtypes)

# It will check your custom environment and output additional warnings if needed
check_env(eval_env)

print(obs_space, eval_env.reset())


eval_callback = EvalCallback(
    eval_env,
    best_model_save_path=args["model_path"],
    log_path="./logs/",
    eval_freq=10000,
    deterministic=True,
    render=False,
)

if args["model_load"] != "":
    model = PPO.load(args["model_load"])
else:
    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="./tensorboard_logs/")

model.learn(total_timesteps=args["step_train"], callback=eval_callback)
