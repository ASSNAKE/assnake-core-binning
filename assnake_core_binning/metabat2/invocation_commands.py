import click, glob, os
import assnake.api.loaders
import assnake
from assnake.cli.cli_utils import sample_set_construction_options, add_options, generic_command_individual_samples,\
    generate_result_list, generic_command_dict_of_sample_sets, prepare_sample_set_tsv_and_get_results


@click.command('metabat2', short_help='Bin contigs with Metabat2')
@add_options(sample_set_construction_options)

@click.option('--min-len','-l', help='Minimum length of contigs', default=1000)
@click.option('--overwrite', is_flag=True, help='Overwrite existing sample_set.tsv files', default=False)

@click.pass_obj

def metabat2_invocation(config, min_len,overwrite, **kwargs):
    # load sample sets     
    sample_sets = generic_command_dict_of_sample_sets(config,   **kwargs)

    sample_set_dir_wc = '{fs_prefix}/{df}/assembly/{sample_set}/'
    result_wc = '{fs_prefix}/{df}/binning/metabat2/{df}/{sample_set}/final_contigs__{mod}/metabat2.done'
    res_list = prepare_sample_set_tsv_and_get_results(sample_set_dir_wc, result_wc, df = kwargs['df'], sample_sets = sample_sets, mod = min_len, overwrite = overwrite)

    config['requests'] += res_list

