import util

def get_interference(conn, where='', orderby=''):
    return util.select_distinct(conn, 'interference', where, orderby)

def get_nice(conn, where='', orderby=''):
    return util.select_distinct(conn, 'nice', where, orderby)

def get_cores(conn, where='', orderby=''):
    return util.select_distinct(conn, 'cores', where, orderby)

def get_applications(conn, where='', orderby=''):
    return util.select_distinct(conn, 'application', where, orderby)
