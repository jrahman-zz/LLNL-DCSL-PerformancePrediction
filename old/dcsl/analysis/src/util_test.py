
import util
import sys
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
#    conn = util.load_db(sys.argv[1], sys.argv[2])
    conn = util.load_db(sys.argv[1], ':memory:')
    (column_names, data) = util.select(conn)
    print(column_names)
    print(data[0])
