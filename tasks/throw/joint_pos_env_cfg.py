
from tasks.throw.throw_env_cfg import ThrowEnvCfg
from robots import KOMARM_CFG


#ThrowEnvCfgで定義した環境を、具体化しているクラス
class KomarmThrowCubeEnvCfg(ThrowEnvCfg):
    def __post_init__(self):
        super().__post_init__()

        self.scene.robot = KOMARM_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")
        


class KomarmThrowCubeEnvCfg_PLAY(KomarmThrowCubeEnvCfg):
    def __post_init__(self):
        super().__post_init__()

