import pandas as pd

def load_mag_contigs(samples, source, dfs, assembly, assembler, centr, binn, collection,):
    '''
    Loads info about one bin from MAGs, returns dataframe with contigs coverage info in samples.
    '''
    bin_wc = '/data5/bio/databases/fna/assembly/{assembler}/{dfs}/{ass}/imp__tmtic_def1/{collection}/bin_by_bin/{binn}/{binn}-contigs.names'
    taxa_wc = '/data5/bio/databases/fna/assembly/{assembler}/{dfs}/{ass}/imp__tmtic_def1/{collection}/bin_by_bin/{binn}/{binn}-bin_taxonomy.tab'

    # samples_for_source = meta.loc[meta['source'] == source]
    # samples_for_source = list(samples_for_source['fs_name'])
    T5_stats = bb_stats.get_cov_stats('/data6/bio/TFM/pipeline/datasets', 
                           dfs, 
                           samples,
                           'bwa', 
                           'imp__tmtic_def1', 
                           'assembly___{assembler}___{dfs}___{ass}___imp__tmtic_def1'.format(ass = assembly, assembler=assembler, dfs= dfs),
                          'final_contigs__1000')

    contigs_in_bin = pd.read_csv(bin_wc.format(binn = binn, ass = assembly,assembler=assembler, dfs= dfs, collection=collection), header=None)
    contigs_in_bin.columns = ['contig']
    merged = contigs_in_bin.merge(T5_stats, right_on='#ID', left_on='contig')
    merged = merged.drop(['#ID'], axis=1)

    merged['part'] = merged['Length']/merged['Length'].sum()
    for s in samples:
        merged['avg_on_per__'+s]=merged['Avg_fold__'+s]*merged['Covered_percent__'+s]
#             merged['avg_on_per_on_part__'+s]=merged['avg_on_per__'+s]*merged['part']/meta.loc[meta['fs_name'] == s]['reads'].item()
        # merged['avg_on_per_on_part__'+s]=merged['avg_on_per__'+s]*merged['part']/centr.loc[s]['bacteria'].item()
    
    return merged

def load_mags_info(meta, source, dfs, assembly, assembler, centr, collection, report_abundance_as = 'width'):
    '''
    Loads information about MAGs for specific assembly and samples, estimates abundance and returns a dataframe
     with index corresponding to bins and columns corresponding to abundance in samples. Can be transformed to OTU table by applying `df.T`
    '''
    mags = []
    
    # TODO replace with load_mag_contigs function
    bin_wc = '/data5/bio/databases/fna/assembly/{assembler}/{dfs}/{ass}/imp__tmtic_def1/{collection}/bin_by_bin/{binn}'
    taxa_wc = '/data5/bio/databases/fna/assembly/{assembler}/{dfs}/{ass}/imp__tmtic_def1/{collection}/bin_by_bin/{binn}/{binn}-bin_taxonomy.tab'
    
    bins  = [r.split('/')[-1] for r 
             in glob.glob(bin_wc.format(binn = '*', dfs=dfs, ass = assembly, assembler=assembler, collection=collection))]
    bin_wc += '/{binn}-contigs.names'

    samples_for_source = meta.loc[meta['source'] == source]
    samples_for_source = list(samples_for_source['fs_name'])
    T5_stats = bb_stats.get_cov_stats('/data6/bio/TFM/pipeline/datasets', 
                           dfs, 
                           samples_for_source,
                           'bwa', 
                           'imp__tmtic_def1', 
                           'assembly___{assembler}___{dfs}___{ass}___imp__tmtic_def1'.format(ass = assembly, assembler=assembler, dfs= dfs),
                          'final_contigs__1000')

    for b in bins:
        contigs_in_bin = pd.read_csv(bin_wc.format(binn = b, ass = assembly,assembler=assembler, dfs= dfs, collection=collection), header=None)
        contigs_in_bin.columns = ['contig']
        merged = contigs_in_bin.merge(T5_stats, right_on='#ID', left_on='contig')
        merged = merged.drop(['#ID'], axis=1)

        no_drop = ['contig', 'Length', 'Ref_GC',]

        merged['part'] = merged['Length']/merged['Length'].sum()
        for s in samples_for_source:
            no_drop.append('avg_on_per_on_part__'+s)
            no_drop.append('cov_width__'+s)

            merged['avg_on_per__'+s]=merged['Avg_fold__'+s]*merged['Covered_percent__'+s]
#             merged['avg_on_per_on_part__'+s]=merged['avg_on_per__'+s]*merged['part']/meta.loc[meta['fs_name'] == s]['reads'].item()
            if centr is not None:
                merged['avg_on_per_on_part__'+s]=merged['avg_on_per__'+s]*merged['part']/(centr.loc[s]['bacteria'].item() + centr.loc[s]['uncl'].item())
            merged['cov_width__'+s] = merged['Covered_percent__'+s]/100*merged['part']
        cols = list(merged.columns)    
        drop = list(set(cols) - set(no_drop))    

        merged = merged.drop(drop, axis=1)


        # taxa = pd.read_csv(taxa_wc.format(binn = b, ass = assembly), header=None, sep='\t')
        # taxa = taxa.fillna('Unknown')
        dd = {'Mag': b}
        for s in samples_for_source:
            if report_abundance_as == 'width':
                dd.update({s: merged['cov_width__'+s].sum()})
            else:
                dd.update({s: merged['avg_on_per_on_part__'+s].sum()})
        mags.append(dd)

    mags = pd.DataFrame(mags)
    mags.index = mags['Mag']
    mags = mags.drop(['Mag'], axis=1)
    return mags