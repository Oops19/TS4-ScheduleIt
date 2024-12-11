#
# LICENSE
# https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2023 https://github.com/Oops19
#
import traceback

import services

from interactions.context import InteractionContext, QueueInsertStrategy
from interactions.priority import Priority
from objects.components import ComponentContainer
from objects.components.statistic_component import HasStatisticComponent
from schedule_it.modinfo import ModInfo

from sims4.resources import Types as ResourceType
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.objects.common_object_utils import CommonObjectUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

from sims.sim import Sim
# noinspection PyUnresolvedReferences
from sims4.math import Vector3, Quaternion, Transform, Location
from socials.group import SocialGroup
from ts4lib.utils.interaction.enqueue_interaction import EnqueueInteraction


class ScheduleItPosePlayer:

    @staticmethod
    @CommonConsoleCommand(
            ModInfo.get_identity(), 'o19.si.pp', '...',
    )
    def o19_cheat_init_pp1(output: CommonConsoleCommandOutput):
        try:
            clip_x = 'FEMDOMANIA:PosePack_202201302332405072_set_1'
            clip_y = 'FEMDOMANIA:PosePack_202201302332405072_set_2'
            clip_object = 'FEMDOMANIA:PosePack_202103152243374038_set_3'  # DOUBLE_BED
            clip_prop_1 = 'FEMDOMANIA:PosePack_202103152243374038_set_4'  # 145433
            clip_prop_2 = 'FEMDOMANIA:PosePack_202103152243374038_set_5'  # 145433
            clip_prop_3 = 'FEMDOMANIA:PosePack_202103152243374038_set_6'  # 145433

            output(f"Pose name: {clip_x}")
            _connection = None
            target_sim: Sim = CommonSimUtils.get_active_sim()
            sim = CommonSimUtils.get_active_sim()
            # Sim/Object: 'Dina#Caliente' (425327441346477631)
            # Sim/Object: 'Bebe#Rexha' (425327441345118999)
            # Sim/Object: 'object_bedDoubleCLLeather_01' (425327441346203022)
            sim_dina = CommonSimUtils.get_sim_instance(425327441346477631)
            sim_bebe = CommonSimUtils.get_sim_instance(425327441345118999)
            bed = CommonObjectUtils.get_game_object(425327441346203022)

            interaction_manager = services.get_instance_manager(ResourceType.INTERACTION)
            interaction_id = 16579329647886045878  # <I c="ScheduleItPoseInteraction" i="interaction" m="schedule_it" n="o19:pose_interaction" s="16579329647886045878"><!-- E6159C79445992B6 -->

            interaction = interaction_manager.get(interaction_id)
            output(f"{interaction}")

            client = services.client_manager().get(_connection)
            context = InteractionContext(sim, InteractionContext.SOURCE_SCRIPT, Priority.High, client=client, pick=None)
            result = sim.push_super_affordance(super_affordance=interaction, target=sim, context=context, x=sim, pose_name=clip_x, pose_clip=clip_x, clip_x=clip_x)  # y=sim_bebe clip_y=clip_y, object=bed, clip_object=clip_object
            if not result:
                output(f'Failed to push: {result}')

            output(f"ok")
        except Exception as e:
            output(f"Error {e}")

    # Action towards object
    @staticmethod
    @CommonConsoleCommand(
            ModInfo.get_identity(), 'o19.si.pp2', '...',
    )
    def o19_cheat_init_pp2(output: CommonConsoleCommandOutput):
        try:
            sim = CommonSimUtils.get_active_sim()
            output(f"sim {sim}")

            # sim_bebe = CommonSimUtils.get_sim_instance(425327441345118999)
            # output(f"sim_bebe {sim_bebe}")

            interaction_manager = services.get_instance_manager(ResourceType.INTERACTION)
            interaction_id = 14427  # toilet-use-sitting (14427)
            interaction = interaction_manager.get(interaction_id)
            output(f"interaction {interaction}")

            object_id = 425327441346203122  # Sim/Object: 'object_toiletC_02' (425327441346203122) at '409.288/151.000/325.621' '0.000/0.000/0.000/1.000'
            game_object = CommonObjectUtils.get_game_object(object_id)

            eq = EnqueueInteraction()
            result = eq.run_interaction(sim, interaction_id, target=game_object)

            # _connection = None
            # client = services.client_manager().get(_connection)
            # context = InteractionContext(sim, InteractionContext.SOURCE_SCRIPT, Priority.High, client=client, pick=None)
            # result = sim.push_super_affordance(super_affordance=interaction, target=game_object, context=context)
            if not result:
                output(f'Failed to push: {result}')

            output(f"ok")
        except Exception as e:
            output(f"Error {e}")

    # Action towards sim
    @staticmethod
    @CommonConsoleCommand(
            ModInfo.get_identity(), 'o19.si.pp3', '...',
    )
    def o19_cheat_init_pp3(output: CommonConsoleCommandOutput):
        try:
            sim = CommonSimUtils.get_active_sim()
            output(f"sim {sim}")

            sim_bebe = CommonSimUtils.get_sim_instance(425327441345118999)
            output(f"sim_bebe {sim_bebe}")

            interaction_manager = services.get_instance_manager(ResourceType.INTERACTION)
            interaction_id = 13991  # n="sim_BeAffectionate" s="13991">
            interaction = interaction_manager.get(interaction_id)
            output(f"interaction {interaction}")

            _connection = None
            client = services.client_manager().get(_connection)
            context = InteractionContext(sim, InteractionContext.SOURCE_SCRIPT, Priority.High, client=client, pick=None)
            result = sim.push_super_affordance(super_affordance=interaction, target=sim_bebe, context=context)
            if not result:
                output(f'Failed to push: {result}')

            output(f"ok")
        except Exception as e:
            output(f"Error {e}")


    # BROKEN
    # Action towards sim
    @staticmethod
    @CommonConsoleCommand(
            ModInfo.get_identity(), 'o19.si.pp3xx', '...',
    )
    def o19_cheat_init_pp3xx(output: CommonConsoleCommandOutput):
        try:
            interaction_manager = services.get_instance_manager(ResourceType.INTERACTION)
            interaction_id = 320160  # m="interactions.social.social_mixer_interaction" n="socials_Friendly_CrossAge_Interactions_familyKiss_targeted_alwaysOn_CTYAE_to_CTYAE" s="320160">
            # # mixer_social_ComplimentOutfit_targeted_Friendly_alwaysOn_skills (37013),
            # mixer_social_TellDirtyJoke_targeted_funny_emotionSpecific (25893),
            # interaction_id = 16722869358278951099
            interaction = interaction_manager.get(interaction_id)
            output(f"interaction {interaction}")
            super_interaction = interaction.super_interaction
            output(f"super_interaction {super_interaction}")
            _super_interaction = interaction._super_interaction
            output(f"_super_interaction {_super_interaction}")

            _connection = None
            sim = CommonSimUtils.get_active_sim()
            # social_group = sim.get_main_group()
            # output(f"social_group {social_group}")
            # interaction.social_group = social_group  # fails even if not None
            # output(f"sim._social_groups {sim._social_groups}")
            output(f"sim {sim}")

            sim_bebe = CommonSimUtils.get_sim_instance(425327441345118999)
            output(f"sim_bebe {sim_bebe}")
            # output(f"sim_bebe.social_group {sim_bebe._social_groups}")

            hsc = HasStatisticComponent()
            cc = ComponentContainer()
            super_interaction.context.sim = sim
            sc = SocialGroup(cc, hsc, si=super_interaction, target_sim=sim_bebe)
            output(f"sc {sc}")

            sim._social_groups = sc
            sim_bebe._social_groups = sc
            interaction.social_groups = sc

            client = services.client_manager().get(_connection)
            context = InteractionContext(sim, InteractionContext.SOURCE_SCRIPT, Priority.High, client=client, pick=None)
            result = sim.push_super_affordance(super_affordance=interaction, target=sim_bebe, context=context, si=super_interaction, skip_safe_tests=True, skip_test_on_execute=True)
            if not result:
                output(f'Failed to push: {result}')

            output(f"ok")
        except Exception as e:
            output(f"Error {e}")
            output(f"Error {traceback.format_exc()}")