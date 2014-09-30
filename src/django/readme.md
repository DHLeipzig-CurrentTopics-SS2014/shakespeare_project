
### running
1. go to this directory in terminal.
2. remove your db.sqlite3 file
3. sync current model to your db
    python manage.py syncdb

Now we need to load the data, the script works for the output of the lampeter parser w/o words.
1. to run the shell
    python manage.py shell
2. in it:
    from corpora.tools.corpus_parser import CorpusParser
    cp = CorpusParser()
    cp.parse_folder(foldername, corpus_name)
the folder must be in this directory! (for some to me unknown reason full path does not work for me)

now the data is loaded, you can either use it in the shell or start the server:
1. run the server
    python manage.py runserver
2. check http://127.0.0.1/texts/

### db schema
* can be seen in corpora/models


