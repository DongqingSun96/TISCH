import argparse
from optparse import OptionParser
import os, sys
import django
import pickle as p
import env
from scrna_parser_from_gse import _sync_gse
from scrna_parser_from_gse import sync_samples_from_gse_factor
from scrna_parser_from_gse import getLocalGeo
import time
import datetime

#def handler(signum, frame):
#    print "time out!"
def getSyncLog(infoStr):
    """ouput the record to DoneGsmXml.log file
    """
    os.system('echo "[%s] %s"' % (time.strftime('%H:%M:%S'), infoStr))


def convertTime(timeRegion):
    """check input time region and split per 31 days
    """
    minString = timeRegion.split('-')[0]
    maxString = timeRegion.split('-')[1]
    t1, t2 = minString.split('/'), maxString.split('/')
    mintime = datetime.datetime(int(t1[0]), int(t1[1]), int(t1[2]))
    maxtime = datetime.datetime(int(t2[0]), int(t2[1]), int(t2[2]))
    deltTime = maxtime - mintime
    getSplitTime = []
    if deltTime > datetime.timedelta(days=31):
        cnt = int(str(deltTime).split(' ')[0]) / 31
        for i in range(1, cnt+2):
            if i == 1:
                start = mintime
                mintime = start + datetime.timedelta(days=31)
                getSplitTime.append('%s-%s'%(start.strftime("%Y/%m/%d"), mintime.strftime("%Y/%m/%d")))
            elif i > 1 and i <= cnt:
                start = mintime + datetime.timedelta(days=1)
                mintime = start + datetime.timedelta(days=31)
                getSplitTime.append('%s-%s'%(start.strftime("%Y/%m/%d"), mintime.strftime("%Y/%m/%d")))
            else:
                start = mintime + datetime.timedelta(days=1)
                getSplitTime.append('%s-%s'%(start.strftime("%Y/%m/%d"), maxtime.strftime("%Y/%m/%d")))
         # output record to log file, so that user known what happened
        getSyncLog("# the input date region include %s"%str(deltTime))
        getSyncLog("# split date region into %d:"%len(getSplitTime))
        for i in getSplitTime:
            getSyncLog(i)
        return getSplitTime
    return [timeRegion]

def main():
    try:
        parser = argparse.ArgumentParser(description="""single cell dataset parser from GEO""")
        sub_parsers = parser.add_subparsers(help = "sub-command help", dest = "sub_command")
        new_parser = sub_parsers.add_parser("parser",  help = "parse new sample",description = "parse new data from GEO with option of filling in CistromeDB MySQL or not.")
        new_parser.add_argument('-d', dest='date_region', type=str, required = False, help='Parser will get the pubic samples in this given date region, Please use the format: 2016/01/01-2017/01/01. Default is the recent 100000 entries in GEO.')
        new_parser.add_argument('-o', dest='fsave', type=str, required = False, help='The table you want to save the new sample information, the default is "singleCell_new_collection.xls" which will be built in the working directory.')
        new_parser.add_argument('-fi', dest='fill', action="store_true", default=False, help="currently not used!!! This option should be given or not. add this option means parse the new samples from GEO and add in MySQL database at same time, or means just parse new samples save in outside table, default is False.")
        new_parser.add_argument('-el', dest='exclude',metavar="FILE", required=False, help="a one-column file contains Accession number that has been parsed")

        known_parser = sub_parsers.add_parser('known', help = 'add samples, known gsm id and factor', description = 'add samples to CistromeDB MySQL database, those samples are with known gsm id and facotr names.')
        known_parser.add_argument('-i', dest='infile', type=str, required = True, help='The file contains at least two column, one is gsm id, one is factor name with offical gene symbol.')
        known_parser.add_argument('-gc', dest='gsm_col', type=int, required = True, help='The column for gsm id in the -i table, start with 0.')
        known_parser.add_argument('-fi', dest='fill', action="store_true", default=False, help="currently not used!!!  This option should be given or not. add this option means parse the new samples from GEO and add in MySQL database at same time, or means just parse new samples save in outside table, default is False.")
        known_parser.add_argument('-o', dest='fsave', type=str, required = False, help='The table you want to save the new sample information, the default is "singleCell_new_collection.xls" which will be built in the working directory.')
        known_parser.add_argument('-p', dest="path_of_xml", type = str, required = False, help = 'The folder path contain all the xml files, eg: "./geo", the xml storage format should be: "./geo/GSE1000/GSE1000102.xml".')
        known_parser.add_argument('-rf', dest="refresh", action="store_true", default=False, help = 'currently not used!!!  whether you want to update if gsmid existed already. Optional.')
        known_parser.add_argument('-el', dest='exclude',metavar="FILE", required=False, help="a one-column file contains Accession number that has been parsed")

        local_parser = sub_parsers.add_parser('local', help = "go through the XML files in the given path, and parse the detail sample information.")
        local_parser.add_argument('-p', dest="path_of_xml", type = str, required = True, help = 'The folder path contain all the xml files, eg: "./geo", the xml storage format should be: "./geo/GSE1000/GSE1000102.xml".')
        local_parser.add_argument('-fi', dest='fill', action="store_true", default=False, help="currently not used!!!  This option should be given or not. add this option means parse the new samples from GEO and add in MySQL database at same time, or means just parse new samples save in outside table, default is False.")
        local_parser.add_argument('-o', dest='fsave', type=str, required = False, help='The table you want to save the new sample information, the default is "singleCell_new_collection.xls" which will be built in the working directory.')

        args = parser.parse_args()
        if args.sub_command == 'parser':
            dregion, file_save, fill_or_not, excludes = args.date_region, args.fsave, args.fill, args.exclude
            # check date region
            if not dregion:
                getSyncLog("No date region setting!")
                dregion = False
            else:
                checkTime = convertTime(dregion)
            #check save file    
            if not file_save:
                file_save = './singleCell_new_collection.xls'
    
            for oneTime in checkTime:
                dregion = oneTime
                getSyncLog("#+++++++++ New Collection in %s"%dregion)
                if fill_or_not:
                    getSyncLog('parse new sample and add in database')
                    _sync_gse(file_save, fill_or_not, dregion, exludeFile=excludes, refresh=True)
                elif not fill_or_not:
                    getSyncLog("parse new samples and do not add in database")
                    _sync_gse(file_save, fill_or_not, dregion, exludeFile=excludes, refresh=True)
                else:
                    getSyncLog('unrecognized -fi option')
                    sys.exit(1)

        if args.sub_command == 'known':
            print('fresh database or not: '+ str(args.refresh))
            infile, gsm_col, path, fill_or_not, file_save, excludes = args.infile, args.gsm_col, args.path_of_xml, args.fill, args.fsave, args.exclude

            if not file_save:
                file_save = 'singleCell_result_from_known.xls'

            if path:
                sync_samples_from_gse_factor(infile, gsm_col, fsave = file_save, xmlPath=path, fill_or_not = fill_or_not, refresh = args.refresh)
            else:
                sync_samples_from_gse_factor(infile=infile, gsm_col=gsm_col, fsave = file_save, fill_or_not = fill_or_not, refresh = args.refresh)

        if args.sub_command == 'local':
            file_save, fill_or_not, path, typo, excludes = args.fsave, args.fill, args.path_of_xml, True, False
            if not file_save:
                file_save = './singleCell_new_collection.xls'

            getLocalGeo(file_save, fill_or_not, path, typo, refresh=True)

            
    except KeyboardInterrupt:
        sys.stderr.write("User interrupted me!\n")
        sys.exit(0)

if __name__ == '__main__':
    main()
    #signal.signal(signal.SIGALRM, handler)
