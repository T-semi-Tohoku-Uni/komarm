from pathlib import Path

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

TEMPLATE_ASSETS_DATA_DIR = Path(__file__).resolve().parent


KOMARM_CFG = ArticulationCfg(
    spawn=sim_utils.UrdfFileCfg(
        fix_base=False,
        replace_cylinders_with_capsules=True,
        asset_path=f"{TEMPLATE_ASSETS_DATA_DIR}/inrof2026_koma_urdf/urdf/komarm.urdf",
        activate_contact_sensors=False,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            max_depenetration_velocity=5.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True,
            solver_position_iteration_count=8,
            solver_velocity_iteration_count=0,
        ),
        joint_drive=sim_utils.UrdfConverterCfg.JointDriveCfg(
            gains=sim_utils.UrdfConverterCfg.JointDriveCfg.PDGainsCfg(stiffness=0, damping=0)
        ),
    ),

    init_state=ArticulationCfg.InitialStateCfg(
        rot=(1.0, 0.0, 0.0, 0.0),
        pos=(0.0, 0.0, 0.13),
        joint_pos={
            "Revolute_1": 0.0,
            "Revolute_2": -1.3,
            "Revolute_3": 1.0,
            "Revolute_4": 0.0,
            "Revolute_5": 0.0,
            "Revolute_6": 0.0,
        },
        # Set initial joint velocities to zero
        joint_vel={".*": 0.0},
    ),
    actuators={
        "arm": ImplicitActuatorCfg(
            joint_names_expr=["Revolute_.*"],
            effort_limit_sim=1.5,
            velocity_limit_sim=4.0,
            stiffness={
                "Revolute_1": 10.0,
                "Revolute_2": 20.0,
                "Revolute_3": 25.0,
                "Revolute_4": 15.0,
                "Revolute_5": 10.0,
                "Revolute_6": 5.0,
            },
            damping={
                "Revolute_1": 1.0,
                "Revolute_2": 2.0,
                "Revolute_3": 2.5,
                "Revolute_4": 1.5,
                "Revolute_5": 1.0,
                "Revolute_6": 0.5,
            }
        ),
    },
    soft_joint_pos_limit_factor=0.9,
)