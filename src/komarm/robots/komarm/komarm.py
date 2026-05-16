from pathlib import Path

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

TEMPLATE_ASSETS_DATA_DIR = Path(__file__).resolve().parent


KOMARM_CFG = ArticulationCfg(
    spawn=sim_utils.UrdfFileCfg(
        fix_base=True,
        replace_cylinders_with_capsules=True,
        asset_path=f"{TEMPLATE_ASSETS_DATA_DIR}/urdf/komarm.urdf",
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
        pos=(0.0, 0.0, 0.08),
        joint_pos={
            "Revolute_7": 0.0,
            "Revolute_8": 0.0,
            "Revolute_9": 0.0,
            "Revolute_11": 0.0,
            "Revolute_12": 0.0,
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
                "Revolute_12": 100.0,
                "Revolute_11": 100.0,
                "Revolute_7" : 80.0,
                "Revolute_8" : 50.0,
                "Revolute_9" : 30.0,  
            },
            damping={
                "Revolute_12": 20.0,
                "Revolute_11": 20.0,
                "Revolute_7" : 15.0,
                "Revolute_8" : 10.0,
                "Revolute_9" : 8.0,  
            },
        ),
    },
    soft_joint_pos_limit_factor=0.9,
)