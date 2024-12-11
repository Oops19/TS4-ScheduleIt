#
# LICENSE
# https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2023 https://github.com/Oops19
#
from schedule_it.modinfo import ModInfo
from sims.sim import Sim
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from ts4lib.utils.singleton import Singleton


class SimDataCache(object, metaclass=Singleton):
    def __init__(self):
        self._sim_id = None
        self._sim_data = {}

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity().name)
    def handle_event(event_data: S4CLZoneLateLoadEvent):
        # clear cache when loading a zone
        sc = SimDataCache()
        sc._sim_id = None
        sc._sim_data = {}

    @property
    def sim_id(self) -> int:
        if self._sim_id is None:
            self.sim_id = None
        return self._sim_id

    @sim_id.setter
    def sim_id(self, sim_id: int = None):
        if sim_id is None or sim_id == 0:
            sim_id = CommonSimUtils.get_active_sim_id()
        sim: Sim = CommonSimUtils.get_sim_instance(sim_id)
        self._sim_id = sim_id
        self._sim_data.update({sim_id: sim})

    @property
    def sim(self) -> Sim:
        if self._sim_id is None:
            self.sim_id = None
        return self._sim_data.get(self._sim_id)
