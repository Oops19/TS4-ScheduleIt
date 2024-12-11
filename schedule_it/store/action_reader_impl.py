#
# LICENSE
# https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2023 https://github.com/Oops19
#


from typing import Dict, Any

from ts4lib.utils.config.reader_interface import ReaderInterface
from ts4lib.utils.tuning_helper import TuningHelper


class ActionReaderImpl(ReaderInterface):
    def __init__(self, base_namespace: str, files: Dict):
        super().__init__(base_namespace, files)
        self.th = TuningHelper()

    def parse_definitions(self, file: str, definitions: Any) -> Any:
        return definitions
