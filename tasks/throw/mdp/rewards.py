from __future__ import annotations
from typing import TYPE_CHECKING
import torch
from isaaclab.managers import SceneEntityCfg
from isaaclab.assets import RigidObject




if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv



def landing_distance_reward(
    env: ManagerBasedRLEnv,
    std: float,
    gravity: float = 9.81,
    object_cfg: SceneEntityCfg = SceneEntityCfg("object"),
    target_cfg: SceneEntityCfg = SceneEntityCfg("target"),
) -> torch.Tensor:
    """
    ボールの現在位置・速度から放物運動を仮定して予測落下地点を計算し，
    その地点とターゲット位置との距離に応じた報酬を返す。
    """

    obj: RigidObject = env.scene[object_cfg.name]
    target: RigidObject = env.scene[target_cfg.name]

    obj_pos = obj.data.root_pos_w[:, :3]
    obj_vel = obj.data.root_lin_vel_w[:, :3]
    target_pos = target.data.root_pos_w[:, :3]

    obj_x = obj_pos[:, 0]
    obj_y = obj_pos[:, 1]
    obj_z = obj_pos[:, 2]

    obj_vx = obj_vel[:, 0]
    obj_vy = obj_vel[:, 1]
    obj_vz = obj_vel[:, 2]

    # 落下地点の予測
    discriminant = (obj_vz)**2 + 2 * gravity * obj_z
    discriminant = torch.clamp(discriminant, min=0.0)

    t = (obj_vz + torch.sqrt(discriminant)) / gravity
    t = torch.clamp(t, min=0.0)

    landing_x = obj_x + obj_vx * t
    landing_y = obj_y + obj_vy * t

    landing_xy = torch.stack([landing_x, landing_y], dim=1)
    target_xy = target_pos[:, :2]

    distance = torch.norm(landing_xy - target_xy, dim=1)

    return torch.exp(- (distance / std) ** 2)



def object_speed(
    env: ManagerBasedRLEnv,
    object_cfg: SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:
    """
    物体速度のノルムの二乗を返す。
    """

    obj: RigidObject = env.scene[object_cfg.name]
    obj_vel = obj.data.root_lin_vel_w[:, :3]
    speed = torch.norm(obj_vel, dim=1)
    return speed**2



def toward_target_reward(
    env: ManagerBasedRLEnv,
    object_cfg: SceneEntityCfg = SceneEntityCfg("object"),
    target_cfg: SceneEntityCfg = SceneEntityCfg("target"),
) -> torch.Tensor:
    """
    物体のxy方向速度ベクトルと、
    物体からターゲットへ向かうxy方向ベクトルとの
    コサイン類似度を返す。
    """

    obj: RigidObject = env.scene[object_cfg.name]
    target: RigidObject = env.scene[target_cfg.name]

    obj_pos = obj.data.root_pos_w[:, :2]
    target_pos = target.data.root_pos_w[:, :2]
    direction = target_pos - obj_pos

    vel_xy = obj.data.root_lin_vel_w[:, :2]

    vel_norm = torch.norm(vel_xy, dim=1)
    direction_norm = torch.norm(direction, dim=1)

    eps = 1e-6

    # コサイン類似度
    cosine_similarity = torch.sum(
        vel_xy * direction,
        dim=1,
    ) / (vel_norm * direction_norm + eps)

    return cosine_similarity