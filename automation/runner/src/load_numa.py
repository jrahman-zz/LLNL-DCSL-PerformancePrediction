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
