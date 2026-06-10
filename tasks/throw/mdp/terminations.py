from __future__ import annotations
import torch
from typing import TYPE_CHECKING
from isaaclab.assets import RigidObject
from isaaclab.managers import SceneEntityCfg


if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv

def object_in_target(
    env: ManagerBasedRLEnv,
    threshold: float = 0.05,
    robot_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
    object_cfg: SceneEntityCfg = SceneEntityCfg("object"),
    target_cfg: SceneEntityCfg = SceneEntityCfg("target"),
) -> torch.Tensor:

    object: RigidObject = env.scene[object_cfg.name]
    target: RigidObject = env.scene[target_cfg.name]

    distance = torch.norm(
        object.data.root_pos_w[:, :3]
        - target.data.root_pos_w[:, :3],
        dim=1,
    )

    return distance < threshold