import numa

def load_numa():
    """ Load information about core numbers and numa patterns """

    if not numa.available():
        raise Exception('Numa detection not available')

    max_node = numa.get_max_node()

    nodes = {}
    for i in range(max_node + 1):
        nodes[i] = list(numa.node_to_cpus(i))

    return nodes

def assign_cores(app_core_req, intererence_core_reqs, client_core_req):
    nodes = load_numa()

    app_node = nodes.keys()[0]
    app_cores = nodes[app_node]
    other_cores = reduce(lambda x, y: x + nodes[y], nodes.keys()[1:], [])

    consumed_other_cores = 0
    consumed_app_cores = 0


def get_cores_new(app_request, interference_requests, client_requests):
    nodes = load_numa()

    app_node = nodes.keys()[0]
    app_node_cores = nodes[app_node]
    consumed_app_cores = 0
    other_node_cores = reduce(lambda x, y: x + nodes[y], nodes.keys()[1:], [])
    consumed_other_cores = 0

    # We need to find the largest request for same app cores
    consumed_app_cores = max(reduce(lambda x, y: x + [y[1]], filter(lambda x: x[0] == 0, interference_requests), [app_request]))
    app_cores = app_node_cores[0:app_request]

    interference_cores = []
    client_cores = []

    for core_request in interference_requests:
        (count, coloc) = core_request
        if coloc == 0:
            start = 0
            end = start + count
            available_cores = len(app_node_cores) 
            core_source = app_node_cores
        elif coloc == 1:
            start = consumed_app_cores
            end = start + count
            available_cores = len(app_node_cores) - consumed_app_cores
            core_source = app_node_cores
            consumed_app_cores = consumed_app_cores + count
        elif coloc == 2:
            start = consumed_other_cores
            end = start + count
            available_cores = len(other_node_cores) - consumed_other_cores
            core_source = other_node_cores
            consumed_other_cores = consumed_other_cores + count
        if count > available_cores:
            raise Exception('Too many requests for cores')
        interference_cores.append(core_source[start:end])

    for core_request in client_requests:
        if (core_request < len(other_node_cores) - consumed_other_cores):
            start = consumed_other_cores
            end = start + count
            cores = other_node_cores[start:end]
        

        client_cores.append(cores)

    return (app_cores, interference_cores, client_cores)


def get_cores(policy, num_app_cores, num_interference_cores, num_client_cores):
    nodes = load_numa()

    policies = available_collocation()
    if not policy in policies:
        raise Exception('Collocation policy not supported')

    if policy == 0:
        # Same core
        if len(nodes.keys()) > 1:
            start = 0
            end = num_client_cores
            client_node = nodes.keys()[1]
        else:
            start = max(num_app_cores, num_interference_cores)
            end = start + num_client_cores
            client_node = nodes.keys()[0]
        client_cores = nodes[client_node][start:end]

        interference_node = nodes.keys()[0]
        app_node = interference_node

        app_cores = nodes[app_node][0:num_app_cores]
        interference_cores = nodes[app_node][0:num_interference_cores]

    elif policy == 1:
        # Different cores, same socket

        if len(nodes.keys()) > 1:
            start = 0
            end = num_client_cores
            client_node = nodes.keys()[1]
        else:
            start = num_interference_cores + num_app_cores
            end = start + num_client_cores
            client_node = nodes.keys()[0]
            # Make an adjustment if we run off the end
            if end >= len(nodes[client_node]):
                start = start - (end - len(nodes[client_node]))
                end = start + num_client_cores
        client_cores = nodes[client_node][start:end]
        
        app_node = nodes.keys()[0]
        interference_node = app_node

        app_cores = nodes[app_node][0:num_app_cores]
        start = num_app_cores
        end = start + num_interference_cores
        interference_cores = nodes[interference_node][start:end]

    elif policy == 2:
        # Different sockets
        try:
            app_node = nodes.keys()[0]
            app_cores = nodes[app_node][0:num_app_cores]
        except Exception as e:
            raise Exception('Too few cores on application node')

        try:
            inteference_node = nodes.keys()[1]
            interference_nodes = nodes[interference_node][0:num_interference_cores]
        except Exception as e:
            raise Exception('Too few cores on interference node')

        try:
            if len(nodes.keys()) > 2:
                node = 'client'
                client_node = nodes.keys()[2]
                start = 0
                end = num_client_cores
            else:
                node = 'interference'
                client_node = nodes.keys()[1]
                start = interference_cores
                end = start + num_client_cores
            client_cores = nodes[client_node]
        except Exception as e:
            raise Exception('Too few cores for client on %s node' % node)
    else:
        raise Exception('Bad policy: %s' % policy)

    return (app_cores, interference_cores, client_cores)

def available_collocation():
    nodes = load_numa()
    policies = [0]

     # Check for multi-cores (policy 1)
    for node in nodes.values():
        if len(node) > 1:
            policies.append(1)
            break

    # Check for multi-node (policy 2)
    if len(nodes) > 1:
        policies.append(2)
    
    return set(policies)

def main():
    print get_cores_new(2, [(0, 1), (0, 2), (1, 2)], [2])

if __name__ == '__main__':
    main()
