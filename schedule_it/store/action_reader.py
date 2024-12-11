#
# LICENSE
# https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2023 https://github.com/Oops19
#


from schedule_it.store.action_reader_impl import ActionReaderImpl
from schedule_it.store.action_store import ActionStore
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from schedule_it.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from ts4lib.utils.config.store_parsed import StoreParsed
from ts4lib.utils.config.store_raw import StoreRaw

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), ModInfo.get_identity().name)
log.enable()


class ActionReader:
    @staticmethod
    def read_config():
        try:
            files = {'actions.txt': False, }
            base_namespace = ModInfo.get_identity().base_namespace
            ar = ActionReaderImpl(base_namespace, files)
            ar.read_files()
            file = list(files.keys())[0]
            file_id = ar.file_id(file)
            store_raw = StoreRaw()
            log.debug(f"RAW {file} = {getattr(store_raw, file_id, None)}")
            store_parsed = StoreParsed()
            log.debug(f"RAW {file} = {getattr(store_parsed, file_id, None)}")

            action_store = ActionStore()
            action_store.actions = getattr(store_parsed, file_id).copy()
        except Exception as e:
            log.error(f"{e}")

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity().name)
    def handle_event(event_data: S4CLZoneLateLoadEvent):
        ActionReader().read_config()

    @staticmethod
    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.si.read_actions', '...',)
    def o19_cheat_read_actions(output: CommonConsoleCommandOutput):
        ActionReader().read_config()
        output(f"ok")