#
# LICENSE
# https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2023 https://github.com/Oops19
#


from ts4lib.utils.singleton import Singleton


class ConfigType(object, metaclass=Singleton):
    def __init__(self):
        # These types will not be parsed: 'animations', 'zones',
        # True/False - Use cache
        self.types = {'sims.txt': False, 'traits.txt': True, 'buffs.txt': True,
                      'interactions.txt': True, 'animations.txt': True,
                      'worlds.txt': True,'venues.txt': True, 'regions.txt': True, 'zones.txt': True,
                      'objects.txt': True, 'lot_traits.txt': True, 'broadcasters.txt': True,
                      # no use
                      'statistics.txt': False, 'snippets.txt': False, 'neighbourhoods.txt': False,
                      # 'vanilla_outfits.txt': True, 'outfits.txt': True, 'outfit_sequences.txt': True,
                      }

    @staticmethod
    def deprecated_file_id(type_file_name) -> str:
        return f"{type_file_name.split('.', 1)[0]}"
