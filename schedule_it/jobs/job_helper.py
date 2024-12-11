#
# LICENSE
# https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2023 https://github.com/Oops19
#


from schedule_it.modinfo import ModInfo
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry


from typing import Union, Set, List, Tuple, Dict

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)
log.enable()


class JobHelper:

    @staticmethod
    def get_ids(action_texts: Union[Set, List, Tuple], store_data: Dict, info: str = '') -> Set:
        """
        actions = a_zones = action.get('Zones', None)
        store_data = zone_data = getattr(jobs.store_parsed, 'zones', None)
        zone_ids = JobHelper().get(a_zones, zone_data)
        if zone_id not in zone_ids:
            continue
        """
        rv = set()
        if action_texts and store_data:
            for action_text in action_texts:
                rv.update(store_data.get(action_text, set()))
        if not rv:
            log.warn(f"Bad '{info}' configuration? Empty result for get_ids({action_texts}, {store_data})")
        return rv
