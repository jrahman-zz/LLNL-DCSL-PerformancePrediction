
import util

class Dataset(object):


    def __init__(self, data):
        if isinstance(data, str):
            with open(filename, 'r') as f:
                d = load_csv(filename)
            self._colnames = d.keys()
            self._data = d
            self._rowcount = len(self._data[self._colnames[0]])

    def __getitem__(self, index):
        if self._rowcount >= index:
            raise ValueError('Index %d beyond rowcount %d' % (index, self._rowcount))

    def 


