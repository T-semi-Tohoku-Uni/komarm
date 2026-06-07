import gymnasium as gym
from . import agents

gym.register(
    id="Isaac-KOMARM-Throw-Cube-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": f"{__name__}.joint_pos_env_cfg:KomarmThrowCubeEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:ThrowCubePPORunnerCfg",
    },
    disable_env_checker=True,
)

gym.register(
    id="Isaac-KOMARM-Throw-Cube-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": f"{__name__}.joint_pos_env_cfg:KomarmThrowCubeEnvCfg_PLAY",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:ThrowCubePPORunnerCfg",
    },
    disable_env_checker=True,
)