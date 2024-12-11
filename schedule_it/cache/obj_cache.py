#
# LICENSE
# https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2023 https://github.com/Oops19
#


from typing import Tuple, Any

from schedule_it.modinfo import ModInfo
from ts4lib.utils.singleton import Singleton

# noinspection PyUnresolvedReferences
from sims4.math import Vector3, Quaternion, Transform, Location

from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent


class ObjCache(object, metaclass=Singleton):
    def __init__(self):
        self._obj_id = None
        self._obj_data_init = {}
        self._obj_data = {}
        self._obj = None

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity().name)
    def handle_event(event_data: S4CLZoneLateLoadEvent):
        # clear cache when loading a zone
        sc = ObjCache()
        sc._obj_id = None
        sc._obj_data_init = {}
        sc._obj_data = {}
        sc._obj = None

    @property
    def obj(self) -> Any:
        return self._obj

    @property
    def obj_data_init(self) -> Tuple[Any, Location, Vector3, Quaternion, int, int, int]:
        return self._obj_data_init.get(self._obj_id, (None, None, None, None, None, None, None))

    @property
    def obj_data(self) -> Tuple[Any, Location, Vector3, Quaternion, int, int, int]:
        return self._obj_data.get(self.obj_id, (None, None, None, None, None, None, None))  # update the location data

    @property
    def obj_id(self) -> int:
        return self._obj_id

    @obj_id.setter
    def obj_id(self, obj_id: int = None):
        if obj_id is None:
            return
        obj = CommonObjectUtils.get_game_object(obj_id)

        obj_location = getattr(obj, 'location', None)
        obj_level = getattr(obj, 'level', None)
        obj_zone_id = getattr(obj_location, 'zone_id', None)
        _obj_transform = getattr(obj_location, 'transform', None)
        obj_position = getattr(_obj_transform, 'translation', None)
        obj_orientation = getattr(_obj_transform, 'orientation', None)
        _obj_routing_surface = getattr(obj_location, 'routing_surface', None)  # location.routing_surface.type
        obj_surface_id = int(getattr(_obj_routing_surface, 'type', None))

        self._obj = obj
        self._obj_id = obj_id
        if obj_id not in self._obj_data_init.keys():
            self._obj_data_init.update({obj_id: (obj, obj_location, obj_position, obj_orientation, obj_zone_id, obj_level, obj_surface_id)})
        self._obj_data.update({obj_id: (obj, obj_location, obj_position, obj_orientation, obj_zone_id, obj_level, obj_surface_id)})
