import torch
from typing import TYPE_CHECKING
from isaaclab.managers import SceneEntityCfg
from isaaclab.assets import RigidObject
from isaaclab.utils.math import subtract_frame_transforms


if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv

def object_position_in_robot_root_frame(
        env:ManagerBasedRLEnv,
        robot_cfg:SceneEntityCfg = SceneEntityCfg("robot"),
        object_cfg:SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:    #戻り値の型がtorch.Tensor
    robot: RigidObject = env.scene[robot_cfg.name]
    object: RigidObject = env.scene[object_cfg.name]
    object_pos_w = object.data.root_pos_w[:, :3]
    # 物体の位置をワールド座標系からロボットのroot座標系へ変換している
    object_pos_b, _ = subtract_frame_transforms(
        robot.data.root_state_w[:, :3], robot.data.root_state_w[:, 3:7], object_pos_w
    )
    return object_pos_b