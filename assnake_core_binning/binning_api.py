import pandas as pd
import math, os

#from skbio.stats.composition import *

import loaders as assload
import anal as anal
import viz as viz

import glob

import yaml


class MagCollection:
    '''
    Wrapper class for working with collections of MAGs. 
    '''
    dfs = ''
    preprocs = ''
    samples = ''

    bins = []

    bins_wc = '/data5/bio/databases/fna/assembly/mh__def/{dfs}/{samples}/imp__tmtic_def1/{collection}/bin_by_bin/{binn}'
    taxa_wc = '/data5/bio/databases/fna/assembly/mh__def/{dfs}/{samples}/imp__tmtic_def1/{collection}/bin_by_bin/{binn}/{binn}-bin_taxonomy.tab'
    summary_wc = '/data5/bio/databases/fna/assembly/mh__def/{dfs}/{samples}/imp__tmtic_def1/{collection}/bins_summary.txt'
    checkm_wc = '/data5/bio/databases/fna/assembly/{assembler}/{dfs}/{samples}/imp__tmtic_def1/{collection}/checkm/storage/bin_stats_ext.tsv'

    def __init__(self, dfs, preprocs, samples, collection, assembler):
        self.dfs = dfs
        self.preprocs = preprocs,
        self.samples = samples
        self.collection = collection
        self.assembler = assembler
        bins  = [r.split('/')[-1] for r 
             in glob.glob(self.bins_wc.format(binn = '*', dfs = dfs, samples = self.samples, collection=collection))]

        mags = []
        for b in bins:
            try:
                taxa = pd.read_csv(self.taxa_wc.format(binn = b, dfs = dfs, samples = self.samples, collection=collection), header=None, sep='\t')
                taxa = taxa.fillna('Unknown')
                dd = {"Bin": b,
                'Taxa': list(taxa[0])[0].split('-')[0] + '__' + list(taxa[1])[0]
                }
                mags.append(dd)
            except:
                pass
                print("Can't load: ", self.taxa_wc.format(binn = b, dfs = dfs, samples = self.samples, collection=collection))
            
            # mags.append(dd)
        self.bins = pd.DataFrame(mags)

        
        try:
            self.summary = pd.read_csv(self.summary_wc.format(samples = self.samples, dfs = dfs, collection=collection), sep='\t')
            self.checkm = self.get_bins()
            subcheckm = self.checkm[['Bin', 'Completeness', 'Contamination', 'marker lineage']]
            self.summary = self.summary.merge(subcheckm, left_on = 'bins', right_on = 'Bin')
            self.summary = self.summary.drop(['Bin'], axis=1)
            self.summary = self.summary.merge(self.bins, left_on = 'bins', right_on = 'Bin')
            self.summary = self.summary.drop(['bins'], axis=1)
        except:
            pass
        

    def filter_by_comp_cont(self, completeness, contamination):
        summ = self.summary.loc[self.summary['Completeness'] > completeness]
        summ = summ.loc[summ['Contamination'] < contamination]
        return summ

    def __repr__(self):
        return str({
            'dfs': self.dfs,
            'samples': self.samples,
            'preprocs': self.preprocs,
            'bins': self.bins,
        })

    def get_bins(self):
        bins = []
        with open(self.checkm_wc.format(dfs = self.dfs, samples = self.samples, collection=self.collection,assembler=self.assembler), 'r') as checkm: 
            for line in checkm:
                dic=eval(line.strip().split("\t")[1])
                dic.update({'Bin': line.strip().split("\t")[0]})
                bins.append(dic)
        bbb = pd.DataFrame(bins)
        return bbb


class Mag:
    def __init__(self, dfs, preprocs, samples, collection, binn):
        names_wc = '/data5/bio/databases/fna/assembly/mh__def/FHM/{samples}/imp__tmtic_def1/{collection}/bin_by_bin/{binn}/{binn}-contigs.names'

        with open(names_wc.format(binn = binn, samples = samples, collection=collection), 'r') as names:
            self.contigs = [c.strip() for c in names.readlines()]

