#!/usr/bin/env python

# ================================
# @auther: Xin Dong
# @email: xindong9511@gmail.com
# @date: Apr 2020
# ================================

'''
Parse by GSE

this script is used to parse all supplementary files from GEO

(local version) -- only check local downloaded xml

with the purpose of single cell collection

judge the file type whether it is barcodes or tpm or others

generate a table with download links

'''


import os
import sys
import urllib.request
import re
import argparse
import xml.etree.ElementTree as ET
import time


def judgeType(link_dic):
    file_type_dic = {}
    file_type_dic["raw"] = []
    file_type_dic["barcode"] = []
    file_type_dic["count"] = []
    file_type_dic["tpm"] = []
    file_type_dic["gene"] = []
    file_type_dic["other"] = []
    for name in link_dic.keys():
        if "barcode" in name.lower():
            file_type_dic["barcode"].append(link_dic[name])
        elif "count" in name.lower():
            file_type_dic["count"].append(link_dic[name])
        elif "tpm" in name.lower() or "matrix" in name.lower():
            file_type_dic["tpm"].append(link_dic[name])
        elif "gene" in name.lower():
            file_type_dic["gene"].append(link_dic[name])
        elif "raw" in name.lower():
            file_type_dic["raw"].append(link_dic[name])
        else:
            file_type_dic["other"].append(link_dic[name])
    return file_type_dic

def findSuppleDataXml(xml):
    tree = ET.parse(xml)
    root = tree.getroot()
    link_dic = {}
    for file in root.iter('{http://www.ncbi.nlm.nih.gov/geo/info/MINiML}Supplementary-Data'):
        filelink = file.text.strip()
        filename = filelink.split("/")[-1]
        link_dic[filename] = filelink
    return link_dic


def findSuppleData(gsm_html):
    filename_regexp = re.compile(r'<tr valign="top"><td bgcolor="#[ED]EE[EB][ED][EC]">.*</td>')
    filename_infor = filename_regexp.findall(gsm_html)
    link_regexp = re.compile(r'<td bgcolor="#[DE]EE[BE][ED][EC]">.*href=.*>\(ftp\)')
    link_infor = link_regexp.findall(gsm_html)
    link_dic = {}
    if filename_infor:
        if len(filename_infor) == len(link_infor):
            for i in range(len(filename_infor)):
                name = re.sub(r'<tr valign="top"><td bgcolor="#[ED]EE[EB][ED][EC]">','',filename_infor[i]).replace('</td>','')
                link = re.sub(r'<td bgcolor="#[DE]EE[BE][ED][EC]">.*href="','',link_infor[i]).replace('">(ftp)','')
                link_dic[name] = link
            return link_dic
        else:
            print("some files miss links")
            return {}
    else:
        print("no link") 
        return {}     


def getGsmHtml(gsm):
    try:
        gsm_url = 'http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=%s'%gsm
        gsm_html = urllib.request.urlopen(gsm_url).read().decode('utf-8')
        return gsm_html
    except:
        print("retry......")
        time.sleep(10)
        gsm_url = 'http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=%s'%gsm
        gsm_html = urllib.request.urlopen(gsm_url).read().decode('utf-8')
        return gsm_html


def main():
    class MyParser(argparse.ArgumentParser):
        def error(self, message):
            sys.stderr.write('error: %s\n' % message)
            self.print_help()
            sys.exit(2)

    parser = MyParser()
    parser.add_argument('-l', '--local', action='store_true',help='local file flag', default=False)
    parser.add_argument('-i', '--id', help='GSM id for online search')
    parser.add_argument('-x', '--xmlfolder', help='path to folder which saved xml files')
    parser.add_argument('-L', '--list', help='path to gsm list file')
    parser.add_argument('-o', '--output', help='path to output')
    args = parser.parse_args()

    gsm = args.id
    local_flag = args.local
    xml_path = args.xmlfolder
    input_list = args.list
    output = args.output


    if local_flag:
        header = "\t".join(["gseid","raw","barcode","count","tpm","gene","other"])+"\n"
        dict_gse = {}
        content = ""
        for i in os.listdir(xml_path):
            for j in os.listdir(xml_path+"/"+i):
                link_dic = findSuppleDataXml(xml_path+"/"+i+"/"+j)
                gse = j.split("/")[-1].split(".")[0]
                print(gse)
                file_type_dic = judgeType(link_dic)
                content = content + "\t".join([gse,",".join(file_type_dic["raw"]),
                    ",".join(file_type_dic["barcode"]),",".join(file_type_dic["count"]),",".join(file_type_dic["tpm"]),
                         ",".join(file_type_dic["gene"]),",".join(file_type_dic["other"])]) + "\n"
        with open(output,"w+") as output_file:
            output_file.write(header + content)


        # file_type_dic = judgeType(link_dic)
        # print(file_type_dic)
    else:
        # if input_list:
        #     try:
        #         if os.path.getsize(output) == 0:
        #             with open(output,"a+") as output_file:
        #                 output_file.write("\t".join(["gsmID","barcode","count","tpm","gene","others"]) + "\n")
        #     except FileNotFoundError:
        #         with open(output,"a+") as output_file:
        #             output_file.write("\t".join(["gsmID","barcode","count","tpm","gene","others"]) + "\n")
        #     with open(input_list, "r+") as input_file:
        #         id_list = input_file.readlines()
        #         for i in id_list:
        #             gsmid = i.strip()
        #             print(gsmid)
        #             gsm_html = getGsmHtml(gsmid)
        #             print("Got the page.")
        #             link_dic = findSuppleData(gsm_html)
        #             file_type_dic = judgeType(link_dic)
        #             with open(output,"a+") as output_file:
        #                 output_file.write("\t".join([gsmid,file_type_dic["barcode"],file_type_dic["count"],file_type_dic["tpm"],
        #                 file_type_dic["gene"],",".join(file_type_dic["other"])])+"\n")
        #             print("wait for 10 secs.")
        #             time.sleep(10)
        
                    
        # else:
        #     os.system('echo %s' % gsm)
        #     gsm_html = getGsmHtml(gsm)
        #     link_dic = findSuppleData(gsm_html)
        #     print(link_dic)
        #     file_type_dic = judgeType(link_dic)
        #     print(file_type_dic)
        pass


if __name__ == "__main__":
    main()
    






