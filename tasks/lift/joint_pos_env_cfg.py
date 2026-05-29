# Copyright (c) 2024-2025, Muammer Bay (LycheeAI), Louis Le Lay
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import isaaclab_tasks.manager_based.manipulation.lift.mdp as mdp
from isaaclab.assets import RigidObjectCfg

# from isaaclab.managers NotImplementedError
from isaaclab.sensors.frame_transformer.frame_transformer_cfg import (
    FrameTransformerCfg,
    OffsetCfg,
)
from isaaclab.sim.schemas.schemas_cfg import RigidBodyPropertiesCfg
from isaaclab.sim.spawners.from_files.from_files_cfg import UsdFileCfg
from isaaclab.utils import configclass
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR
from robots import SO_ARM100_CFG, SO_ARM101_CFG, KOMARM_CFG  # noqa: F401
from tasks.lift.lift_env_cfg import LiftEnvCfg
# インポートを修正
from isaaclab.sim.schemas.schemas_cfg import RigidBodyPropertiesCfg, CollisionPropertiesCfg
from isaaclab.markers.config import FRAME_MARKER_CFG  # isort: skip
from isaaclab.sim import SphereCfg, MassPropertiesCfg, RigidBodyMaterialCfg


"lift_env_cfg.pyで定義された抽象的な学習環境を、SO Arm 100/101とキューブで具体化した環境定義"


@configclass
class SoArm100LiftCubeEnvCfg(LiftEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # Set so arm as robot
        self.scene.robot = SO_ARM100_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")  #robotをSO Arm 100のアセットに置き換える

        # override actions
        self.actions.arm_action = mdp.JointPositionActionCfg(
            asset_name="robot",
            joint_names=["shoulder_.*", "elbow_flex", "wrist_.*"],
            scale=0.5,                                       #学習を安定させ、急激動作防止                                                               
            use_default_offset=True,
        )
        self.actions.gripper_action = mdp.BinaryJointPositionActionCfg(
            asset_name="robot",
            joint_names=["gripper"],
            open_command_expr={"gripper": 0.5},              #グリッパーを開くコマンドの表現
            close_command_expr={"gripper": 0.0},             #グリッパーを閉じるコマンドの表現
        )
        # Set the body name for the end effector
        self.commands.object_pose.body_name = ["gripper"]    #目標位置（エンドイフェクタ）をグリッパーの位置に設定

        # Set Cube as object
        self.scene.object = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Object",
            init_state=RigidObjectCfg.InitialStateCfg(
                pos=[0.2, 0.0, 0.0200],
                rot=[1, 0, 0, 0],
            ),
            spawn=SphereCfg(
                radius=0.0200,
                rigid_props=RigidBodyPropertiesCfg(
                    solver_position_iteration_count=32,
                    solver_velocity_iteration_count=8,

                    # 自転しにくくする
                    max_angular_velocity=0.05,
                    angular_damping=50.0,

                    # 掴んだ後に暴れにくくする
                    max_linear_velocity=1000.0,
                    linear_damping=0.5,

                    max_depenetration_velocity=3.0,
                    disable_gravity=False,
                ),
                mass_props=MassPropertiesCfg(
                    mass=0.03,
                ),
                collision_props=CollisionPropertiesCfg(),
                physics_material=RigidBodyMaterialCfg(
                    # 掴み始めで接触が成立しやすい
                    static_friction=8.0,

                    # 掴んだ後に滑りにくい
                    dynamic_friction=8.0,

                    restitution=0.0,

                    # ロボット指側と球側のうち、高い摩擦を優先
                    friction_combine_mode="max",
                    restitution_combine_mode="min",
                ),
            ),
        )

        # Listens to the required transforms
        marker_cfg = FRAME_MARKER_CFG.copy()
        marker_cfg.markers["frame"].scale = (0.05, 0.05, 0.05)
        marker_cfg.prim_path = "/Visuals/FrameTransformer"
        self.scene.ee_frame = FrameTransformerCfg(
            prim_path="{ENV_REGEX_NS}/Robot/base",
            debug_vis=True,
            visualizer_cfg=marker_cfg,
            target_frames=[
                FrameTransformerCfg.FrameCfg(
                    prim_path="{ENV_REGEX_NS}/Robot/gripper",
                    name="end_effector",
                    offset=OffsetCfg(
                        pos=[0.0, -0.08, 0.01],              #エンドイフェクタの位置から指先の位置に補正
                    ),
                ),
            ],
        )


@configclass
class SoArm100LiftCubeEnvCfg_PLAY(SoArm100LiftCubeEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False


@configclass
class SoArm101LiftCubeEnvCfg(LiftEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # Set so arm as robot
        self.scene.robot = SO_ARM101_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")

        # override actions
        self.actions.arm_action = mdp.JointPositionActionCfg(
            asset_name="robot",
            joint_names=["shoulder_.*", "elbow_flex", "wrist_.*"],
            scale=0.5,
            use_default_offset=True,
        )
        self.actions.gripper_action = mdp.BinaryJointPositionActionCfg(
            asset_name="robot",
            joint_names=["gripper"],
            open_command_expr={"gripper": 0.5},
            close_command_expr={"gripper": 0.0},
        )
        # Set the body name for the end effector
        self.commands.object_pose.body_name = ["gripper_link"]

        # Set Cube as object
        self.scene.object = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Object",
            init_state=RigidObjectCfg.InitialStateCfg(pos=[0.2, 0.0, 0.015], rot=[1, 0, 0, 0]),
            spawn=UsdFileCfg(
                usd_path=f"{ISAAC_NUCLEUS_DIR}/Props/Blocks/DexCube/dex_cube_instanceable.usd",
                scale=(0.5, 0.5, 0.5),
                rigid_props=RigidBodyPropertiesCfg(
                    solver_position_iteration_count=16,
                    solver_velocity_iteration_count=1,
                    max_angular_velocity=1000.0,
                    max_linear_velocity=1000.0,
                    max_depenetration_velocity=5.0,
                    disable_gravity=False,
                ),
                collision_props=CollisionPropertiesCfg(),
            ),
        )

        # Listens to the required transforms
        marker_cfg = FRAME_MARKER_CFG.copy()
        marker_cfg.markers["frame"].scale = (0.05, 0.05, 0.05)
        marker_cfg.prim_path = "/Visuals/FrameTransformer"
        self.scene.ee_frame = FrameTransformerCfg(
            prim_path="{ENV_REGEX_NS}/Robot/base_link",
            debug_vis=True,
            visualizer_cfg=marker_cfg,
            target_frames=[
                FrameTransformerCfg.FrameCfg(
                    prim_path="{ENV_REGEX_NS}/Robot/gripper_link",
                    name="end_effector",
                    offset=OffsetCfg(
                        pos=[0.01, 0.0, -0.09],
                    ),
                ),
            ],
        )


@configclass
class SoArm101LiftCubeEnvCfg_PLAY(SoArm101LiftCubeEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False

@configclass
class KomarmLiftCubeEnvCfg(LiftEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # Set so arm as robot
        self.scene.robot = KOMARM_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")

        # override actions
        self.actions.arm_action = mdp.JointPositionActionCfg(
            asset_name="robot",
            joint_names=[".*"],
            scale=0.5,
            use_default_offset=True,
        )
        self.actions.gripper_action = mdp.BinaryJointPositionActionCfg(
            asset_name="robot",
            joint_names=["Revolute_6"],
            open_command_expr={"Revolute_6": -1.57},  
            close_command_expr={"Revolute_6": 0.8},
        )
        # Set the body name for the end effector
        self.commands.object_pose.body_name = ["hand_unit_v3_1"]

        # Set Cube as object
        self.scene.object = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Object",
            init_state=RigidObjectCfg.InitialStateCfg(
                pos=[0.2, 0.0, 0.0350],
                rot=[1, 0, 0, 0],
            ),
            spawn=SphereCfg(
                radius=0.0350,
                rigid_props=RigidBodyPropertiesCfg(
                    solver_position_iteration_count=32,
                    solver_velocity_iteration_count=8,

                    # 自転しにくくする
                    max_angular_velocity=0.05,
                    angular_damping=50.0,

                    # 掴んだ後に暴れにくくする
                    max_linear_velocity=1000.0,
                    linear_damping=0.5,

                    max_depenetration_velocity=3.0,
                    disable_gravity=False,
                ),
                mass_props=MassPropertiesCfg(
                    mass=0.03,
                ),
                collision_props=CollisionPropertiesCfg(),
                physics_material=RigidBodyMaterialCfg(
                    # 掴み始めで接触が成立しやすい
                    static_friction=8.0,

                    # 掴んだ後に滑りにくい
                    dynamic_friction=8.0,

                    restitution=0.0,

                    # ロボット指側と球側のうち、高い摩擦を優先
                    friction_combine_mode="max",
                    restitution_combine_mode="min",
                ),
            ),
        )

        # Listens to the required transforms
        marker_cfg = FRAME_MARKER_CFG.copy()
        marker_cfg.markers["frame"].scale = (0.05, 0.05, 0.05)
        marker_cfg.prim_path = "/Visuals/FrameTransformer"
        self.scene.ee_frame = FrameTransformerCfg(
            prim_path="{ENV_REGEX_NS}/Robot/base_link",
            debug_vis=True,
            visualizer_cfg=marker_cfg,
            target_frames=[
                FrameTransformerCfg.FrameCfg(
                    prim_path="{ENV_REGEX_NS}/Robot/hand_unit_v3_1",
                    name="end_effector",
                    offset=OffsetCfg(
                        pos=[0.090, 0.00, 0.00],
                    ),
                ),
            ],
        )


@configclass
class KomarmLiftCubeEnvCfg_PLAY(KomarmLiftCubeEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False  #あとでtrueにする