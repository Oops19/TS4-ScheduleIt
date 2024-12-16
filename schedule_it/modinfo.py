#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2023 https://github.com/Oops19
#


from sims4communitylib.mod_support.common_mod_info import CommonModInfo


class ModInfo(CommonModInfo):
    _FILE_PATH: str = str(__file__)

    @property
    def _name(self) -> str:
        return 'ScheduleIt'

    @property
    def _author(self) -> str:
        return 'o19'

    @property
    def _base_namespace(self) -> str:
        return 'schedule_it'

    @property
    def _file_path(self) -> str:
        return ModInfo._FILE_PATH

    @property
    def _version(self) -> str:
        return '0.8.3'


'''
TODO v1.0.0 config/regions.txt and config.venues.txt need to use the new names (if used)
    
v0.8.3
    Code now compatible with TS4-Library 0.4.0 and replace Vanilla...(CommonEnum) imports.
v0.8.2
    Change BodyPart to BodyType
v0.8.1 
    Refactor
v0.8.0
    Initial beta version
v0.0.1
    Initial version
'''
