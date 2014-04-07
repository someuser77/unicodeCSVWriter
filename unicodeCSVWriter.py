import xc_Oracle # http://cx-oracle.sourceforge.net/
import csv, codecs, cStringIO
import os

os.environ["NLS_LANG"] = ".UTF8"

# based on the UnicodeWriter example at https://docs.python.org/2/library/csv.html

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """
    
    # add a sep=',' line to the target csv file to hint it.

    def __init__(self, f, dialect=csv.excel, encoding="utf-16", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        vals = [s.encode("utf-8") if isinstance(s, unicode) else str(s) for s in row if s != None]
        
        self.writer.writerow(vals)
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row) 

get_file_name = lambda name: name.zfill(4) + '.csv'

connection = cx_oracle.connect('...')

cursor = connection.cursor()

cursor.execute('...')

cursor.arraysize = 1000
file_counter = 0
rowcount = 0

while True:
    curr_row = cursor.fetchone()
    if curr_row is None:
	break
    with open(get_file_name(str(file_counter)), 'wb') as fout:
	writer = UnicodeWriter(fout)
	while curr_row is not None:
	    writer.writerow(curr_row)
	    rowcount += 1
	    if rowcount % 20000 == 0:
		file_counter += 1
		break
	    curr_row = cursor.fetchone()
	print('Finished creating file: ' + get_file_name(str(file_counter)))
	
connection.close()

del os.environ["NLS_LANG"]








