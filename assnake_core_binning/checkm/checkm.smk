CHECKM = config['CHECKM']

rule check_m:
    input:
        binner_finished = '{fs_prefix}/{df}/binning/metabat2/{df}/{sample_set}/final_contigs__{mod}/metabat2.done'
    output:
        done = '{fs_prefix}/{df}/binning/metabat2/{df}/{sample_set}/final_contigs__{mod}/checkm.done'
    params:
        wd    = '{fs_prefix}/{df}/binning/metabat2/{df}/{sample_set}/final_contigs__{mod}/checkm',
        bin_folder = '{fs_prefix}/{df}/binning/metabat2/{df}/{sample_set}/final_contigs__{mod}/bins',
    log:           '{fs_prefix}/{df}/binning/metabat2/{df}/{sample_set}/final_contigs__{mod}checkm-log.txt'
    benchmark:      '{fs_prefix}/{df}/binning/metabat2/{df}/{sample_set}/final_contigs__{mod}checkm-benchmark.txt'
    threads: 10
    conda: 'checkm_env.yaml'
    shell: ('''(checkm lineage_wf -t {threads} -x fa {params.bin_folder} {params.wd}) >{log} 2>&1; \n
        touch {output.done}''')

# echo {CHECKM} | checkm data setRoot {CHECKM}; \n