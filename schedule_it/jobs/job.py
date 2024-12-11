#
# LICENSE
# https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2023 https://github.com/Oops19
#


import importlib
import random
from typing import Set, Tuple, Dict, List, Any

import services

from objects import HiddenReasonFlag
from routing import SurfaceIdentifier

from schedule_it.jobs.job_helper import JobHelper

from schedule_it.modinfo import ModInfo
from schedule_it.store.action_store import ActionStore
from schedule_it.store.lot_trait_store import LotTraitStore
from server_commands.object_commands import _all_objects_gen
from sims.sim_info import SimInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from sims4communitylib.utils.common_type_utils import CommonTypeUtils

from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils
from sims4communitylib.utils.sims.common_sim_spawn_utils import CommonSimSpawnUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from ts4lib.classes.coordinates.std_quaternion import StdQuaternion
from ts4lib.classes.coordinates.std_vector3 import StdVector3
from ts4lib.enums.vanilla_regions import VanillaRegions
from ts4lib.enums.vanilla_venues import VanillaVenues
from ts4lib.utils.config.store_parsed import StoreParsed
from ts4lib.utils.interaction.enqueue_interaction import EnqueueInteraction
from ts4lib.utils.location_ids import LocationIDs
from ts4lib.utils.objects.lot_object_definition import LotObjectDefinition
from ts4lib.utils.objects.lot_objects import LotObjects
from ts4lib.utils.sims.cache.sim_cache import SimCache
from ts4lib.utils.tuning_helper import TuningHelper
from ts4lib.utils.vanilla_names import VanillaNames
from ts4lib.utils.worlds_and_neighbourhoods import WorldsAndNeighbourhoods
from zone_modifier.zone_modifier_service import ZoneModifierService
# noinspection PyUnresolvedReferences
from sims4.math import Vector3, Quaternion, Transform, Location
from sims4.resources import Types as ResourceType


log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)
log.enable()


class Job:
    def __init__(self):
        self.th = TuningHelper()
        self.store_parsed = StoreParsed()


    @staticmethod
    def run(params: List = None):
        log.debug(f"run({params}: {type(params)})")

        lo = LotObjects()  # TODO move to top
        if isinstance(params, str):
            param = params
        else:
            param = params[0]
        jobs = Job()
        if not param:
            return
        action = ActionStore().actions.get(param)
        log.debug(f"action='{action}'")
        log.debug(f"store_parsed={jobs.store_parsed.__dict__.items()}")

        probability = action.get('GlobalProbability', 100)
        if probability < 100:
            if random.randint(0, 100) > probability:
                log.debug(f"Exit > GlobalProbability({probability}")
                return
        probability = action.get('LocalProbability', 100)

        l = LocationIDs()
        jh = JobHelper()

        zone_id = l.get_current_zone_id()
        a_zones = action.get('Zones', None)
        zone_data = getattr(jobs.store_parsed, 'zones', None)
        if a_zones and zone_data:
            zone_ids = jh.get_ids(a_zones, zone_data, 'zones')
            if zone_id not in zone_ids:
                log.debug(f"Exit > Zone {zone_id} not in {zone_ids}")
                return
            log.debug(f"Zone {zone_id} in {zone_ids}")

        world_id = l.get_current_world_id()
        a_worlds = action.get('Worlds', None)
        world_data = getattr(jobs.store_parsed, 'worlds', None)
        if a_worlds and world_data:
            _world_ids = jh.get_ids(a_worlds, world_data, 'worlds')  # set with ids and strings
            world_ids = set()
            for _world_id in _world_ids:
                if f"{_world_id}".isdigit():
                    world_ids.add(int(_world_id))
                else:
                    try:
                        world_ids.update(WorldsAndNeighbourhoods().get_world_ids([f"{_world_id}", ]))
                    except:
                        pass
            if world_id not in world_ids:
                log.debug(f"Exit > World {world_id} not in {world_ids}")
                return
            log.debug(f"World {world_id} in {world_ids}")

        neighbourhood_id = l.get_current_neighbourhood_id()
        a_neighbourhoods = action.get('Neighbourhoods', None)
        neighbourhood_data = getattr(jobs.store_parsed, 'neighbourhoods', None)
        if a_neighbourhoods and neighbourhood_data:
            _neighbourhood_ids = jh.get_ids(a_neighbourhoods, neighbourhood_data, 'neighbourhoods')  # set with ids and strings
            neighbourhood_ids = set()
            for _neighbourhood_id in _neighbourhood_ids:
                if f"{_neighbourhood_id}".isdigit():
                    neighbourhood_ids.add(int(_neighbourhood_id))
                else:
                    try:
                        neighbourhood_ids.update(WorldsAndNeighbourhoods().get_neighbourhood_ids([f"{_neighbourhood_id}", ]))
                    except:
                        pass
            if neighbourhood_id not in neighbourhood_ids:
                log.debug(f"Exit > Neighbourhood {neighbourhood_id} not in {neighbourhood_ids}")
                return
            log.debug(f"Neighbourhood {world_id} in {neighbourhood_ids}")

        venue_id = l.get_current_venue_id()
        a_venues = action.get('Venues', None)
        venue_data = getattr(jobs.store_parsed, 'venues', None)
        if a_venues and venue_data:
            _venue_ids = jh.get_ids(a_venues, venue_data, 'venues')
            venue_ids = set()
            for _venue_id in _venue_ids:
                if f"{_venue_id}".isdigit():
                    venue_ids.add(int(_venue_id))
                else:
                    try:
                        # venue_ids.add(VanillaNames().to_enum(VanillaVenues, f"{_venue_id}").value)
                        venue_id = VanillaVenues().instance_id(f"{_venue_id}")
                        if venue_id:
                            venue_ids.add(venue_id)
                    except:
                        pass
            if venue_id not in venue_ids:
                log.debug(f"Exit > Venue {venue_id} not in {venue_ids}")
                return
            log.debug(f"Venue {venue_id} in {venue_ids}")

        region_id = l.get_current_region_id()
        a_regions = action.get('Regions', None)
        region_data = getattr(jobs.store_parsed, 'regions', None)
        if a_regions and region_data:
            _region_ids = jh.get_ids(a_regions, region_data, 'regions')
            region_ids = set()
            for _region_id in _region_ids:
                if f"{_region_id}".isdigit():
                    region_ids.add(int(_region_id))
                else:
                    try:
                        # region_ids.add(VanillaNames().to_enum(VanillaRegions, f"{_region_id}").value)
                        region_id = VanillaRegions().instance_id(f"{_region_id}")
                        if region_id:
                            region_ids.add(region_id)
                    except:
                        pass
            if region_id not in region_ids:
                log.debug(f"Exit > Region {region_id} not in {region_ids}")
                return
            log.debug(f"Region {region_id} in {region_ids}")

        a_add_lot_traits = action.get('AddLotTraits', ())
        a_remove_lot_traits = action.get('RemoveLotTraits', ())
        lot_trait_data = getattr(jobs.store_parsed, 'lot_traits', None)
        log.debug(f"lot_traits {lot_trait_data} +{a_add_lot_traits} -{a_remove_lot_traits}")
        if lot_trait_data and (a_add_lot_traits or a_remove_lot_traits):
            _add_lot_traits = jh.get_ids(a_add_lot_traits, lot_trait_data)
            _remove_lot_traits = jh.get_ids(a_remove_lot_traits, lot_trait_data)
            # Types.ZONE_MODIFIER
            __add_lot_traits = jobs.th.get_tuning_ids('ZONE_MODIFIER', list(_add_lot_traits))
            __remove_lot_traits = jobs.th.get_tuning_ids('ZONE_MODIFIER', list(_remove_lot_traits))
            log.debug(f"lot_traits +'{__add_lot_traits}' -'{__remove_lot_traits}'")
            jobs._lot_traits(__add_lot_traits, __remove_lot_traits)

        broadcaster_data = getattr(jobs.store_parsed, 'broadcasters', None)
        a_enable_broadcasters = action.get('EnableBroadcasters', ())
        a_disable_broadcasters = action.get('DisableBroadcasters', ())
        if broadcaster_data and (a_enable_broadcasters or a_disable_broadcasters):
            _enable_broadcasters = jh.get_ids(a_enable_broadcasters, broadcaster_data)
            _disable_broadcasters = jh.get_ids(a_disable_broadcasters, broadcaster_data)
            # Types.BROADCASTER
            __enable_broadcasters = jobs.th.get_tuning_dict('BROADCASTER', list(_enable_broadcasters))
            __disable_broadcasters = jobs.th.get_tuning_dict('BROADCASTER', list(_disable_broadcasters))
            jobs._broadcasters(__enable_broadcasters, __disable_broadcasters)

        num_runs = action.get('NumRuns', 1)

        found_objects = False
        spawn_objects = False
        object_data =  getattr(jobs.store_parsed, 'objects', None)
        a_objects = list(action.get('Objects', []))
        a_object_levels = list(action.get('ObjectLevels', []))  # currently not supported !
        a_spawn_objects = list(action.get('SpawnObjects', []))
        a_despawn_objects = action.get('DeSpawnObjects', False)
        object_ids: Set = set()
        object_ids_l: List = []
        if object_data and a_objects:
            _objects = jh.get_ids(a_objects, object_data)
            lo = LotObjects()
            for _object in _objects:
                if f"{_object}".startswith('-') and f"{_object}"[1:].isdecimal():  # negative numbers for instanced objects
                    if abs(int(_object)) in lo.get_objects().keys():
                        object_ids.add(abs(int(_object)))
                        continue
                if f"{_object}".isdecimal():  # GUID64
                    for lo_object in lo.get_objects().values():
                        lo_object: LotObjectDefinition = lo_object
                        if lo_object.guid64 == int(_object):  #  == object.definition.tuning_file_id
                            object_ids.add(int(_object))
                            continue
                for _name, _object_ids in lo.get_names().items():
                    if f"{_object}" in _name:
                        object_ids.update(_object_ids)

            if object_ids and a_object_levels:
                _object_ids = set()
                for object_id in object_ids:
                    lod: LotObjectDefinition = lo.get_objects().get(object_id)
                    if lod.obj_level in a_object_levels:
                        _object_ids.add(object_id)
                object_ids = _object_ids

            if object_ids:
                num_runs = min(num_runs, len(object_ids))
                found_objects = True
            else:
                if not a_spawn_objects:
                    log.debug(f"Exit > No objects '{_objects}' found on lot.")
                    return

        if a_spawn_objects and found_objects is False:
            spawn_objects = True
            # Get object IDs (guid64) to spawn
            object_ids = set()
            _objects = jh.get_ids(a_spawn_objects, object_data)
            lo = LotObjects()
            lo_objects = lo.get_objects()
            for _object in _objects:
                if f"{_object}".isdecimal():  # GUID64
                    object_ids.add(int(_object))
                    continue
                for _name, _object_ids in lo.get_names().items():
                    if f"{_object}" in _name:
                        for _object_id in _object_ids:
                            lo_object: LotObjectDefinition = lo_objects.get(_object_id)
                            object_ids.add(lo_object.guid64)

            if object_ids and a_object_levels:
                _object_ids = set()
                for object_id in object_ids:
                    game_object = CommonObjectUtils.get_game_object(object_id)
                    if game_object.level in a_object_levels:
                        _object_ids.add(object_id)
                object_ids = _object_ids

            if not object_ids:
                log.debug(f"Exit > No spawn objects '{_objects}' found.")
                return

        if object_ids:
            object_ids_l: List = list(object_ids)
            random.shuffle(object_ids_l)
            num_runs = min(num_runs, len(object_ids_l))

        # object_ids == set()  -> Ignore objects
        # found_objects | spawn_objects == True AND object_ids = (1, 2, )
        log.debug(f"found_objects={found_objects}, spawn_objects={spawn_objects}, object_ids={object_ids}, num_runs={num_runs}")  # TODO

        sc = SimCache()
        a_sims = action.get('Sims', [])
        a_spawn_sims = list(action.get('SpawnSims', []))
        sim_data = getattr(jobs.store_parsed, 'sims', None)
        found_sims = False
        spawn_sims = False
        sim_ids = set()

        # a_sims=['o19:bg'], a_spawn_sims=['o19:bg'], sim_data={'o19:bg': {425327441345782904, 425327441345645628}, 'o19:bellaGoth': {425327441345645628}}
        log.debug(f"a_sims={a_sims}, a_spawn_sims={a_spawn_sims}, sim_data={sim_data}")
        if a_sims and sim_data:
            for a_sim in a_sims:
                sim_ids.update(sim_data.get(a_sim), set())

            if sim_ids:
                # Make sure sims are on lot
                log.debug(f"sim_ids {sim_ids} exist")
                _sim_ids = set()
                for sim_id in sim_ids:
                    sim_info = CommonSimUtils.get_sim_info(sim_id)
                    if sim_info.is_instanced(allow_hidden_flags=HiddenReasonFlag.NONE):
                        _sim_ids.add(sim_id)
                sim_ids = _sim_ids
                log.debug(f"sim_ids {sim_ids} are on lot")

            if sim_ids:
                sim_ids = list(sim_ids)
                random.shuffle(sim_ids)
                num_runs = min(num_runs, len(sim_ids))
                found_sims = True
            else:
                if not a_spawn_sims:
                    log.debug(f"Exit > No sims '{a_sims}' found on lot.")
                    return
                else:
                    log.debug(f"No sims '{a_sims}' found on lot.")

        if a_spawn_sims and sim_data and found_sims is False:
            for a_sim in a_spawn_sims:
                sim_ids.update(sim_data.get(a_sim), set())

            if sim_ids:
                sim_ids = list(sim_ids)
                random.shuffle(sim_ids)
                num_runs = min(num_runs, len(sim_ids))
                spawn_sims = True
            else:
                log.debug(f"Exit > No spawn sims '{a_spawn_sims}' found.")
                return

        # sim_ids == set()  -> Ignore sims
        # found_sims | spawn_sims == True AND sim_ids = (1, 2, ...)
        log.debug(f"found_sims={found_sims}, spawn_sims={spawn_sims}, sim_ids={sim_ids}, num_runs={num_runs}")  # TODO



        for i in range(0, num_runs):
            if probability < 100:
                if random.randint(0, 100) > probability:
                    log.debug(f"Next > Probability({probability}")
                    continue

            game_object = None
            _obj_location = action.get('ObjectLocation', None)
            if object_ids:
                object_id = object_ids_l[i]
                if found_objects:
                    lod: LotObjectDefinition = lo.get_objects().get(object_id)
                    game_object = lod.game_object
                    object_location = game_object.location
                    log.debug(f"TODO: Found obj {object_id} at {object_location}")

                    obj_level = lod.obj_level
                    obj_surface_id = lod.obj_surface_id
                    obj_translation = StdVector3(lod.obj_position.x, lod.obj_position.y, lod.obj_position.z)
                    obj_orientation = StdQuaternion(lod.obj_orientation.w, lod.obj_orientation.x, lod.obj_orientation.y, lod.obj_orientation.z)
                else:
                    obj_levels, obj_surface_id, obj_translation, obj_orientation = jobs._process_location_data(_obj_location)
                    obj_level = random.choice(obj_levels)
                    obj_location = jobs._get_location(zone_id, obj_level, obj_surface_id, obj_translation, obj_orientation)
                    _obj_random_scale = action.get('RandomScale', 0)
                    obj_scale = action.get('Scale', 1) + random.random() * (_obj_random_scale * 2) - _obj_random_scale

                    # TODO spawn object
                    game_object = None  # TODO
                    log.debug(f"TODO: spawn obj {object_id} at {object_location} with scale {obj_scale} -> continue")
                    continue
                log.debug(f"obj_translation {obj_translation}")
                log.debug(f"obj_orientation {obj_orientation}")

            _sim_location = action.get('SimLocation', None)
            sim_levels, sim_surface_id, sim_translation, sim_orientation = jobs._process_location_data(_sim_location)
            sim_level = random.choice(sim_levels)

            log.debug(f"ffff {object_id}")
            log.debug(f"ffff {_sim_location}")
            if object_location and _sim_location:
                sim_level = obj_level
                sim_surface_id = obj_surface_id
                obj_orientation: StdQuaternion = obj_orientation
                sim_translation_4d = StdQuaternion(0, sim_translation.x, sim_translation.y, sim_translation.z)
                sim_translation_4d = (obj_orientation * sim_translation_4d) * obj_orientation.conjugate()
                sim_translation_3d = StdVector3(sim_translation_4d.x, sim_translation_4d.y, sim_translation_4d.z)
                sim_translation = obj_translation + sim_translation_3d
                sim_orientation = obj_orientation.multiply(sim_orientation)
                log.debug(f"!! sim_translation {sim_translation}")
                log.debug(f"!! sim_orientation {sim_orientation}")
            sim_location = jobs._get_location(zone_id, sim_level, sim_surface_id, sim_translation, sim_orientation)

            _object_animations = action.get('ObjectAnimations', None)
            if _object_animations:
                object_animation = random.choice(_object_animations)
                log.debug(f"TODO play obj animation {object_animation} ")  # TODO play the animation (later, together with sim?)

            sim = None
            if sim_ids:
                sim_id: int = sim_ids[i]
                sim_info = CommonSimUtils.get_sim_info(sim_id)

                if found_sims:
                    sim = CommonSimUtils.get_sim_instance(sim_id)
                    if action.get('ResetSim', False):
                        log.debug(f"Resetting sim {sim_info}")
                        CommonSimSpawnUtils().hard_reset(sim_info, source='ScheduleIt', cause='crontab job')
                    if action.get('TeleportSim', False):
                        log.debug(f"Teleporting sim {sim_info}")
                        sim.location = sim_location
                elif spawn_sims:
                    log.debug(f"Spawning sim {sim_info} at {sim_location}")
                    if CommonSimSpawnUtils().spawn_sim(sim_info, location=sim_location):
                        sim = CommonSimUtils.get_sim_instance(sim_id)

                if sim is None:
                    log.debug(f"Skip > No sim for '{sim_id}' found.")
                    continue

                # Sim is on lot
                a_add_traits = action.get('AddTraits', ())
                a_remove_traits = action.get('RemoveTraits', ())
                trait_data = getattr(jobs.store_parsed, 'traits', None)
                log.debug(f"traits +{a_add_traits} -{a_remove_traits} from  {trait_data} ")
                if trait_data and (a_add_traits or a_remove_traits):
                    _add_traits = jh.get_ids(a_add_traits, trait_data)
                    _remove_traits = jh.get_ids(a_remove_traits, trait_data)
                    jobs._traits(
                        sim_info,
                        _add_traits,
                        _remove_traits,
                    )

                a_add_buffs = action.get('AddBuffs', ())
                a_remove_buffs = action.get('RemoveBuffs', ())
                buff_data = getattr(jobs.store_parsed, 'buffs', None)
                log.debug(f"buffs {buff_data} +{a_add_buffs} -{a_remove_buffs}")
                if buff_data and (a_add_buffs or a_remove_buffs):
                    _add_buffs = jh.get_ids(a_add_buffs, buff_data)
                    _remove_buffs = jh.get_ids(a_remove_buffs, buff_data)
                    jobs._buffs(
                        sim_info,
                        _add_buffs,
                        _remove_buffs,
                    )

                # Sim is on lot
                a_sim_object_interactions = action.get('SimObjectInteractions', [])
                a_sim_interactions = action.get('SimInteractions', [])
                if a_sim_object_interactions:
                    a_interactions = a_sim_object_interactions
                elif a_sim_interactions:
                    a_interactions = a_sim_interactions
                else:
                    a_interactions = []
                interaction_data = getattr(jobs.store_parsed, 'interactions', None)
                log.debug(f"a_sim_interactions {a_sim_interactions}, interaction_data {interaction_data}")  # TODO de-duplicate
                log.debug(f"a_sim_object_interactions {a_sim_object_interactions}, interaction_data {interaction_data}")  # TODO de-duplicate
                if a_interactions and interaction_data:
                    log.debug(f"a_interactions {a_interactions}, interaction_data {interaction_data}")
                    a_interaction = random.choice(a_interactions)
                    interaction_ids = list(interaction_data.get(a_interaction))
                    interaction_id = random.choice(interaction_ids)
                    eq = EnqueueInteraction()
                    if a_sim_object_interactions:
                        lod: LotObjectDefinition = lo.get_objects().get(object_id)
                        game_object = lod.game_object
                        eq.run_interaction(sim, interaction_id=interaction_id, target=game_object)
                    else:
                        eq.run_interaction(sim, interaction_id=interaction_id)
                    continue

                a_sim_object_animations = action.get('SimObjectAnimations', [])
                log.debug(f"a_sim_object_animations {a_sim_object_animations}, a_sim_object_animations {a_sim_object_animations}")  # TODO de-duplicate
                log.debug(f"object_location {object_location}")
                log.debug(f"sim_location {sim_location}")
                sim.location = sim_location

                a_outfits = action.get('Outfits', [])
                if a_outfits:
                    a_outfit = random.choice(list(a_outfits))
                    outfit_category, outfit_index = a_outfit.split('.')
                    CommonOutfitUtils.set_current_outfit(sim_info, (int(outfit_category), int(outfit_index)))

                a_sim_animations = action.get('SimAnimations', [])
                animation_data = getattr(jobs.store_parsed, 'animations', None)
                log.debug(f"a_sim_animations {a_sim_animations}, animation_data {animation_data}")  # TODO de-duplicate
                if a_sim_animations and animation_data:
                    log.debug(f"a_sim_animations {a_sim_animations}, animation_data {animation_data}")
                    a_sim_animation = random.choice(list(a_sim_animations))
                    animation_names = list(animation_data.get(a_sim_animation))
                    animation_name = random.choice(animation_names)
                    eq = EnqueueInteraction()
                    eq.run_pose(sim, animation_name)

                    continue



    @staticmethod
    def _get_location(zone_id: int, level: int, surface_id: int, translation: StdVector3, orientation: StdQuaternion) -> Location:
        log.debug(f"_get_location({zone_id}, {level}, {surface_id}, {translation}, {orientation})")
        _translation = translation.as_ts4_vector3()
        _orientation = orientation.as_ts4_quaternion()
        _transform = Transform(_translation, _orientation)
        _routing_surface = SurfaceIdentifier(zone_id, level, surface_id)
        _location = Location(_transform, _routing_surface)
        log.debug(f"_get_location() -> '{_location}'")
        return _location

    @staticmethod
    def _process_location_data(location: Dict = None):
        log.debug(f"_process_location_data({location})")
        _default_levels = [0, ]
        _default_surface_id = 0
        _default_v = StdVector3(0, 0, 0)
        _default_q = StdQuaternion(1, 0, 0, 0)
        _default_q0000 = StdQuaternion(0, 0, 0, 0)  # 4d vector to randomize a quaternion
        if location is None:
            return _default_levels, _default_surface_id, _default_v, _default_q
        levels = location.get('Levels', _default_levels)
        surface_id = location.get('SurfaceId', _default_surface_id)
        _translation = StdVector3(*location.get('Translation', _default_v))
        _random_translation = StdVector3(*location.get('RandomTranslation', _default_v))
        translation: StdVector3 = _translation + _random_translation
        _orientation = StdQuaternion(*location.get('Orientation', _default_q))
        _random_orientation = StdQuaternion(*location.get('RandomOrientation', _default_q0000))
        orientation: StdQuaternion = _orientation.add(_random_orientation)  # normalized result. Don't use '+' here.
        log.debug(f"_process_location_data() -> {translation}, {orientation}")
        return levels, surface_id, translation, orientation

    @staticmethod
    def _buffs(sim_info: SimInfo, add: Tuple, remove: Tuple):
        log.debug(f"_buffs({sim_info}, {add}, {remove})")
        CommonBuffUtils.remove_buffs(sim_info, list(remove))  # Remove buffs which could affect 'add'
        CommonBuffUtils.add_buffs(sim_info, list(add))
        CommonBuffUtils.remove_buffs(sim_info, list(remove))

    @staticmethod
    def _traits(sim_info: SimInfo, add: Tuple, remove: Tuple):
        log.debug(f"_traits({sim_info}, {add}, {remove})")
        CommonTraitUtils.remove_traits(sim_info, list(remove))  # Remove traits which could affect 'add'
        CommonTraitUtils.add_traits(sim_info, list(add))
        CommonTraitUtils.remove_traits(sim_info, list(remove))

    @staticmethod
    def broken_add_locations(object_location: Location, sim_location: Location) -> Location:  # TODO xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        """
        Add the translation vectors of two locations. The 2nd vector will be added depending on the orientation of the 1st location.
         Used for the final location:
        * loc1.routing_surface / loc1.world_routing_surface
        * loc2.orientation
        """

        """
        o19.mypp2 x
        o19.pp.rot sim "(0,1,0,0)"
        o19.pp.move sim "(0, 0, 1.4)"
        """

        # Rotate the sim vector f(object-orientation)
        transform_2 = sim_location.transform
        v2 = transform_2.translation
        std_v = StdVector3(v2.x, v2.y, v2.z)
        transform_1 = object_location.transform
        o1 = transform_1.orientation
        std_q = StdQuaternion(o1.w, o1.x, o1.y, o1.z)
        std_v_r = std_q.rotate_vector(std_v)
        sim_vector = Vector3(std_v_r.x, std_v_r.y, std_v_r.z)

        obj_vector = transform_1.translation
        translation = Vector3(obj_vector.x + sim_vector.x, obj_vector.y + sim_vector.y, obj_vector.z + sim_vector.z)
        routing_surface = getattr(object_location, 'routing_surface', getattr(object_location, 'world_routing_surface'))  # routing_surface for the sim (same os object)
        orientation = transform_2.orientation  # orientation of the sim (not modified)
        transform = Transform(translation, orientation)
        return Location(transform, routing_surface)

    @staticmethod
    def broken__get_location(tra: StdVector3, rtra: StdVector3, rot: StdQuaternion, rrot: StdQuaternion, zone_id, level, surface_id) -> Location:
        log.debug(f"_get_location({tra}, {rtra}, {rot}, {rrot}, {zone_id}, {level}, {surface_id})")
        x = tra.x + random.random() * (rtra.x * 2) - rtra.x
        y = tra.y + random.random() * (rtra.y * 2) - rtra.y
        z = tra.z + random.random() * (rtra.z * 2) - rtra.z
        translation = Vector3(x, y, z)

        w = rot.w + random.random() * (rrot.w * 2) - rrot.w
        x = rot.x + random.random() * (rrot.x * 2) - rrot.x
        y = rot.y +  random.random() * (rrot.y * 2) - rrot.y
        z = rot.z + random.random() * (rrot.z * 2) - rrot.z
        q = StdQuaternion(w, x, y, z)  # wxyz order
        q = q.normalize()  # TS4 doesn't officially support this
        orientation = Quaternion(q.x, q.y, q.z, q.w)  # TS4 order

        _transform = Transform(translation, orientation)
        _routing_surface = SurfaceIdentifier(zone_id, level, surface_id)
        log.debug(f"_get_location() -> '{translation}, {orientation}'")
        return Location(_transform, _routing_surface)

    @staticmethod
    def _get_objects_by_name(objects: List, object_levels: List) -> Dict:
        log.debug(f"_get_objects_by_name({objects}, {object_levels})")
        rv = {}
        manager = services.object_manager()
        lot_filter = None
        for o in _all_objects_gen(manager, lot_filter):
            name = type(o).__name__
            if name in objects:
                _object_id = o.id
                _object: o = manager.get(_object_id)
                if CommonTypeUtils.is_sim_instance(_object):
                    continue
                if object_levels:
                    if _object.level not in object_levels:
                        continue
                rv.update({_object_id: _object})
        log.debug(f"_get_objects_by_name() -> '{rv}'")
        return rv

    @staticmethod
    @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), ZoneModifierService, ZoneModifierService._get_zone_modifiers_from_zone_data.__name__, handle_exceptions=False)
    def o19_x_get_zone_modifiers_from_zone_data(original, self, *args, **kwargs):
        try:
            lts = LotTraitStore()
            zone_modifiers: Set[Any] = original(self, *args, **kwargs)
            zone_modifiers.update(lts.add)
            for zm in lts.remove:
                try:
                    zone_modifiers.remove(zm)
                except:
                    pass
            return zone_modifiers
        except Exception as e:
            log.warn(f"{e}")
        return original(self, *args, **kwargs)

    @staticmethod
    def _lot_traits(add: Set, remove: Set):
        # access store ....
        log.debug(f"_lot_traits({add}, {remove})")
        lts = LotTraitStore()
        lts.add = add
        lts.remove = remove

    @staticmethod
    def _broadcasters(enable_broadcasters: Dict, disable_broadcasters: Dict):
        # {key.instance: (tuning, f"{instance_manager.TYPE.name}", f"{tuning.__name__}")}
        log.debug(f"_broadcasters({enable_broadcasters}, {disable_broadcasters})")
        for tuning_id, elements in enable_broadcasters.items():
            tuning = elements[0]
            setattr(tuning, 'allow_sims', True)
        for tuning_id, elements in disable_broadcasters.items():
            tuning = elements[0]
            setattr(tuning, 'allow_sims', False)


    @staticmethod
    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.si.runjob', '...',
    )
    def o19_read_cfg_cheat_init_bbb(output: CommonConsoleCommandOutput):
        try:
            job_id = "o19:doIt"
            callback = "schedule_it.jobs.jobs.Jobs.run"
            arguments = ["o19:doIt", ]
            _class_string, _function_name = callback.rsplit('.', 1)
            _module_name, _class_name = _class_string.rsplit('.', 1)
            _class = getattr(importlib.import_module(_module_name), _class_name)
            function = getattr(_class, _function_name)
            output(f"{function}({arguments})")
            function(*arguments)
            output("ok")
        except Exception as e:
            log.error(f"{e}")

    def o19_pp_rot_sim_object(self):
        object_location: Location = None
        obj_orientation: Quaternion = object_location.transform.orientation

        sim_location: Location = None
        sim_orientation: Quaternion = sim_location.transform.orientation
