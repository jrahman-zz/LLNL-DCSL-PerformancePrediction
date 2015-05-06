

class Dataset:
    def __init__(self, headers, data):
        self._cols = headers
        self._data = data

    def __getitem__(self, index):
        if isinstance(index, str):
            self._get_column(index)
        if isinstance(index, int):
            self._get_row(index)
        raise ValueError('Invalid index')

    def __delitem__(self, index):
        if isinstance(index, str):
            self._del_column(index)
        if isinstance(index, int):
            self._del_row(index)
        raise ValueError('Invalid index')

    def _get_column(self, name):
        column = []
        for row in data:
            column.app(row[self._cols[name]])
        return column

    def _get_row(self, index):
        return self._data[index]

    def _del_column(self, name):
        index = self._cols[name]
        for key in self._cols:
            if self._cols[key] > index:
                self._cols[key] = self._cols[key] - 1
        del self._cols[name]
        for row in data:
            row[index].pop()

    def _del_row(self, index):
        data[index].pop(index)

