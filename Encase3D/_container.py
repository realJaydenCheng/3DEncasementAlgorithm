from _cargo import *
from copy import deepcopy


class Container(object):
    def __init__(self, length: int, width: int, height: int) -> None:
        self._length = length
        self._width = width
        self._height = height
        self._refresh()

    def _refresh(self):
        self._horizontal_line = 0  # 水平放置参考线
        self._vertical_line = 0  # 垂直放置参考线
        self._available_points = [Point(0, 0, 0)]  # 可放置点有序集合
        self._setted_cargos = []

    def _sort_available_points(self):
        self._available_points.sort(key=lambda x: x.z)
        self._available_points.sort(key=lambda x: x.x)
        self._available_points.sort(key=lambda x: x.y)

    def is_encasable(self, site: Point, cargo: Cargo) -> bool:
        encasable = True
        temp = deepcopy(cargo)
        temp.point = site
        if (
            temp.x + temp.length > self.length or
            temp.y + temp.width > self.width or
            temp.z + temp.height > self.height
        ):
            encasable = False
        for setted_cargo in self._setted_cargos:
            if _is_cargos_collide(temp, setted_cargo):
                encasable = False
        return encasable

    def _encase(self, cargo: Cargo) -> Point:
        # flag存储放置位置, (-1, -1, 0)放置失败并调整参考线, (-1, -1, -1)放置失败.
        flag = Point(-1, -1, -1)  
        # 用于记录执行前的参考线位置, 便于后续比较
        history = [self._horizontal_line, self._vertical_line]
        def __is_line_changed(horizontal_line:int, vertical_line:int) -> bool:
            return (
                not flag.is_valid and # 防止破坏已经确定可放置的点位, 即只能在(-1, -1, -1)基础上改
                self._horizontal_line == history[0] and 
                self._vertical_line == history[-1]
            ) 
        for point in self._available_points:
            if (
                self.is_encasable(point, cargo) and
                point.x + cargo.length < self._horizontal_line and
                point.z + cargo.height < self._vertical_line
            ):
                flag = point
                break
        if not flag.is_valid:
            if (
                self._horizontal_line == 0 or
                self._horizontal_line == self.length
            ):
                if self.is_encasable(Point(0, 0, self._vertical_line), cargo):
                    flag = (0, 0, self._vertical_line)
                    self._vertical_line += cargo.height
                    self._horizontal_line = cargo.length 
                    # 放置了货物 不检测参考线改变
                elif self._vertical_line < self.height:
                    self._vertical_line = self.height
                    self._horizontal_line = self.length
                    if __is_line_changed():
                        flag.z == 0 # 放置失败并调整参考线
            else:
                for point in self._available_points:
                    if (
                        point.x == self._horizontal_line and
                        point.y == 0 and
                        self.is_encasable(point, cargo) and
                        point.z + cargo.height <= self._vertical_line
                    ):
                        flag = point
                        self._horizontal_line += cargo.length
                        break
                        # 放置了货物 不检测参考线改变
                if not flag.is_valid:
                    self._horizontal_line = self.length
                    if __is_line_changed():
                        flag.z == 0 # 放置失败并调整参考线
        if flag.is_valid:
            cargo.point = flag
            if flag in self._available_points:
                self._available_points.remove(flag)
            self._adjust_setting_cargo(cargo)
            self._setted_cargos.append(cargo)
            self._available_points.extend([
                Point(cargo.x + cargo.length, cargo.y, cargo.z),
                Point(cargo.x, cargo.y + cargo.width, cargo.z),
                Point(cargo.x, cargo.y, cargo.z + cargo.height)
            ])
            self._sort_available_points()
        return flag

    def _adjust_setting_cargo(self, cargo: Cargo):
        site = cargo.point
        temp = deepcopy(cargo)
        if not self.is_encasable(site, cargo):
            return None
        xyz = [site.x, site.y, site.z] 
        # 序列化坐标以执行遍历递减操作, 减少冗余
        for i in range(3):
            while xyz[i] > 1:
                xyz[i] -= 1
                temp.point = Point(xyz[0], xyz[1], xyz[2])
                for setted_cargo in self._setted_cargos:
                    if not _is_cargos_collide(setted_cargo, temp):
                        continue
                    xyz[i] += 1
                    break
        cargo.point = Point(xyz[0], xyz[1], xyz[2]) # 反序列化

    @property
    def length(self) -> int:
        return self._length

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def getVolume(self) -> int:
        return self.height * self.length * self.width


def _is_rectangles_overlap(rec1, rec2) -> bool:
    return not (
        rec1[0] >= rec2[2] or rec1[1] >= rec2[3] or
        rec2[0] >= rec1[2] or rec2[1] >= rec1[3]
    )


def _is_cargos_collide(cargo0: Cargo, cargo1: Cargo) -> bool:
    return (
        _is_rectangles_overlap(cargo0.get_shadow_of("xy"), cargo1.get_shadow_of("xy")) and
        _is_rectangles_overlap(cargo0.get_shadow_of("yz"), cargo1.get_shadow_of("yz")) and
        _is_rectangles_overlap(cargo0.get_shadow_of(
            "xz"), cargo1.get_shadow_of("xz"))
    )
