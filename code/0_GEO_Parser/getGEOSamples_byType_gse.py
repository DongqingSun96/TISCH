import os,sys
import json, re, time
import urllib.request, urllib.parse, urllib.error
import traceback
from datetime import datetime
import pickle
import subprocess
from operator import itemgetter
import random
import importlib
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from xml.dom.minidom import parseString

#AUTO-load classifiers
#a trick to get the current module
_modname = globals()['__name__']
_this_mod = sys.modules[_modname]

_ppath = "/".join(_this_mod.__file__.split("/")[:-1])

from django.utils.encoding import smart_str
import env
models = env.models

import scrna_parser_from_gse

def readGeoXML(path, docString=None):
    """
    Input: a file path or a string--default is to use the path

    Tries to read in the geo xml record,
    **KEY: REMOVES the xmlns line
    Returns the xml record text WITHOUT the xmlns line!!!
    """
    if docString:
        f = docString.split("\n")
    else:
        if path:
            f = open(path)
        else:
            f = ''
    tmp = []
    try:
        for l in f:
            if l.find("xmlns=\"http://www.ncbi.nlm.nih.gov/geo/info/MINiML\"") == -1:
                tmp.append(l)
    except: # sometimes, the xml is not saved as utf-8 in local, do getGeoXml agaim
        gsmid = os.path.basename(path).rstrip('.xml')
        ag = scrna_parser_from_gse.getGeoXML(accession=gsmid)
        f = open(os.path.join('./geo/'+gsmid[:7]+'/'+gsmid+'.xml'))
        tmp = []
        for l in f:
            if l.find("xmlns=\"http://www.ncbi.nlm.nih.gov/geo/info/MINiML\"") == -1:
                tmp.append(l)
    if not docString and not isinstance(f, str):
        f.close()
    return "".join(tmp)


def _getFieldXML(sample_path, fields = ['Sample/Library-Strategy', 'Sample/Description', 'Sample/Data-Processing',
    'Sample/Channel/Extract-Protocol', "Sample/Title", 'Sample/Channel/Source', 'Sample/Channel/Characteristics']):
    """
    get text of items in filds list from XML
    we need these info for matching key words, like single cell
    """
    text = readGeoXML(sample_path)
    ## parse XML content
    rt = ET.fromstring(text)
    info = {}
    for field in fields:
        tmp = rt.findall(field)
        if tmp:
            info[field] = '; '.join([x.text.strip() for x in tmp])
        else:
            pass
    return info

def _matchKeyWord(xmlContent, key, fileds=False):
    ## match key words in a specific xml content
    ## return the match words
    res = {}
    if not fileds:
        fileds = list(xmlContent.keys()) # use all fields if not speficify
    for field in xmlContent.keys():
        if field in fileds:
            tmp = list(set(re.findall(r'%s'%key, xmlContent[field].replace('-', '').replace('_', ''), re.I)))
            if tmp:
                res[field]= tmp # a list in dict
    return res

def _match_scRNAseq(xmlContent, fields=False):
    """
    match key words, like single cell, single cell RNA-seq, and sequencing platform,etc
    return a dict, contains geo items and matched keys
    """
    if not xmlContent:
        os.system('echo "No XML content"')
        return {}
    #filter bulk RNA-seq in single cell RNA-seq GSE, uploder mentioned single cell but actually bulk RNA-seq 
    ## bulk RNA-seq apears in sample description, title, and source name
    for key in ['bulk rnaseq', 'a549', ]:
        bulk1 = _matchKeyWord(xmlContent, key = key, fileds = fields)
        if bulk1:
            os.system('echo "%s"' % key)
            return {}
    ## or library stratey : bulk RNA-seq appears in any fields 
    bulk2 = _matchKeyWord(xmlContent, key = "library strategy: bulk rnaseq")
    if bulk2:
        os.system('echo "bulk rnaseq"')
        return {} # return empty, if bulk RNA-seq appears in Title 
    match_res = {}
    ## 1. match with single cell words, remove special characters, like '-'
    for key1 in ['single cell', 'scrnaseq', 'singlecell rnaseq', 'singlecell transcriptome']:
        tmp = _matchKeyWord(xmlContent, key1)
        if tmp:
            for i in tmp.keys():
                match_res[i].extend(tmp[i]) if i in match_res.keys() else match_res.update({i:tmp[i]})
    # print(match_res)
    tmp = []
    ## 2. match with platform words
    keys = {}
    with open('platform.txt') as f:
        for line in f:
            line = line.rstrip().split('\t')
            keys[line[0]] = line[1] # platforms of sequecing, like 10X Genomics, Smart-seq2
    for key2 in keys.keys():
        tmp = _matchKeyWord(xmlContent, keys[key2]) # result of key word matching, a list in dict
        if tmp:
            for i in tmp.keys():
                # print(tmp)
                match_res[i].extend(tmp[i]) if i in match_res.keys() else match_res.update({i:tmp[i]})
    return match_res

def _match_scATACseq(xmlContent, fields=False):
    """
    match key words, like single cell, single cell RNA-seq, and sequencing platform,etc
    return a dict, contains geo items and matched keys
    """
    if not xmlContent:
        os.system('echo "No XML content"')
        return {}
    #filter bulk RNA-seq in single cell RNA-seq GSE, uploder mentioned single cell but actually bulk RNA-seq 
    ## bulk RNA-seq apears in sample description, title, and source name
    for key in ['bulk atacseq']:
        bulk1 = _matchKeyWord(xmlContent, key = key, fileds = fields)
        if bulk1:
            os.system('echo "%s"' % key)
            return {}
    ## or library stratey : bulk RNA-seq appears in any fields 
    bulk2 = _matchKeyWord(xmlContent, key = "library strategy: bulk atacseq")
    if bulk2:
        os.system('echo "bulk atacseq"')
        return {} # return empty, if bulk RNA-seq appears in Title 
    match_res = {}
    ## 1. match with single cell words, remove special characters, like '-'
    for key1 in ['single cell', 'scatacseq', 'singlecell atacseq', 'singlecell accessiblity']:
        tmp = _matchKeyWord(xmlContent, key1)
        if tmp:
            for i in tmp.keys():
                match_res[i].extend(tmp[i]) if i in match_res.keys() else match_res.update({i:tmp[i]})
    # print(match_res)
    tmp = []
    ## 2. match with platform words
    keys = {}
    with open('platform.txt') as f:
        for line in f:
            line = line.rstrip().split('\t')
            keys[line[0]] = line[1] # platforms of sequecing, like 10X Genomics, Smart-seq2
    for key2 in keys.keys():
        tmp = _matchKeyWord(xmlContent, keys[key2]) # result of key word matching, a list in dict
        if tmp:
            for i in tmp.keys():
                # print(tmp)
                match_res[i].extend(tmp[i]) if i in match_res.keys() else match_res.update({i:tmp[i]})
    return match_res

def _checkSuperSeries(sample_path):
    # remove SuperSeries
    xml_string = readGeoXML(sample_path)
    root = ET.fromstring(xml_string)
    if 'SuperSeries of' in [child.attrib['type'] for child in root.findall('Series/Relation')]:
        return True
    else:
        return False

def _checkType(acc, sample_path, type_need):
    """
    check whether it is single cell RNAseq or single cell ATAC-seq
    based on key words matching
    """ 
    ## read in XML to get sample description
    ret = {}
    fields = ['Series/Title', 'Series/Summary', 'Series/Type', 'Series/Overall-Design']
    if sample_path and os.path.isfile(sample_path):
        if _checkSuperSeries(sample_path) == True:
            return None
        # NOTE: we need readGeoXML to process
        xmlContent = _getFieldXML(sample_path, fields = fields)
        # parse single cell
        if 'sc-rna-seq' in type_need:
            # single cell RNA-seq, Library-strategy must be RNA-Seq
            rnaseq = _matchKeyWord(xmlContent, key = 'rnaseq', fileds = fields)
            if 'Expression profiling by high throughput sequencing' in xmlContent['Series/Type']:
                res = _match_scRNAseq(xmlContent, fields)
                if res:
                    ret[acc] = res
                    return ret
            else:
                os.system('echo "%s: No rnaseq"'%acc)
        if 'sc-atac-seq' in type_need:
            # single cell ATAC-seq, Library-strategy must be ATAC-Seq
            rnaseq = _matchKeyWord(xmlContent, key = 'atacseq', fileds = fields)
            if 'Genome binding/occupancy profiling by high throughput sequencing' in xmlContent['Series/Type']:
                res = _match_scATACseq(xmlContent, fields)
                if res:
                    ret[acc] = res
                    return ret
            else:
                os.system('echo "%s: No atacseq"'%acc)
    if sample_path and not os.path.isfile(sample_path):
        xml = scrna_parser_from_gse.getGeoXML(accession=acc, path="/".join(sample_path.split("/")[0:-2]))
        if _checkSuperSeries(sample_path) == True:
            return None
        ret = _checkType(acc = acc, sample_path = sample_path, type_need = type_need) if xml else None
        return ret
    return None
            

def getGeoSamples_byType(ddir="geo", ttype=["sc-rna-seq", "sc-atac-seq"], unique_ids=False, refresh=False):
    """A filter for our Geo model; searches our db for the specific sample
    type.
    NOTE: hones in on Library-Strategy tag

    Returns a list of samples fitting the specified

    NOTE: building this up takes time, around 10 secs almost 1 minute!
    TRY: caching the result, reading from a cached file takes only 1 minute
    Store them in files by the .ttype--in the local dir
    """
    ret = {}
    if not unique_ids: #qury all local samples
        #NEED to generate the file, and make the call recursively
        #actually, just one level of recursion b/c geo is pretty flat
        p = os.path.join(ddir)
        ls = os.listdir(p)
        ls = [x for x in ls if x.startswith('GSE') and x != 'GSE'] # for real gsm ids
        for df in ls:
            path = os.path.join(p, df)
            if os.path.isfile(path): #it's a file--check if it's ChIP-Seq
                print(path)
                typo = _checkType(acc=df.split(".")[0], sample_path=path, type_need=ttype) # check whether the seq type is chip-seq, atac, or dnase
                if typo:
                    ret.update(typo)
            else:
                #it's a dir recur
                newd = os.path.join(ddir, df)
                newdict = getGeoSamples_byType(ddir=newd, ttype=ttype, refresh=refresh)
                if newdict and (type(newdict) == type(ret)):
                    ret = dict(ret, **newdict)
    elif unique_ids: # query just for the specified gsm
        for gseid in unique_ids:
            p = os.path.join(ddir+'/'+gseid[:7]+'/'+gseid+'.xml')
            typo = _checkType(acc=gseid, sample_path=p, type_need=ttype)
            if typo:
                ret.update(typo)
    else:
        pass
    return ret


def getGeoSamples_byTypes(path, ddir, datatype=False, gseids=False, refresh=False): #ttypes = ["ATAC-Seq"]): #"ChIP-Seq", "DNase-Hypersensitivity"]):
    ret = []
    if not refresh and os.path.exists(path):
        ret = pickle.load(open(path))
        return ret
    #for t in ttypes:
    if datatype and gseids:
        ret = getGeoSamples_byType(ddir=ddir, ttype=datatype, unique_ids=gseids, refresh=refresh)
    elif datatype and not gseids:
        ret = getGeoSamples_byType(ddir=ddir, ttype=datatype, refresh=refresh)
    elif gseids and not datatype:
        ret = getGeoSamples_byType(ddir=ddir, unique_ids=gseids, refresh=refresh)
    else:
        ret = getGeoSamples_byType(ddir=ddir, refresh=refresh)
    # pickle.dump(ret, open(path, "w"))
    return ret
