import os
import assnake
# from assnake_core_assembly.megahit.cmd_megahit import megahit_invocation
from assnake.utils import read_yaml
from assnake_core_binning.checkm.invocation_commands import chekcm_invocation
from assnake_core_binning.metabat2.invocation_commands import metabat2_invocation

this_dir = os.path.dirname(os.path.abspath(__file__))
snake_module = assnake.SnakeModule(name = 'assnake-core-binning', 
                           install_dir = this_dir,
                           snakefiles = ['./metabat2/metabat2.smk', './checkm/checkm.smk'],
                           invocation_commands = [chekcm_invocation, metabat2_invocation],
                           wc_configs = []
                            )
