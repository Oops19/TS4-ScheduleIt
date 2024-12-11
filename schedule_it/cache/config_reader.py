#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2023 https://github.com/Oops19
#


import re
from typing import Dict, Any, List, Set

from schedule_it.cache.config_type import ConfigType
from schedule_it.modinfo import ModInfo
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from ts4lib.custom_enums.custom_body_type import CustomBodyType
from ts4lib.enums.vanilla_objects import VanillaObjects
from ts4lib.enums.vanilla_regions import VanillaRegions
from ts4lib.enums.vanilla_venues import VanillaVenues
from ts4lib.utils.config.reader_interface import ReaderInterface
from ts4lib.utils.config.store_parsed import StoreParsed
from ts4lib.utils.config.store_raw import StoreRaw

from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry

from ts4lib.utils.tuning_helper import TuningHelper
from ts4lib.utils.vanilla_names import VanillaNames
from ts4lib.utils.worlds_and_neighbourhoods import WorldsAndNeighbourhoods

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)
log.enable()


###
class ConfigReader(ReaderInterface):
    def __init__(self, base_namespace: str, files: Dict):
        super().__init__(base_namespace, files)
        self.th = TuningHelper()
        try:
            from ts4lib.utils.sims.cache.sim_cache import SimCache
            self.sc = SimCache()

        except:
            self.sc = None
            log.warn("Failed to initialize SimCache!")

    def parse_definitions(self, file: str, definitions: List) -> Any:
        log.debug(f"parse_definitions({file}, {definitions}: {type(definitions)})")
        f = file.split('.', 1)[0]
        rv = set()
        if f == 'sims':
            group_values = self._get_sim_ids(definitions)
        elif f == 'buffs':
            group_values = self._get_tuning_ids('BUFF', definitions)
        elif f == 'traits':
            group_values = self._get_tuning_ids('TRAIT', definitions)
        elif f == 'interactions':
            group_values = self._get_tuning_ids('INTERACTION', definitions)
        elif f == 'lot_traits':
            group_values = self._get_tuning_ids('ZONE_MODIFIER', definitions)
        elif f == 'broadcasters':
            group_values = self._get_tuning_dict( 'BROADCASTER', definitions)  # {id: (tuning, manager, name), } #
        elif f == 'statistics':
            group_values = self._get_tuning_ids('STATISTIC', definitions)
        elif f == 'snippets':
            group_values = self._get_tuning_ids('SNIPPET', definitions)
        elif f == 'worlds':
            group_values = self._get_locations(worlds=definitions)
        elif f == 'neighbourhoods':
            group_values = self._get_locations(neighbourhoods=definitions)
        elif f == 'venues':
            # group_values = self._get_from_enum(VanillaVenues, definitions)
            group_values = self._get_from_pseudo_enum(f, definitions)
        elif f == 'regions':
            # group_values = self._get_from_enum(VanillaRegions, definitions)
            group_values = self._get_from_pseudo_enum(f, definitions)
        elif f == 'body_parts':
            # group_values = self._get_from_enum(BodyType, definitions)
            group_values = self._get_from_enum(CustomBodyType, definitions)
        elif f in ['animations', 'objects', 'zones', ]:
            group_values = set(definitions)  # Don't parse
        elif f in ['vanilla_outfits', 'outfits', 'outfit_sequences', ]:
            group_values = set()  # TODO
        else:
            log.warn(f"Parsing of '{f}' not implemented!")
            return set()
        log.debug(f"parse_definitions({file}) -> {group_values}")
        return group_values

    def _get_from_pseudo_enum(self, class_name: str, definitions):
        ids = set()
        for definition in definitions:
            if f"{definition}".isdecimal():
                ids.add(int(definition))
            else:
                if class_name == 'venues':
                    ids.add(VanillaVenues().instance_id(definition))
                elif class_name == 'regions':
                    ids.add(VanillaRegions().instance_id(definition))
                elif class_name == 'outfits':
                    # only exact match, to be extended to match also short names
                    ids.add(VanillaObjects().instance_id(definition))

        if 0 in ids:
            ids.remove(0)
        return ids

    def _get_from_enum(self, class_name: Any, definitions):
        """
        class_name: properly imported class (eg 'VanillaRegions') or full qualified class name (eg 'ts4lib.common_enums.vanilla_regions.VanillaRegions')
        """
        vn = VanillaNames()
        ids = set()
        for definition in definitions:
            if f"{definition}".isdecimal():
                ids.add(int(definition))
            else:
                ids.add(vn.to_enum(class_name, definition).value)
        return ids

    def _get_tuning_dict(self, manager: str, definitions: List[str]) -> Dict:
        return self.th.get_tuning_dict(manager, definitions)

    def _get_tuning_ids(self, manager: str, definitions: List[str]) -> Set[int]:
        return self.th.get_tuning_ids(manager, definitions)

    def _get_locations(self, worlds: List = None, neighbourhoods: List = None) -> Set[int]:
        if worlds:
            return WorldsAndNeighbourhoods().get_world_ids(worlds)
        elif neighbourhoods:
            return WorldsAndNeighbourhoods().get_neighbourhood_ids(neighbourhoods)
        else:
            return set()

    def _get_sim_ids(self, definitions: List) -> Set[int]:
        sim_ids = set()
        for sim_definition in definitions:
            sim_definition = f"{sim_definition}".lower().strip()  # convert to string to support `123` and `'123'`
            if sim_definition.isdigit():
                sim_ids.add(int(sim_definition))
                continue
            if self.sc is None:
                continue

            if sim_definition.startswith('##&') or sim_definition.startswith('##|'):
                # B1) Handle 1-n groups, eg 'GHOST'
                groups = re.sub(r'[#|, \t]+', ' ', sim_definition).strip()
                _sim_ids: Set = None
                for group in groups.split(' '):
                    if group[0] == '!':
                        invert = True
                        group = group[1:]
                    else:
                        invert = False
                    if group in ['all']:
                        __sim_ids = self.sc.sim_ids.copy()
                    elif group == 'female':
                        __sim_ids = self.sc.get_sim_ids_by_genders(['female', ])
                    elif group == 'male':
                        __sim_ids = self.sc.get_sim_ids_by_genders(['male', ])
                    elif group == 'tyae':
                        __sim_ids = self.sc.age_tyae
                    elif group in ['infant', 'toddler', 'child', 'teen', 'youngadult', 'adult', 'elder']:
                        __sim_ids = self.sc.get_sim_ids_by_ages([group])
                    elif group in ['human', 'alien', 'vampire', 'mermaid', 'witch', 'werewolf', 'ghost']:
                        __sim_ids = self.sc.get_sim_ids_by_occult_types([group])
                    else:
                        log.warn(f"Group '{group}' not found.")
                        continue
                    if invert:
                        __sim_ids = self.sc.sim_ids.difference(__sim_ids)

                    log.debug(f"Group {group} with {len(__sim_ids)} ids.")
                    if _sim_ids is None:
                        _sim_ids = __sim_ids
                    else:
                        _sim_ids = _sim_ids & __sim_ids
                    log.debug(f"Joined {group} with {len(__sim_ids)} ids.")

                if _sim_ids:
                    sim_ids.update(_sim_ids)

            elif '#' in sim_definition:
                # B3) Assume that this is a (partial) sim_name
                _sim_ids, _, _, _, _ = self.sc.get_sim_ids_by_sim_name(sim_definition)
                sim_ids.update(_sim_ids)
            else:
                log.warn(f"Invalid sim definition '{sim_definition}'.")
        return sim_ids

    @staticmethod
    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.si.readcfg', '...',)
    def o19_cheat_read_cfg(output: CommonConsoleCommandOutput):
        try:
            files = ConfigType().types
            base_namespace = ModInfo.get_identity().base_namespace
            cr = ConfigReader(base_namespace, files)
            cr.read_files()
            store_raw = StoreRaw()
            store_parsed = StoreParsed()
            for file in files.keys():
                file_id = cr.file_id(file)
                log.debug(f"RAW {file} = {getattr(store_raw, file_id, None)}")
                log.debug(f">>> {file} = {getattr(store_parsed, file_id, None)}")
            output("ok")
        except Exception as e:
            log.error(f"{e}")


# TODO REMOVE ME LATER ########################################

@CommonEventRegistry.handle_events(ModInfo.get_identity().name)
def handle_event(event_data: S4CLZoneLateLoadEvent):

    try:
        files = ConfigType().types
        base_namespace = ModInfo.get_identity().base_namespace
        cr = ConfigReader(base_namespace, files)
        cr.read_files()
        store_raw = StoreRaw()
        store_parsed = StoreParsed()
        for file in files.keys():
            file_id = cr.file_id(file)
            log.debug(f"RAW {file} = {getattr(store_raw, file_id, None)}")
            log.debug(f">>> {file} = {getattr(store_parsed, file_id, None)}")
    except Exception as e:
        log.error(f"{e}")