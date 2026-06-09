from isaaclab.utils import configclass
from dataclasses import MISSING
from isaaclab.assets import (
    ArticulationCfg,
    DeformableObjectCfg,
    RigidObjectCfg,
    AssetBaseCfg,
)
from isaaclab.envs import ManagerBasedRLEnvCfg
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.sensors.frame_transformer.frame_transformer_cfg import FrameTransformerCfg
from isaaclab.sim.spawners.from_files.from_files_cfg import GroundPlaneCfg, UsdFileCfg
from isaaclab.managers import ObservationGroupCfg as ObsGroup
from isaaclab.managers import SceneEntityCfg
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import CurriculumTermCfg as CurrTerm
from isaaclab.managers import TerminationTermCfg as DoneTerm
from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.managers import RewardTermCfg as RewTerm
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR
import isaaclab.sim as sim_utils
import tasks.throw.mdp as mdp

"抽象的な学習環境の定義（テンプレート）"

#Sceneの定義
@configclass
class ObjectBoxSceneCfg(InteractiveSceneCfg):

    robot: ArticulationCfg = MISSING
    ee_frame: FrameTransformerCfg = MISSING
    object: RigidObjectCfg | DeformableObjectCfg = MISSING
    #あとでboxを作る or 領域
    # target: RigidObjectCfg = MISSING

    plane = AssetBaseCfg(
        prim_path="/World/GroundPlane",
        init_state=AssetBaseCfg.InitialStateCfg(pos=[0, 0, -1.05]),
        spawn=GroundPlaneCfg(),
    )

    table = AssetBaseCfg(
        prim_path="{ENV_REGEX_NS}/Table",
        init_state=AssetBaseCfg.InitialStateCfg(pos=[0.5, 0, 0], rot=[0.707, 0, 0, 0.707]),
        spawn=UsdFileCfg(usd_path=f"{ISAAC_NUCLEUS_DIR}/Props/Mounts/SeattleLabTable/table_instanceable.usd"),
    )

    #あとでboxを作る or 領域
    box = AssetBaseCfg(

    )

    light = AssetBaseCfg(
        prim_path="/World/light",
        spawn=sim_utils.DomeLightCfg(color=(0.75, 0.75, 0.75), intensity=3000.0),
    )


@configclass
class CommandsCfg:

    object_pose = mdp.UniformPoseCommandCfg(
        asset_name="robot",
        body_name=MISSING,
        resampling_time_range=(5.0, 5.0),
        debug_vis=True,
        #objectの位置を指定する
        ranges=mdp.UniformPoseCommandCfg.Ranges(
            pos_x=(0.20, 0.20),
            pos_y=(-0.20, 0.20),
            pos_z=(0.10, 0.10),
            roll=(0.0, 0.0),
            pitch=(0.0, 0.0),
            yaw=(0.0, 0.0),
        ),
    )

#Actionの定義
@configclass
class ActionsCfg:
    
    arm_actions: mdp.JointPositionActionCfg | mdp.DifferentialInverseKinematicsActionCfg = MISSING
    gripper_action: mdp.BinaryJointPositionActionCfg = MISSING


@configclass
class ObservationsCfg:
    
    @configclass
    class PolicyCfg(ObsGroup):
        #あとでobsを定義 それをPolicyCfgに入れる
        joint_pos = ObsTerm(func=mdp.joint_pos_rel)
        joint_vel = ObsTerm(func=mdp.joint_vel_rel)
        ee_pos = ObsTerm(func=mdp.ee_position_in_robot_root_frame)
        ee_vel = ObsTerm(func=mdp.ee_velocity_in_robot_root_frame)
        target_pos = ObsTerm(func=mdp.target_position_in_robot_root_frame)
        actions = ObsTerm(func=mdp.last_action)

    policy = PolicyCfg()


@configclass
class EventCfg:

    #resetの時にシーンを初期状態にリセットするイベント
    reset_all = EventTerm(
        func=mdp.reset_scene_to_default, 
        mode="reset"
    )

    #resetの時にobjectの位置をランダムにリセットするイベント
    reset_object_position = EventTerm(
        func=mdp.reset_root_state_uniform,
        mode="reset",
        #ここをあとで考える
        params={
            "pose_range": {"x": (0.10, 0.10), "y": (0.0, 0.0), "z": (0.0, 0.0)},  #cubeの初期位置を定義
            "velocity_range": {},
            "asset_cfg": SceneEntityCfg("object", body_names="Object"),
        },
    )

    #resetの時にactuator gainsをランダムにリセットするイベント
    randomize_actuator_gains = EventTerm(
        func=mdp.randomize_actuator_gains,
        mode="reset",
        params={
            "asset_cfg": SceneEntityCfg("robot"),

            "stiffness_distribution_params": (0.1, 10),  #komarm.pyにあるstiffnessの値に対して、0.8倍から1.2倍の範囲でランダムに変化させる
            "damping_distribution_params": (0.1, 10),    #komarm.pyにあるdampingの値に対して、0.8倍から1.2倍の範囲でランダムに変化させる
            "operation": "scale",                         #stiffnessとdampingの両方に同じ倍率をかける
            "distribution": "uniform",                    #一様分布 
        },
    )


@configclass
class RewardsCfg:

    landing_reward = RewTerm(
        func=mdp.landing_distance_reward,
        params={"std": 0.1},
        weight=1.0,
    )

    obj_speed_reward = RewTerm(
        func=mdp.object_speed,
        weight=0.1,
    )

    toward_target_reward = RewTerm(
        func=mdp.toward_target_reward,
        weight=0.5,
    )

    # release_obj_reward ,object_is_thrown
    # target_in_reward

    #actionの変化量に対してペナルティを与えるreward(後にカリキュラムラーニング)
    action_rate = RewTerm(
        func=mdp.action_rate_l2,
        weight=-1e-4
    )

    #jointの速度に対してペナルティを与えるreward（後にカリキュラムラーニング）
    joint_vel = RewTerm(
        func=mdp.joint_vel_l2,
        weight=-1e-4,
        params={"asset_cfg": SceneEntityCfg("robot")},
    )
    


@configclass
class CurriculumCfg:

    #num_steps以上から報酬のaction_rateの重みをweightに変更する
    action_rate = CurrTerm(
        func=mdp.modify_reward_weight, 
        params={
            "term_name": "action_rate", 
            "weight": -1e-1, 
            "num_steps": 10000
        }
    )

    #num_steps以上から報酬のjoint_velの重みをweightに変更する
    joint_vel = CurrTerm(
        func=mdp.modify_reward_weight,
        params={
            "term_name": "joint_vel",
            "weight": -1e-1,
            "num_steps": 10000
        }
    )

    #あとで箱の大きさを小さくするカリキュラムを書く

@configclass
class TerminationCfg:
    time_out = DoneTerm(
        func=mdp.time_out, 
        time_out=True
    )

    object_dropping = DoneTerm(
        func=mdp.root_height_below_minimum,
        params={
            "minimum_height": -0.05, 
            "asset_cfg": SceneEntityCfg("object")
        }
    )


"上で定義したクラスのインスタンスを作成して、強化学習環境全体を抽象的に設定している"

@configclass
class KomarmThrowEnvCfg(ManagerBasedRLEnvCfg):
    #あとで書く
    rewards: RewardsCfg = RewardsCfg()
    pass