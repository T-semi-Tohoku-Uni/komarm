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
from robots import KOMARM_CFG  
from tasks.throw.throw_env_cfg import ThrowEnvCfg
# インポートを修正
from isaaclab.sim.schemas.schemas_cfg import RigidBodyPropertiesCfg, CollisionPropertiesCfg
from isaaclab.markers.config import FRAME_MARKER_CFG  # isort: skip
from isaaclab.sim import SphereCfg, MassPropertiesCfg, RigidBodyMaterialCfg



#ThrowEnvCfgで定義した環境を、具体化しているクラス
class KomarmThrowCubeEnvCfg(ThrowEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # Set komarm as robot
        self.scene.robot = KOMARM_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")

        # override actions
        self.actions.arm_action = mdp.JointPositionActionCfg(
            asset_name="robot",
            joint_names=["Revolute_1", "Revolute_2", "Revolute_3", "Revolute_4", "Revolute_5"],
            scale=0.5,
            use_default_offset=True,
        )
        self.actions.gripper_action = mdp.BinaryJointPositionActionCfg(
            asset_name="robot",
            joint_names=["Revolute_6"],
            open_command_expr={"Revolute_6": -0.4},  
            close_command_expr={"Revolute_6": 0.4},
        )
        # Set the body name for the end effector
        self.commands.object_pose.body_name = ["hand_unit_v3_1"]

        # Set Cube as object
        self.scene.object = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Object",
            #あとで計算する
            init_state=RigidObjectCfg.InitialStateCfg(
                pos=[0.2, 0.0, 0.0300],
                rot=[1, 0, 0, 0],
            ),
            spawn=SphereCfg(
                radius=0.0300,
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

        # Set big Cube as target box
        self.scene.target = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Target",
            #あとで計算する
            init_state=RigidObjectCfg.InitialStateCfg(pos=[0.4, 0.4, 0.015], rot=[1, 0, 0, 0]),
            spawn=UsdFileCfg(
                usd_path=f"{ISAAC_NUCLEUS_DIR}/Props/Blocks/DexCube/dex_cube_instanceable.usd",
                scale=(2, 2, 1),   #6cm * 2 = 12cmの正方形の板にする
                # rigid_props=RigidBodyPropertiesCfg(
                #     solver_position_iteration_count=16,
                #     solver_velocity_iteration_count=1,
                #     max_angular_velocity=1000.0,
                #     max_linear_velocity=1000.0,
                #     max_depenetration_velocity=5.0,
                #     disable_gravity=False,
                # ),
                # collision_props=CollisionPropertiesCfg(),
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
                        pos=[0.09, 0.00, 0.00],
                    ),
                ),
            ],
        )

@configclass
class KomarmThrowCubeEnvCfg_PLAY(KomarmThrowCubeEnvCfg):
    def __post_init__(self):
        super().__post_init__()

        # make a smaller scene for play
        self.scene.num_envs = 1
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False
