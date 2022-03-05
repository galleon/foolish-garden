from gym.envs.registration import register

register(
    id="MonPetitPotager-v0",
    entry_point="foolish_garden.mpp_env:MonPetitPotagerEnv",
    max_episode_steps=1000,
    kwargs={"targets": [0.2, 0.1, 0.1, 0.2, 0.05, 0.2, 0.15]},
)
