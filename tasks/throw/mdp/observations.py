from __future__ import annotations
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


def target_position_in_robot_root_frame(
    env: ManagerBasedRLEnv,
    robot_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
    target_cfg: SceneEntityCfg = SceneEntityCfg("target"),
) -> torch.Tensor:
    
    robot: RigidObject = env.scene[robot_cfg.name]
    target: RigidObject = env.scene[target_cfg.name]

    target_pos_w = target.data.root_pos_w[:, :3]
    target_pos_b, _ = subtract_frame_transforms(
        robot.data.root_state_w[:, :3], robot.data.root_state_w[:, 3:7], target_pos_w
    )
    return target_pos_b


def ee_position_in_robot_root_frame(
    env: ManagerBasedRLEnv,
    robot_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
    ee_cfg: SceneEntityCfg = SceneEntityCfg(
        "robot",
        body_names=["end_effector"],  
    ),
) -> torch.Tensor:
    """
    エンドエフェクタの位置をロボットroot座標系で返す。
    """

    robot: RigidObject = env.scene[robot_cfg.name]
    asset: RigidObject = env.scene[ee_cfg.name]

    ee_pos_w = asset.data.body_pos_w[:, ee_cfg.body_ids[0]]

    ee_pos_b, _ = subtract_frame_transforms(
        robot.data.root_state_w[:, :3],
        robot.data.root_state_w[:, 3:7],
        ee_pos_w,
    )

    return ee_pos_b



def ee_velocity_in_robot_root_frame(
    env: ManagerBasedRLEnv,
    robot_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
    ee_cfg: SceneEntityCfg = SceneEntityCfg(
        "robot",
        body_names=["end_effector"], 
    ),
) -> torch.Tensor:
    """
    エンドエフェクタの線速度をロボットroot座標系で返す。
    """

    robot: RigidObject = env.scene[robot_cfg.name]
    asset: RigidObject = env.scene[ee_cfg.name]

    ee_vel_w = asset.data.body_lin_vel_w[:, ee_cfg.body_ids[0]]

    # rootの並進速度を引く
    ee_vel_b = ee_vel_w - robot.data.root_lin_vel_w

    return ee_vel_b