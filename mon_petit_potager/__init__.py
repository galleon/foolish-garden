from gym.envs.registration import register

register(
    id="MonPetitPotager-v0",
    entry_point="envs.mon_petit_potager_env:AcasEnv",
    max_episode_steps=1000,
    kwargs={"size": (600, 600)},
)
