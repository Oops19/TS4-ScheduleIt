#
# LICENSE
# https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2023 https://github.com/Oops19
#


## TODO move to T4Lib

from typing import Any, Union

import services
from interactions.context import InteractionContext
from interactions.priority import Priority
from schedule_it.modinfo import ModInfo
from sims.sim import Sim
from sims4.resources import Types as ResourceType
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)
log.enable()


class OldJobInteractions:

    def _push_super_affordance(self, sim: Sim, interaction, target: Union[Sim, Any] = None, pose_name: str = None, _connection = None,
                               priority: Priority = Priority.High, interaction_context: InteractionContext = InteractionContext.SOURCE_SCRIPT, **kwargs) -> bool:
        """
        :param sim: The sim
        :param sim: The interaction
        :param target: The target sim or object. Defaults to 'sim'
        :param pose_name: The pose to play, if any.
        :param _connection: None
        :param priority: Priority.Low / High / Critical
        :param interaction_context: InteractionContext.SOURCE_SCRIPT / SOURCE_REACTION / SOURCE_AUTONOMY / SOURCE_PIE_MENU

        """
        log.debug(f"_push_super_affordance({sim},{interaction}, {target}, {pose_name}, {kwargs})")
        if target is None:
            target = sim
        client = services.client_manager().get(_connection)
        context = InteractionContext(sim, interaction_context, priority, client=client, pick=None)
        return sim.push_super_affordance(super_affordance=interaction, target=target, context=context, pose_name=pose_name, **kwargs)

    def run_pose(self, sim: Sim, pose_name: str, **kwargs):
        log.debug(f"run_pose({sim}, {pose_name}, {kwargs})")

        interaction_manager = services.get_instance_manager(ResourceType.INTERACTION)
        interaction_id = 16579329647886045878  # <I c="ScheduleItPoseInteraction" i="interaction" m="schedule_it" n="o19:pose_interaction" s="16579329647886045878"><!-- E6159C79445992B6 -->
        interaction = interaction_manager.get(interaction_id)
        return self._push_super_affordance(sim, interaction, pose_name=pose_name, **kwargs)

    def run_interaction(self, sim: Sim, interaction_id: int, target: Union[Sim, Any] = None, **kwargs):
        log.debug(f"run_interaction({sim}, {interaction_id}, {target}, {kwargs})")

        interaction_manager = services.get_instance_manager(ResourceType.INTERACTION)
        interaction = interaction_manager.get(interaction_id)
        return self._push_super_affordance(sim, interaction, target=target, **kwargs)
