#!/usr/bin/env python3
####################################
#
# parser for the cen corpus
# ! requires the system tool catdoc to be installed !
#
# usage: ./cen_parser.py <cen.zip> <output_dir>
#
####################################
import os
import sys
import re
import string
import zipfile

def parse_index_entry(index_entry):
   year = index_entry[:index_entry.index(', ')]
   author = index_entry[index_entry.rindex(', ')+2:-1]
   title = index_entry[index_entry.index(', ')+2:index_entry.index(' (')]
   return author, year, title

def get_index(index_string_from_catdoc):
   new_index = list()

   # first line in the index string is a header
   for index_entry in index_string_from_catdoc.strip().split('\n')[1:]:
      #~ print(index_entry)
      author, year, title = parse_index_entry(index_entry)

      filename_title = re.sub(r'\.|,','', title)
      filename_title = re.sub('’', '\'', filename_title)
      filename_title = filename_title.lower()

      text_file_name = year + ' ' + filename_title + '.txt'

      if text_file_name == "1891 don orsino.txt":
         text_file_name = "1892 don orsino.txt"

      if text_file_name == "1898 penelope\'s experience in scotland.txt":
         text_file_name = "1898 penelope\'s experiences in scotland.txt"

      if text_file_name == "1907 the old peobody pew.txt":
         text_file_name = "1907 the old peabody pew.txt"

      if text_file_name == "1906 rezanov .txt":
         text_file_name = "1906 rezanov.txt"

      if text_file_name == "1911 ethan forme.txt":
         text_file_name = "1911 ethan frome.txt"

      if text_file_name == "1902 the splendid idle forties.txt":
         text_file_name = "1902 the splindid idle forties.txt"

      if text_file_name == "1908 dorothy and the wizard of oz.txt":
         text_file_name = "1908 dorothy and the wizard in oz.txt"

      if text_file_name == "1898 helbeck of bannisdale.txt":
         new_index.append(("1898 helbeck of bannisdale 1.txt", author, year, title))
         new_index.append(("1898 helbeck of bannisdale 2.txt", author, year, title))
         continue
      if text_file_name == "1896 sir george tressady.txt":
         new_index.append(("1896 sir george tressady 1.txt", author, year, title))
         new_index.append(("1896 sir george tressady 2.txt", author, year, title))
         continue
      new_index.append((text_file_name, author, year, title))
   return new_index

def dump_all_to_xml(index, cen_corpus_file, destination_directory):
   for filename, author, year, title in index:
      xml_string = '<xml>\n'

      xml_string += '   <author>' + author + '</author>\n'
      xml_string += '   <year>' + year + '</year>\n'
      xml_string += '   <title>' + title + '</title>\n'

      print('OPEN: ' + filename)
      #encoding? in "1881 a fair barbarian.txt"(3211): _naivet<E9>_
      text_file = cen_corpus_file.open(os.path.join('cen', filename), mode='r')#, encoding = 'iso8859_15')
      text = text_file.read().decode('iso8859_15')
      text_file.close()
      # why is string.punctuation encoded in iso8859_15?
      text = str(text).translate(dict.fromkeys(string.punctuation.encode('iso8859_15'), None))
      xml_string += '   <text>\n'
      xml_string +=  text.lower()
      xml_string += '   </text>\n'
      xml_string += '</xml>\n'

      xml_file = open(destination_directory + '/' + re.sub(' ', '_', title) + '.xml', 'w')
      xml_file.write(xml_string)


def main(corpus, result_dir):
   zf = zipfile.ZipFile(corpus)
   if not os.path.exists(result_dir):
       os.makedirs(result_dir)

   from subprocess import Popen, PIPE
   #requires the tool "catdoc" to be installed on the system
   process = Popen(['catdoc', '-w', '-'],stdout=PIPE, stdin=PIPE)
   stdout, stderr = process.communicate(input=zf.read('index cen.doc'))
   index_string = stdout.decode('utf-8')

   index = get_index(index_string)

   dump_all_to_xml(index, zf, result_dir)
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
