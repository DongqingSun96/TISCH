"""Library to interface with Pubmed"""

import os
import re
import sys
import urllib.request, urllib.parse, urllib.error
import traceback
import datetime
import subprocess

import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

#AUTO-load classifiers
#a trick to get the current module 
_modname = globals()['__name__']
_this_mod = sys.modules[_modname]

_ppath = "/".join(_this_mod.__file__.split("/")[:-1])

# #CAN drop this if this is an app!
# DEPLOY_DIR="/home/lentaing/envs/newdc1.4/src"
# sys.path.insert(0, DEPLOY_DIR)
# from django.core.management import setup_environ
# from django.utils.encoding import smart_str
# import settings
# setup_environ(settings)
import env
models = env.models

def getPubmedXML(accession):
    """our PUBMED XML librarian!
    Given an accession #, tries to look for the record locally,
    IF not found, then makes a remote call to fetch it using the following 
    query:
    http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?id=20442865&db=pubmed&mode=xml

    Returns the pubmed record as xml string
    """
    docString = None
    path = os.path.join(_ppath, "pubmed")
    if not os.path.exists(path):
        os.mkdir(path)
    subdir = os.path.join(path, accession[:5])
    if not os.path.exists(subdir):
        os.mkdir(subdir)
    path = os.path.join(subdir, "%s.xml" % accession)

    if os.path.exists(path):
        f = open(path)
        docString = f.read()
        f.close()
    else:
        URL = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?id=%s&db=pubmed&mode=xml" % accession
        try:
            urlf = urllib.request.urlopen(URL)
            docString = urlf.read()
            docString = docString.decode('utf-8', errors = 'ignore')
            urlf.close()
            #write to file
            f = open(path, "w")
            f.write(docString)
            f.close()
        except:
            print("Exception in user code:")
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
            docString = None

    return docString

def pubmedToGDS(pmid):
    """Given a pubmed id, will try to reverse-look up the corresponding
    GSE that is associated
    """
    ret = None
    path = os.path.join(_ppath, "GSE_PUB")
    proc=subprocess.Popen(['grep','-R', pmid, path], 
                          stdout=subprocess.PIPE)  
    out, err = proc.communicate()
    m = re.findall("(\d+)\.txt", out.decode('utf-8'))
    if m:
        #NOTE: mutliple GSEs can be associated with a pubmed--we return all
        ret = ",".join(m)
    return ret

def getOrCreatePaper(pmid):
    """Given a pubmed id, tries to look for a django Paper obj; 
    IF not found, will create a new Paper obj and return it
    """
    ret = None
    tmp = models.Papers.objects.filter(pmid=pmid)
    # tmp = None
    print(tmp)
    print("Bitcher")
    if tmp:
        #return the first hit
        ret = tmp[0]
    else:
        #create a new paper- 
        #print "creating paper"
        p = models.Papers()
        # p = models.Papers.objects.get_or_create(pmid=pmid)
        #set ids
        p.pmid = pmid
        p.unique_id = pubmedToGDS(pmid)
        p.status = "new"

        #fill the fields
        docString = getPubmedXML(pmid)
        root = ET.fromstring(docString)
        article = root.findall("PubmedArticle/MedlineCitation/Article")
        
        if article:
            article = article[0]
            title = article.findall("ArticleTitle")
            if title:
                p.title = ''.join(title[0].itertext())
                # if title[0].text and title[0].getchildren()[0]:
                #     p.title = ''.join(title[0].itertext())
                # elif (not title[0].text) and title[0].getchildren()[0]:
                #     c = title[0].getchildren()[0].tag
                #     p.title = title[0].findall('%s'%c)[0].text.strip() 
                #     p.title = title[0].text.strip() 
                # elif (not title[0].text) and (not title[0].getchildren()[0]):
                #     p.title = None
                # else: # children tag exists
                #     p.title = title[0].text.strip() 

            abstract = article.findall("Abstract/AbstractText")
            if abstract:
                p.abstract = abstract[0].text.strip()

            #GET authors
            ls = []
            authors = article.findall("AuthorList/Author")
            if authors:
                for a in authors:
                    lastn = list(a)[0].text.strip()
                    #first= a._children[1].text.strip()
                    if len(list(a)) > 2:
                        inits = list(a)[2].text.strip()
                    else:
                        inits = ""
                    ls.append("%s %s" % (lastn, inits))
                p.authors = ",".join(ls)
                if len(p.authors) > 1000:
                    p.authors = ",".join(ls[-3:-1])
            journal = article.findall("Journal")
            if journal:
                journal = journal[0]
                #try to find the journal
                params = {}
                jname = journal.findall("ISOAbbreviation")
                if jname:
                    params['name'] = jname[0].text.strip()
                    #DISABLING auto-ISSN
                    #issn = journal.findall("ISSN")
                    #if issn:
                    #    params['issn'] = issn[0].text.strip()

                    j,created = models.Journals.objects.get_or_create(**params)
                    p.journal = j


        pub_date = root.findall("PubmedArticle/MedlineCitation/DateCreated")
        if pub_date:
            pub_date = pub_date[0]
            year = pub_date.findall("Year")[0].text.strip()
            month = pub_date.findall("Month")[0].text.strip()
            day = pub_date.findall("Day")[0].text.strip()
            p.pub_date = datetime.date(int(year), int(month), int(day))
        
        p.date_collected = datetime.datetime.now()
        
        #final bits
        try:
            p.save()
        except:
            print(p.authors)
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
            sys.exit(1)
            
        ret = p
        
    return ret
            
