import json
import os
import re
import sys
import urllib.request, urllib.parse, urllib.error
import traceback
from datetime import datetime
import time
import pickle
import pickle
import subprocess
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from xml.dom.minidom import parseString
from bs4 import BeautifulSoup
#AUTO-load classifiers
#a trick to get the current module
_modname = globals()['__name__']
_this_mod = sys.modules[_modname]

_ppath = "/".join(_this_mod.__file__.split("/")[:-1])

from django.utils.encoding import smart_str

import env
models = env.models

import pubmed
import getGEOSamples_byType_gse
import scrna_parser_from_gse  


def _parse_a_field(description_dict, a_field, DCmodel, max_create_length=100, new=False):
    if  not description_dict.get(a_field, None):
        return None
    if len(description_dict.get(a_field, "")) > 0:
        if DCmodel in [models.CellTypes]: #remove '-' when match cell types, like T-cells > T cells
            description_dict_new = {}
            for v in list(description_dict.keys()):
                description_dict_new[v] = description_dict[v].replace('-', ' ')
            description_dict = description_dict_new  
        result_searched_by_name = sorted(DCmodel.objects.extra(
            where={"%s REGEXP CONCAT('([^a-zA-Z0-9]|^)', `name`, '([^a-rt-zA-RT-Z0-9]|$)')"},
                                  params=[description_dict[a_field]]),
            key=lambda o: len(o.name),
            reverse=True)

        if result_searched_by_name and len(result_searched_by_name[0].name.strip()) > 0:
            return result_searched_by_name[0]


    if new and (len(description_dict.get(a_field, "")) > 0) and (len(description_dict.get(a_field, "")) <= max_create_length):
        #return description_dict[a_field]
        if DCmodel in [models.CellLines, models.CellTypes, models.TissueTypes]: # these three will check wheather they appare in each other
            return description_dict[a_field]
        else:
            # ret, created = DCmodel.objects.get_or_create(name=description_dict[a_field])
            # if created:
            #     ret.status = 'new'
            return description_dict[a_field]


    return None

def _parse_fields(description_dict, strict_fields, greedy_fields, DCmodel, greedy_length=100):
    for sf in strict_fields:
        ret = _parse_a_field(description_dict, sf, DCmodel, greedy_length, new=False)
        if ret:
            return ret

            
    for gf in greedy_fields:
        ret = _parse_a_field(description_dict, gf, DCmodel, greedy_length, new=True)
        if ret:
            return ret

    tmp = {}
    for x in list(description_dict.keys()): # using all description to parse information
        if x not in ['antibody', 'chip_antibody', 'last update date', 'release date']:
            tmp[x] = description_dict[x]
    characteristics = {'characteristics':' '.join(list(tmp.values()))}
    ret = _parse_a_field(characteristics, 'characteristics', DCmodel, greedy_length, new = False)
    if ret:
        return ret

    if DCmodel in [models.CellLines]: # search cell line by pubic database information
        ret = geo_parser_newVersion.search_cellline_from_out(characteristics, 'characteristics')
        if ret:
            if ret and (str(ret) not in ['OF', 'IP']):
                return ret
    return None

def parseCellType(description_dict):
    return _parse_fields(description_dict,
                         ['cell type', 'cell lineage', 'cell', 'cell line', 'source name', 'cell description', 'title', ],
                         ['cell type'],
                         models.CellTypes)


def parseCellPop(description_dict):
    return _parse_fields(description_dict, ['cell', 'source name', 'cell description', 'title', 'cell type', 'cell lineage'], [], models.CellPops)


def parseTissue(description_dict):
    return _parse_fields(description_dict,
                         ['tissue', 'tissue type', 'tissue depot', 'source name', 'cell description', 'title', 'cell type', 'cell lineage','cell', 'cell line'],
                         ['tissue', 'tissue type'],
                         models.TissueTypes)



def parseDisease(description_dict):
    return _parse_fields(description_dict,
                         ['disease', 'tumor stage', 'cell karotype', 'source name', 'title'],
                         ['disease'],
                         models.DiseaseStates)


def parseReleaseTime(description_dict):
    # a trick to convert time string into a datetime object
    time_struct = time.strptime(description_dict["release date"], "%Y-%m-%d")
    return datetime.fromtimestamp(time.mktime(time_struct))


def search_between_table(description_dict, strict_fields, serious_fields, DCmodel):
    for sf in strict_fields:
        sea = _parse_a_field(description_dict, sf, DCmodel, 100, new=False)
        if sea:
            return sea
    tmp = {}
    for k in list(description_dict.keys()):
        if k not in ['antibody', 'chip_antibody', 'last update date', 'release date']:
            tmp[k] = description_dict[k]
    characteristics = {'characteristics':' '.join(list(tmp.values()))}
    sea = _parse_a_field(characteristics, 'characteristics', DCmodel, 100, new = False)
    if sea:
        return sea
    if DCmodel in [models.CellTypes]:
        """try metamap if no cell type"""
        feature = characteristics['characteristics'].replace('(', ' ').replace(')', ' ')
        try:
            content = subprocess.getoutput('echo "%s" | metamap -y -I '%(feature))
            content = [x for x in content.split('\n') if x.endswith('[Cell]')]
            if content:
                proCell = content[0][content[0].index(':')+1:].rstrip('[Cell]').strip()
                if proCell:
                    Cell = proCell
                    if '(' in proCell:
                        Cell = proCell[:proCell.index('(')].strip('(').strip()
                    if Cell.lower() not in ['cell', 'cancer', 'tumor', 'clone', 'cell line', 'cells', 'human cell line', 'mouse cell line', 'cellline', 'celllines']:
                        if (not _parse_a_field({'cellType':Cell}, 'cellType', models.CellPops, 100, new = False)) and (not _parse_a_field({'cellType':Cell}, 'cellType', models.CellLines, 100, new = False)) : # in case metamap result in cell pop
                            print("metamap cell type")
                            return Cell
        except:
            pass
    if serious_fields:
        for sf in serious_fields:
            tmp = description_dict.get(sf, "")
            if tmp and (DCmodel == models.CellTypes) and (not _parse_a_field({'cell':tmp}, 'cell', models.CellLines, 100, new = False)) and (not _parse_a_field({'cell':tmp}, 'cell', models.TissueTypes, 100, new = False)) and (not _parse_a_field({'cell':tmp}, 'cell', models.CellPops, 100, new = False)):
                return tmp
            if tmp and (DCmodel == models.CellLines) and (not _parse_a_field({'cell':tmp}, 'cell', models.CellTypes, 100, new = False)):
                return tmp
            if tmp and (DCmodel == models.TissueTypes) and (not _parse_a_field({'cell':tmp}, 'cell', models.CellTypes, 100, new = False)) and (not _parse_a_field({'cell':tmp}, 'cell', models.CellLines, 100, new = False)):
                return tmp
            if tmp and (DCmodel not in [models.CellTypes, models.CellLines, models.TissueTypes]):
                return tmp
    return None

def parseAndsearch(description_dict, field):
    tmp_sea_cellLine = search_between_table(description_dict,
                         field, ['cell line'],
                         models.CellLines)
    tmp_sea_cellType = search_between_table(description_dict,
                         field, ['cell type'],
                         models.CellTypes)
    tmp_sea_tissueType = search_between_table(description_dict,
                         field, ['tissue', 'tissue type'],
                         models.TissueTypes)
    tmp_sea_cellpop = search_between_table(description_dict,
                         field, [],
                         models.CellPops)
    tmp_sea_disease = search_between_table(description_dict,
                         field, [],
                         models.DiseaseStates)
    if str(tmp_sea_tissueType).lower() in ['primary tumor', 'tumor']:
        tmp_sea_tissueType = None
    return {'cellType':tmp_sea_cellType, 'cellLine':tmp_sea_cellLine, 'tissueType':tmp_sea_tissueType, 'cellpop':tmp_sea_cellpop, 'disease':tmp_sea_disease}               
        


def cleanCategory(s):
    """Given a string, replaces ' ' with '_'
    '/', '&', '.', '(', ')'with ''
    """
    tmp = s.replace(" ", "_")
    for bad in ['/', '&', '.', '(', ')', ',']:
        tmp = tmp.replace(bad, "")
    return tmp


def gse_idToAcc(gdsId):
    """Given a GDS id, e.g. 200030833, tries to give a GDS accession, e.g.
    GSE30833

    NOTE: there is an algorithm: acc = "GSE"+gdsId[1:] (strip leading 0s)
    """
    #Cut = dropping of the "2" (which indicates series) and removal of leading
    #leading 0s
    cut = gdsId[1:].lstrip("0")
    return "GSE%s" % cut

def _parse_from_html(gseid, n = 0):
    """
    query GEO page of GSE, get the species and GSM samples
    """
    os.system('echo "html %s times"'%n)
    context = None
    try:
        url = 'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=%s'%gseid
        urlf = urllib.request.urlopen(url)
        context = urlf.read()
        context = context.decode(encoding='utf-8',errors='ignore')
        urlf.close()
    except:
        if n == 1: # if 1, already tried once, pass
            return(None)
        context = _parse_from_html(gseid, n = 1) # try again 

    return(context)

def _parse_species_gsm(urlcont):
    ## parse species and GSM ids
    Soup = BeautifulSoup(urlcont, 'html.parser')
    strings = [x.string for x in Soup.find_all('a')]
    if strings:
        gsmids = list(set([x for x in strings if str(x).startswith('GSM')]))
        species = list(set([x for x in strings if str(x) in ['Homo sapiens', 'Mus musculus']]))
        return('; '.join(species), '; '.join(gsmids))
    return(None, None)
        

def update_one_sample(gseid, ddir='geo', parse_fields=['other_ids', 'paper', 'name', 'species', 'description', 'antibody', 'factor',
                                           'cell type', 'cell line', 'cell pop', 'tissue', 'strain', 'disease','update date','release date']):
    """Given a gsmid, tries to create a new sample--auto-filling in the
    meta fields


    If overwrite is True and there is the sample that has the same gsmid, this function will overwrite that sample

    NOTE: will try to save the sample!!

    Returns newly created sample
    """

    print('+++ description')
    fields = ['Series/Title', 'Series/Summary', 'Series/Type',
            'Series/Overall-Design', 'Series/Status/Release-Date', 'Series/Status/Last-Update-Date',
             'Sample/Accession', 'Series/Pubmed-ID']
    sample_path = os.path.join(ddir+'/'+gseid[:7]+'/'+gseid+'.xml')
    xmlContent = getGEOSamples_byType_gse._getFieldXML(sample_path, fields = fields)

    if 'species' in parse_fields:
        print('+++ species')
        urlcont = _parse_from_html(gseid)
        if urlcont:
            species, accession = _parse_species_gsm(urlcont)
            species = species if species else None
            accession = accession if accession else None
        else:
            species, accession = None, None
        # if getFromPost(geoPost, "organism") == "HOMO SAPIENS":
        #     species = models.Species.objects.get(pk=1)
        # else:
        #     species = models.Species.objects.get(pk=2)
    
    paper = None
    pmid = None
    if 'paper' in parse_fields and 'Series/Pubmed-ID' in xmlContent:
        print('+++ paper')
        try:
            pmid = xmlContent['Series/Pubmed-ID']
            paper = pubmed.getOrCreatePaper(pmid)
        except:
            pmid = None
            paper = None

    if 'name' in parse_fields:
        print('+++ title')
        name = xmlContent['Series/Title']

    #HERE is where I need to create a classifier app/module
    #FACTOR, platform, species--HERE are the rest of them!

    if 'description' in parse_fields:
        print('+++ add description')
        description = json.dumps(xmlContent)
     # for cell   
    description_dict = {}
    for field in ['Series/Title', 'Series/Summary', 'Series/Type',
            'Series/Overall-Design']:
        description_dict[field] = xmlContent[field]
    if 'cell type' in parse_fields:
        print('+++ cell type')
        tmp_celltype = None
        # get first parsed cell type information
        searchCellType = parseAndsearch(description_dict, ['cell type', 'cell lineage', 'cell', 'cell line', 'source name', 'cell description', 'title'])
        if searchCellType['cellType'] and (str(searchCellType['cellType']).upper() not in [str(searchCellType['cellLine']).upper(), str(searchCellType['tissueType']).upper()]):
            tmp_celltype = searchCellType['cellType'] # use the cell type if parsed information not in other tables. else use "None" defined before
    
    if 'tissue' in parse_fields:
        print('+++ tissue')
        tmp_tissue = None
        searchTisssue = parseAndsearch(description_dict, ['tissue', 'tissue type', 'tissue depot', 'source name', 'cell description', 'title', 'cell type', 'cell lineage','cell', 'cell line'])
        if searchCellType['tissueType'] and (str(searchCellType['tissueType']).upper() not in [str(searchCellType['cellLine']).upper(), str(searchCellType['cellType']).upper(), str(searchCellType['cellpop']).upper(), str(searchCellType['disease']).upper()]):
            tmp_tissue = searchTisssue['tissueType']
        else:
            if tmp_tissue:
                test_tissue = parseAndsearch({'cell type':str(tmp_tissue)}, ['cell type']) # test parsed tissue information whether in cell type table
            else:
                test_tissue = {'cellType':None}
            if test_tissue['cellType']: # means parsed tissue information in cell type table, then ignore tissue
                tmp_tissue = None

    if 'disease' in parse_fields:
        print('+++ disease')
        disease_state = parseDisease(description_dict)
        if searchCellType['disease']:
            disease_state = searchCellType['disease']

    if 'cell pop' in parse_fields:
        print('+++ cell pop')
        cell_pop = parseCellPop(description_dict)
        if searchCellType['cellpop']:
            cell_pop = searchCellType['cellpop']

    if 'release date' in parse_fields:
        geo_release_date = xmlContent['Series/Status/Release-Date']
        geo_last_update_date = xmlContent['Series/Status/Last-Update-Date']
    xmlContent.pop('Sample/Accession') if 'Sample/Accession' in xmlContent.keys() else None

    res = [gseid, str(species), str(pmid), str(paper), str(name), str(tmp_celltype),
        str(tmp_tissue), str(disease_state), str(cell_pop), str(geo_release_date), 
        str(geo_last_update_date), str(accession), str(xmlContent)]
    time.sleep(3)
    return res
