from typing import Iterable, List
from _cargo import *
from _container import *

class Strategy(object):
    # 继承此类 重写两个函数 实现自定义两个装载策略: 装箱顺序 和 货物摆放.
    def encasement_sequence(cargos:Iterable) -> Iterable:
        return cargos

    def choose_cargo_poses(cargo:Cargo) -> list:
        return list(CargoPose)

def encase_cargos_into_container(
    cargos:Iterable, 
    container:Container, 
    strategy:Strategy
):
    sorted_cargos:List[Cargo] = strategy.encasement_sequence(cargos)
    i, j = 0, 0
    while i < len(sorted_cargos):
        cargo = sorted_cargos[i]
        poses = strategy.choose_cargo_poses(cargo)
        while j < len(poses):
            cargo.pose = poses[j]
            is_encased = container._encase(cargo)
            if is_encased.is_valid:
                break
            j += 1
        if is_encased.is_valid:
            i += 1 # 成功放入 继续装箱
        elif is_encased == Point(-1,-1,0):
            continue # 没放进去但是修改了参考线位置 重装
        else :
            i += 1 # 纯纯没放进去 跳过看下一个箱子


class VolumeGreedyStrategy(Strategy):
    def encasement_sequence(cargos:Iterable) -> Iterable:
        return sorted(cargos, key= lambda cargo:cargo.volume)

    def choose_cargo_poses(cargo:Cargo) -> list:
        return list(CargoPose)