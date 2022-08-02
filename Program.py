from Encase3D import *
from Encase3D import drawer



if __name__ == "__main__":
    cargos = [Cargo(170,100,120) for i in range(30)]
    cargos.extend([Cargo(100,80,90) for i in range(30)])
    cargos.extend([Cargo(150,120,90) for i in range(30)])
    cargos.extend([Cargo(210,120,100) for i in range(30)])

    case = Container(850,570,480)
    print(
        encase_cargos_into_container(cargos,case,VolumeGreedyStrategy)
    )
    case.save_encasement_as_file()
    drawer.draw_reslut(case)
    