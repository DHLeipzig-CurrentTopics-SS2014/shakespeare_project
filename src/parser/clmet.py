#!/usr/env/python3

from lxml import etree
from os import listdir,makedirs
from os.path import isfile,join,exists


path = "plain_text/"

subfolders = [f for f in listdir(path) if not isfile(join(path,f))]


for folder in subfolders:  
    
    # Generiert Ordner
    if not exists("result"): makedirs("result")
    if not exists("result/"+folder): makedirs("result/"+folder)
    
    files = [f for f in listdir(path+folder) if isfile(join(path+folder,f))]

    for file in files:

        xml=etree.parse(path+folder+"/"+file,parser=etree.HTMLParser())
        author = xml.xpath("//author")[0].xpath("string()")
        title = xml.xpath("//title")[0].xpath("string()")
        year = xml.xpath("//date")[0].xpath("string()")
        splitted_text = xml.xpath("//text")[0].xpath("string()").split()

        file = open("result"+"/"+folder+"/"+file,"w")
        file.write("<xml>")
        
        file.write("<author>"+author+"</author>");
        file.write("<year>"+year+"</year>");
        file.write("<title>"+title+"</title>")


        file.write("<text>")
        for word in splitted_text:
            file.write("<w>"+word+"</w>")
        
        file.write("</text>")
        file.write("</xml>")
        file.close()
    


