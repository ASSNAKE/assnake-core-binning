CHECKM = config['CHECKM']

rule check_m:
    input:
        # TODO replace with files
        bin_folder = '{fs_prefix}/{df}/binning/metabat2/{df}/{sample_set}/final_contigs__{mod}/bins'
    output:
        done = '{fs_prefix}/{df}/binning/metabat2/{df}/{sample_set}/final_contigs__{mod}/checkm.done'
    params:
        wd    = '{fs_prefix}/{df}/binning/metabat2/{df}/{sample_set}/final_contigs__{mod}/checkm'
    log:           '{fs_prefix}/{df}/binning/metabat2/{df}/{sample_set}/final_contigs__{mod}checkm-log.txt'
    benchmark:      '{fs_prefix}/{df}/binning/metabat2/{df}/{sample_set}/final_contigs__{mod}checkm-benchmark.txt'
    threads: 20
    conda: 'checkm_env.yaml'
    shell: ('''echo {CHECKM} | checkm data setRoot {CHECKM}; \n
        (checkm lineage_wf -t {threads} -x fa {input.bin_folder} {params.wd}) >{log} 2>&1; \n
        touch {output.done}''')




rule check_m_collection:
    input:
        exported = os.path.join(fna_db_dir, 'assembly/mh__{params}/{df}/{samples}/final_contigs__{mod}/{collection}/all_bins.done')
    output:
        done =  os.path.join(fna_db_dir, 'assembly/mh__{params}/{df}/{samples}/final_contigs__{mod}/{collection}/checkm.done')
    params:
        wd    = os.path.join(fna_db_dir, 'assembly/mh__{params}/{df}/{samples}/final_contigs__{mod}/{collection}/checkm'),
        bin_folder = os.path.join(fna_db_dir, 'assembly/mh__{params}/{df}/{samples}/final_contigs__{mod}/{collection}/all_bins/'), 
    log:          os.path.join(fna_db_dir, 'assembly/mh__{params}/{df}/{samples}/final_contigs__{mod}/{collection}/checkm-log.txt')
    benchmark:      os.path.join(fna_db_dir, 'assembly/mh__{params}/{df}/{samples}/final_contigs__{mod}/{collection}/checkm-benchmark.txt')
    threads: 24
    conda: 'checkm_env.yaml'
    shell: ('''echo {CHECKM} | checkm data setRoot {CHECKM}; \n
        (checkm lineage_wf -t {threads} -x fa {params.bin_folder} {params.wd}) >{log} 2>&1; \n
        touch {output.done}''')