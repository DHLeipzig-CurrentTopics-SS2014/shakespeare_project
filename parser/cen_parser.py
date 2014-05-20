import os
import re
import string

def parse_index_entry(index_entry):
   year = index_entry[:index_entry.index(', ')]
   author = index_entry[index_entry.rindex(', ')+2:-1]
   title = index_entry[index_entry.index(', ')+2:index_entry.index(' (')]
   title = re.sub(r'\.|,','', title)
   return author.lower(), year, title.lower()

index = open('index.txt', 'r')

for index_entry in index:
   xml_string = '<xml>\n'

   author, year, title = parse_index_entry(index_entry)
   xml_string += '   <author>' + author + '</author>\n'
   xml_string += '   <year>' + year + '</year>\n'  
   xml_string += '   <title>' + title + '</title>\n'

   text_file_name = year + ' ' + title + '.txt'
   print('OPEN: ' + text_file_name)
   text_file = open(os.path.join('cen', text_file_name), 'r', encoding = 'iso8859_15')
   text = text_file.read()
   text_file.close()
   text = text.translate(dict.fromkeys(string.punctuation.encode('iso8859_15'), None))
   xml_string += '   <text>\n'

   for word in text.split():
      xml_string += '      <w>' + word.lower() + '</w>\n'

   xml_string += '   </text>\n'
   xml_string += '</xml>\n'
     
   xml_file = open('cen_xml/' + re.sub(' ', '_', title) + '.xml', 'w')
   xml_file.write(xml_string)
   
