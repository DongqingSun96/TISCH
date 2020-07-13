import pandas as pd
import os
import sys
import xml.etree.ElementTree as ET
import urllib.request
import time



def merge_extract_result(result_table, name, index, col):
    ori_value = result_table.loc[index, col]
    result = result_table.copy()
    if isinstance(ori_value,str):
        result.loc[index,col] = ori_value + ",[RAW]%s" % name
    else:
        result.loc[index,col] = "[RAW]%s" % name
    return result

def findSuppleDataXml(xml):
    root = ET.fromstring(xml)
    file_list = []
    for file in root.iter('file'):
        filename = file.text.strip()
        file_list.append(filename)
    return file_list

parser_result_table = "txt/parse_gse.txt"
folder = "0710_collection"
series_list = ["GSE111458","GSE103867","GSE148345","GSE115501","GSE132465","GSE127888","GSE112271","GSE126131","GSE150321","GSE124898","GSE140430","GSE142116","GSE128822","GSE113336","GSE109085","GSE125680","GSE128933","GSE76312","GSE129845","GSE107747","GSE103866","GSE144735","GSE111896","GSE109308","GSE146026","GSE132065","GSE111065","GSE149614","GSE122703","GSE145896","GSE133094","GSE61844","GSE119630","GSE140819","GSE123476","GSE110680","GSE132257","GSE126068","GSE97930","GSE74450","GSE137941","GSE134577","GSE81076","GSE134570","SE120221","GSE130804","GSE102580","GSE100618","GSE146763","GSE110973","GSE71318","GSE125970","GSE143214","GSE143669","GSE130560","GSE98011","GSE148371","GSE147104","GSE85241","GSE128992","GSE123028","GSE67835","GSE131409","GSE109822","GSE111822","GSE119969","GSE138002","GSE130784","GSE136831","GSE133854","GSE109205","GSE110154","GSE147457","GSE116500","GSE141238","GSE131882","GSE131434","GSE113931","GSE118209","GSE113046","GSE100501","GSE116106","GSE149100","GSE81233","GSE136447","GSE140231","GSE142538","GSE113675","GSE100866","GSE135922","GSE130148","GSE133181","GSE122970","GSE133345","GSE117837","GSE104995","GSE115982","GSE144568","GSE110791","GSE76234","GSE128991","GSE105142","GSE130228","GSE130117","GSE126250","GSE129611","GSE106888","GSE128518","GSE114961","GSE145843","GSE116683","GSE83501","GSE109555","GSE111404","GSE150728","GSE62408","GSE145838","GSE143417","GSE133894","GSE85534","GSE130888","GSE132950","GSE136103","GSE119807","GSE112438","GSE113036","GSE136871","GSE144434","GSE130473","GSE130973","GSE143567","GSE142449","GSE90734","GSE107794","GSE111301","GSE121477","GSE97104","GSE142637","GSE130289","GSE87195","GSE134576","GSE137877","GSE115639","GSE148665","GSE138680","GSE130882"]

table = pd.read_csv(parser_result_table, sep="\t")
result = table[table["gseid"].isin(series_list)]

# download function
# some series only provided bw files, and too large to download
# so I changed to get gse from web page
for i in result.index:
    gseid = result.loc[i,"gseid"]
    path = "%s/%s" % (folder,gseid)
    print(path)
    url_list = result.loc[i,:].tolist()
    url_group = []
    for url_str in url_list:
        if isinstance(url_str,str):
            url_item = url_str.split(",")
            url_group = url_group + url_item
        else:
            continue
    url_group = url_group[1:]
    print(url_group)
    try:
        os.makedirs(path)
    except:
        print("%s has created!" % path)
    for url in url_group:
        filename = url.split("/")[-1]
        if not os.path.exists("%s/%s" %  (path, filename)):
            os.system("wget %s -O %s/%s" % (url, path, filename))
            print("finish download")
        else:
            print("file existed!")
    series_matrix_link = "https://ftp.ncbi.nlm.nih.gov/geo/series/%snnn/%s/matrix/%s_series_matrix.txt.gz" % (gseid[0:6],gseid,gseid)
    os.system("wget %s -O %s/%s" % (series_matrix_link, path, series_matrix_link.split("/")[-1]))
    # file_list = os.listdir(path)





# result.to_csv("single_cell_supplementary_file_after_extraction.txt", index=None, sep="\t")
            
    