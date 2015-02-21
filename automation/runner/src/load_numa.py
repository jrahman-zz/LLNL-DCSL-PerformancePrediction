import numa

def load_numa():
    """ Load information about core numbers and numa patterns """

    if not numa.available():
        raise Exception('Numa detection not available')

    max_node = numa.get_max_node()

    nodes = []
    for i in range(max_node + 1):
        nodes.append(numa.node_to_cpus(i))

    return nodes
