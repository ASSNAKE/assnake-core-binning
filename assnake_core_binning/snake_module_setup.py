import os
import assnake
# from assnake_core_assembly.megahit.cmd_megahit import megahit_invocation
from assnake.utils import read_yaml

this_dir = os.path.dirname(os.path.abspath(__file__))
snake_module = assnake.SnakeModule(name = 'assnake-core-binning', 
                           install_dir = this_dir,
                           snakefiles = ['./metabat2/metabat2.smk', './checkm/checkm.smk'],
                           invocation_commands = [],
                           wc_configs = []
                            )
