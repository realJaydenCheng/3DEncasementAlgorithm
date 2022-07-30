from Encase3D import *
from Encase3D import drawer



if __name__ == "__main__":
    cargos = [Cargo(175,100,120) for i in range(25)]
    cargos.extend([Cargo(127,103,94) for i in range(15)])
    cargos.extend([Cargo(157,128,90) for i in range(15)])
    cargos.extend([Cargo(237,128,136) for i in range(25)])

    case = Container(850,570,480)
    encase_cargos_into_container(cargos,case,VolumeGreedyStrategy)
    drawer.draw_reslut(case)