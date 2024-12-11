#
# LICENSE
# https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2023 https://github.com/Oops19
#


import services


from crafting.crafting_process import CraftingProcess
from crafting.recipe import Phase
from interactions.base.super_interaction import SuperInteraction

from interactions.context import InteractionContext, QueueInsertStrategy
from interactions.priority import Priority
from schedule_it.modinfo import ModInfo

from sims4.resources import Types as ResourceType
from sims.sim import Sim
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

from sims.sim import Sim
from routing import SurfaceType, SurfaceIdentifier
# noinspection PyUnresolvedReferences
from sims4.math import Vector3, Quaternion, Transform, Location

class MyPosePlayer:

    @staticmethod
    @CommonConsoleCommand(
            ModInfo.get_identity(), 'o19.mypp', '...',
        command_arguments=(
                CommonConsoleCommandArgument('pose_name', 'str', 'a random name', is_optional=False),
        )
    )
    def o19_cheat_init_bbb(output: CommonConsoleCommandOutput, pose_name: str):
        try:
            if pose_name == "-":
                pose_name = 'Grey Naya:PosePack_201911050602337560_set_1'
                pose_name = 'FEMDOMANIA:PosePack_202201302332405072_set_1'

            output(f"Pose name: {pose_name}")
            _connection = None
            # target_sim_id = 425327441346477632  # Nina Kaliente
            # target_sim: Sim = CommonSimUtils.get_sim_instance(target_sim_id)
            target_sim: Sim = CommonSimUtils.get_active_sim()
            sim = CommonSimUtils.get_active_sim()

            interaction_manager = services.get_instance_manager(ResourceType.INTERACTION)

            interaction_id = 12880964001135365186  # <I c="PoseInteraction" i="interaction" m="poseplayer" n="andrew:pose_interaction" s="12880964001135365186">
            interaction_id = 16579329647886045878  # <I c="PoseInteraction" i="interaction" m="schedule_it" n="o19:pose_interaction" s="16579329647886045878"><!-- E6159C79445992B6 -->
            interaction_id = 12880964001135365186  #  n="andrew:pose_interaction"
            interaction = interaction_manager.get(interaction_id)

            client = services.client_manager().get(_connection)
            context = InteractionContext(sim, InteractionContext.SOURCE_PIE_MENU, Priority.High, client=client, pick=None)
            result = sim.push_super_affordance(super_affordance=interaction, target=target_sim, context=context, pose_name=pose_name)
            if not result:
                output(f'Failed to push: {result}')

            output(f"ok")
        except Exception as e:
            output(f"Error {e}")


    @staticmethod
    @CommonConsoleCommand(
            ModInfo.get_identity(), 'o19.myint', '...',
        command_arguments=(
                CommonConsoleCommandArgument('pose_name', 'str', 'a random name', is_optional=False),
        )
    )
    def o19_cheat_init_bbb(output: CommonConsoleCommandOutput, pose_name: str):
        try:
            _connection = None
            sim = CommonSimUtils.get_active_sim()
            target_obj = CommonObjectUtils.get_game_object(409565074712297982)  # Kritical:PracticalSexArcade-objectTuning1

            interaction_manager = services.get_instance_manager(ResourceType.INTERACTION)

            interaction_id = 14120797559332646387  # Kritical:PracticalSexArcade-InteractionInsideIdle1(1)
            interaction = interaction_manager.get(interaction_id)

            # interaction.affordance.immediate = True
            client = services.client_manager().get(_connection)
            context = InteractionContext(sim, InteractionContext.SOURCE_PIE_MENU, Priority.High, client=client, pick=None) # , insert_strategy=QueueInsertStrategy.FIRST)
            result = sim.push_super_affordance(super_affordance=interaction, target=target_obj, context=context)
            if not result:
                output(f'Failed to push: {result}')

            output(f"ok")
        except Exception as e:
            output(f"Error {e}")



    @staticmethod
    @CommonConsoleCommand(
            ModInfo.get_identity(), 'o19.mypp2', '...',
        command_arguments=(
                CommonConsoleCommandArgument('pose_name', 'str', 'a random name', is_optional=False),
        )
    )
    def o19_cheat_init_bbb(output: CommonConsoleCommandOutput, pose_name: str):
        try:
            _connection = None
            sim = CommonSimUtils.get_active_sim()
            game_object = CommonObjectUtils.get_game_object(409565074712297982)  # object_sculpture

            # Teleport sim into object
            location = game_object._location
            '''
            level = getattr(game_object, 'level', 0)
            transform = location.transform
            position = transform.translation
            zone_id = services.current_zone_id()
            orientation = Quaternion(0, 0, 0, 1)
            surface = int(SurfaceType.SURFACETYPE_WORLD)
            _transform = Transform(position, orientation)
            _routing_surface = SurfaceIdentifier(zone_id, level, surface)
            location = Location(_transform, _routing_surface)
            '''
            sim.location = location


            interaction_manager = services.get_instance_manager(ResourceType.INTERACTION)

            interaction_id = 12880964001135365186  # <I c="PoseInteraction" i="interaction" m="poseplayer" n="andrew:pose_interaction" s="12880964001135365186">
            # interaction_id = 16579329647886045878  # <I c="PoseInteraction" i="interaction" m="schedule_it" n="o19:pose_interaction" s="16579329647886045878"><!-- E6159C79445992B6 -->
            interaction = interaction_manager.get(interaction_id)

            pose_name = "Kritical:PosePack_202008080858060484_set_1"

            client = services.client_manager().get(_connection)
            context = InteractionContext(sim, InteractionContext.SOURCE_PIE_MENU, Priority.High, client=client, pick=None) # , insert_strategy=QueueInsertStrategy.FIRST)
            result = sim.push_super_affordance(super_affordance=interaction, target=game_object, context=context, pose_name=pose_name)
            if not result:
                output(f'Failed to push: {result}')

            output(f"ok")
        except Exception as e:
            output(f"Error {e}")

    @staticmethod
    @CommonConsoleCommand(
            ModInfo.get_identity(), 'o19.myint2', '...',
    )
    def o19_cheat_init_bbb(output: CommonConsoleCommandOutput):
        try:
            _connection = None
            sim = CommonSimUtils.get_active_sim()
            target_obj = CommonObjectUtils.get_game_object(425327441346203053)  # 'Stove Minor LOW 01'

            interaction_manager = services.get_instance_manager(ResourceType.INTERACTION)

            interaction_id = 13395  # fridge_CreateTray
            interaction = interaction_manager.get(interaction_id)

            recipe_Food_Homestyle_GrilledCheese_Large_id = 15763
            recipe_manager = services.get_instance_manager(ResourceType.RECIPE)
            recipe = recipe_manager.get(recipe_Food_Homestyle_GrilledCheese_Large_id)
            # recipe = CommonResourceUtils.load_instance(Types.RECIPE, recipe_Food_Homestyle_GrilledCheese_Large_id)

            phaseSimple_Food_FryingPan_Bread = 15622  # phaseSimple_Food_FryingPan_Bread
            phaseSimple_IngredientsTray_Bread = 15642  # phaseSimple_IngredientsTray_Bread <L n="_first_phases"><E>GetIngredientTray</E>

            p = Phase(recipe=recipe, phase_id=phaseSimple_IngredientsTray_Bread)

            cp = CraftingProcess(crafter=sim, recipe=recipe, bucks_cost=13)

            # <T n="crafting_type_requirement">15545<!--craftingObjectType_Fridge--></T>

            # interaction.affordance.immediate = True
            client = services.client_manager().get(_connection)
            context = InteractionContext(sim, InteractionContext.SOURCE_PIE_MENU, Priority.High, client=client, pick=None) # , insert_strategy=QueueInsertStrategy.FIRST)
            result = sim.push_super_affordance(super_affordance=interaction, target=target_obj, context=context, phase=p, crafting_process=cp, ingredient_cost_only=True, costs=False)
            if not result:
                output(f'Failed to push: {result}')

            output(f"ok")
        except Exception as e:
            output(f"Error {e}")
