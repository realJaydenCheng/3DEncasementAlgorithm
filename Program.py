from Encase3D import *
from Encase3D import drawer



if __name__ == "__main__":
    cargos = [Cargo(175,80,120) for i in range(10)]
    cargos.extend([Cargo(47,63,80) for i in range(20)])
    cargos.extend([Cargo(57,48,30) for i in range(20)])
    cargos.extend([Cargo(257,88,130) for i in range(20)])

    case = Container(750,470,420)
    encase_cargos_into_container(cargos,case,VolumeGreedyStrategy())
    drawer.draw_reslut(case)