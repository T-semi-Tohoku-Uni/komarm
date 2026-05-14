import gymnasium as gym

gym.register(
    id="komarm-Reach-v0",

    entry_point="komarm.komarm_task.komarm_env:KomarmReachEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point" : "komarm.komarm_task.komarm_env:KomarmReachEnvCfg",
        "skrl_cfg_entry_point" : "komarm.komarm_task.ppo_config.yaml",
    }
)