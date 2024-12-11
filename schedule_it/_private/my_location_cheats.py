#
# LICENSE
# https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2023 https://github.com/Oops19
#


from typing import Tuple, Any
from routing import SurfaceType, SurfaceIdentifier
from schedule_it.cache.obj_cache import ObjCache
from schedule_it.cache.sim_data_cache import SimDataCache

from schedule_it.modinfo import ModInfo

from sims.sim import Sim
# noinspection PyUnresolvedReferences
from sims4.math import Vector3, Quaternion, Transform, Location

from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ts4lib.utils.singleton import Singleton

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)
log.enable()

class MyLocationCheats:
    """
    set sim|obj sim_id/obj_id  # store sim/obj
    pos sim|obj "(0, 1, 2)"  # change absolute position
    move sim|obj "(0, 1, 2)"  # move relative
    rot sim|obj "(0, 0, 0, 1)"  # rotate sim / obj
    """

    # o19.pp.set obj 409565074712297982
    # o19.pp.rot obj
    # o19.mypp2 x
    # o19.pp.rot sim "(0,1,0,0)"
    # o19.pp.move sim "(0, 0, 1.4)"

    @staticmethod
    def conjugate(q: Quaternion):
        return Quaternion(-q.x, -q.y, -q.z, q.w)

    @staticmethod
    def q_mul(q1: Quaternion, q2: Quaternion):
        w = q1.w * q2.w - q1.x * q2.x - q1.y * q2.y - q1.z * q2.z
        x = q1.w * q2.x + q1.x * q2.w + q1.y * q2.z - q1.z * q2.y
        y = q1.w * q2.y - q1.x * q2.z + q1.y * q2.w + q1.z * q2.x
        z = q1.w * q2.z + q1.x * q2.y - q1.y * q2.x + q1.z * q2.w
        return Quaternion(x, y, z, w)

    @staticmethod
    def split_location(sim_obj: Any):
        location = getattr(sim_obj, 'location', None)

        _transform = getattr(location, 'transform', None)
        position = getattr(_transform, 'translation', None)
        orientation = getattr(_transform, 'orientation', None)

        _routing_surface = getattr(location, 'routing_surface', None)  # location.routing_surface.type
        surface_id = int(getattr(_routing_surface, 'type', None))

        zone_id = getattr(location, 'zone_id', None)
        level = getattr(sim_obj, 'level', None)
        return location,  position, orientation, zone_id, level, surface_id


    @staticmethod
    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.pp.set', '...',
                              command_arguments=(
                                      CommonConsoleCommandArgument('xxx_type', 'str', '(s|o) (sim|obj) (sim|object)', is_optional=False),
                                      CommonConsoleCommandArgument('xxx_id', 'int', '(sim_id|obj_id)', is_optional=False),
                              )
                          )
    def cheat_o19_pp_set(output: CommonConsoleCommandOutput, xxx_type: str, xxx_id: int):
        try:
            sc = SimDataCache()
            oc = ObjCache()
            if xxx_type[0] == 's':
                sc.sim_id = xxx_id
                output(f"{sc.sim}")
            elif xxx_type[0] == 'o':
                oc.obj_id = xxx_id
                output(f"{oc.obj_data_init}")  # (obj, obj_location, obj_position, obj_transform, obj_zone_id, obj_level, obj_surface_id)})
                obj, obj_location, obj_position, obj_orientation, obj_zone_id, obj_level, obj_surface_id = oc.obj_data_init
                output(f"obj_position {obj_position}")
                output(f"obj_orientation {obj_orientation}")

            else:
                output(f"Unknown type '{xxx_type}")
                return
            output(f"ok")
        except Exception as e:
            output(f"Error {e}")

    @staticmethod
    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.pp.rot', '...',
                              command_arguments=(
                                      CommonConsoleCommandArgument('xxx_type', 'str', '(s|o) (sim|obj) (sim|object)', is_optional=False),
                                      CommonConsoleCommandArgument('quaternion', 'str', '(0, 0, 0, 1) as (x, y, z, w)', is_optional=True),
                              )
                          )
    def cheat_o19_pp_rot(output: CommonConsoleCommandOutput, xxx_type: str, quaternion: str = None):
        try:
            sc = SimDataCache()
            oc = ObjCache()
            if quaternion:
                quaternion = quaternion.replace('(', '').replace(' ', '').replace(')', '')
                x, y, z, w = quaternion.split(',')
                x = float(x)
                y = float(y)
                z = float(z)
                w = float(w)
            else:
                x = y = z = 0.0
                w = 1.0

            obj, obj_location, obj_position, obj_orientation, obj_zone_id, obj_level, obj_surface_id = oc.obj_data

            if obj_location is None:
                output(f"ERROR: Location is None")
                return
            if xxx_type[0] == 's':
                output(f"{obj_orientation} * {Quaternion(x, y, z, w)}")
                obj_orientation = MyLocationCheats().q_mul(obj_orientation, Quaternion(x, y, z, w))
            else:
                obj_orientation = Quaternion(x, y, z, w)  # replace obj_orientation

            _transform = Transform(obj_position, obj_orientation)
            _routing_surface = SurfaceIdentifier(obj_zone_id, obj_level, obj_surface_id)
            location = Location(_transform, _routing_surface)

            if xxx_type[0] == 's':
                sim = sc.sim
                sim.location = location
                # sim.reset(ResetReason.RESET_EXPECTED, None, 'Teleport') - stops animation :(
            elif xxx_type[0] == 'o':
                obj = oc.obj
                obj.location = location
            output(f"ok")
        except Exception as e:
            output(f"Error {e}")

    @staticmethod
    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.pp.move', 'Move relative to object position and orientation',
                              command_arguments=(
                                      CommonConsoleCommandArgument('xxx_type', 'str', '(s|o) (sim|obj) (sim|object)', is_optional=False),
                                      CommonConsoleCommandArgument('position', 'str', '(0, 0, 0) as (x, y, z)', is_optional=True),
                              )
                          )
    def cheat_o19_pp_move(output: CommonConsoleCommandOutput, xxx_type: str, position: str = None):
        try:
            sc = SimDataCache()
            oc = ObjCache()
            if position:
                position = position.replace('(', '').replace(' ', '').replace(')', '')
                x, y, z = position.split(',')
                x = float(x)
                y = float(y)
                z = float(z)
            else:
                x = y = z = 0.0

            sim_location,  sim_position, sim_orientation, sim_zone_id, sim_level, sim_surface_id = MyLocationCheats().split_location(sc.sim)

            obj, obj_location, obj_position, obj_orientation, obj_zone_id, obj_level, obj_surface_id = oc.obj_data
            if obj is None:
                output(f"ERROR: Object is None.")
                return

            if x != 0 or y != 0 or z != 0:
                v4d = Quaternion(x, y, z, 0)  # w = 0
                v4d = MyLocationCheats().q_mul(MyLocationCheats().q_mul(obj_orientation, v4d), MyLocationCheats().conjugate(obj_orientation))
            else:
                v4d = Quaternion(x, y, z, 1)  # w = 1
            position = Vector3(obj_position.x + v4d.x, obj_position.y + v4d.y, obj_position.z + v4d.z)

            if xxx_type[0] == 's':
                _transform = Transform(position, sim_orientation)
                _routing_surface = SurfaceIdentifier(obj_zone_id, obj_level, obj_surface_id)
                location = Location(_transform, _routing_surface)

                sim = sc.sim
                sim.location = location
            elif xxx_type[0] == 'o':
                _transform = Transform(position, obj_orientation)
                _routing_surface = SurfaceIdentifier(obj_zone_id, obj_level, obj_surface_id)
                location = Location(_transform, _routing_surface)

                obj = oc.obj
                obj.location = location
            output(f"ok")
        except Exception as e:
            output(f"Error {e}")

    @staticmethod
    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.pp.pos', 'Move to absolute position.',
                              command_arguments=(
                                      CommonConsoleCommandArgument('xxx_type', 'str', '(s|o) (sim|obj) (sim|object)', is_optional=False),
                                      CommonConsoleCommandArgument('position', 'str', '(0, 0, 0) as (x, y, z)', is_optional=False),
                              )
                          )
    def cheat_o19_pp_pos(output: CommonConsoleCommandOutput, xxx_type: str, position: str = None):
        try:
            position = position.replace('(', '').replace(' ', '').replace(')', '')
            x, y, z = position.split(',')
            x = float(x)
            y = float(y)
            z = float(z)

            sc = SimDataCache()
            oc = ObjCache()
            obj, obj_location, obj_position, obj_orientation, obj_zone_id, obj_level, obj_surface_id = oc.obj_data
            if obj is None:
                output(f"ERROR: Object is None.")
                return

            obj_position = Vector3(x, y, z)  # replace obj_position with user-data

            _transform = Transform(obj_position, obj_orientation)
            _routing_surface = SurfaceIdentifier(obj_zone_id, obj_level, obj_surface_id)
            location = Location(_transform, _routing_surface)

            if xxx_type[0] == 's':
                sim = sc.sim
                sim.location = location
            elif xxx_type[0] == 'o':
                obj = oc.obj
                obj.location = location
            output(f"ok")
        except Exception as e:
            output(f"Error {e}")

    # todo on-lot-load - clear cache