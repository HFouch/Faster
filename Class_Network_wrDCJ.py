from Class_wrDCJ_Node import Node
from networkx import DiGraph
from Class_extremities_and_adjacencies import Extremities_and_adjacencies
import time

class Network:

    def __init__(self, start_node, target_node, adjacenciesB):
        self.hash_table = {}
        self.start_node = start_node
        self.target_node = target_node
        self.adjacenciesB = adjacenciesB

        hash_key_start = hash(str(self.start_node.state))
        hash_key_target = hash(str(self.target_node.state))
        self.hash_table.update({hash_key_start: self.start_node})
        self.hash_table.update({hash_key_target: self.target_node})
        self.level = 0

        # Build network

    def build_hash_table(self, current_node):
        t0 = time.time()

        adjacenciesB = self.adjacenciesB

        get_adjacencies = Extremities_and_adjacencies()
        #print()
        node = current_node
        #print()
        #print()
        #print('current node and state: ')
        #print(node)
        #print(node.state)
        #print('____________________________________________________________________________________')

        #if the genome has a circular intermediate (i.e all of its children will be linear)
        if node.next_operation != 0:
            operation_type = None

            operations = []
            # if point of cut = previous point of join:
            if node.next_operation_weight == 0.5:

                operations.append(node.next_operation)
                operation_type = 'trp1'


            elif node.next_operation_weight == 1.5:
                operations = []
                if type(node.next_operation) is list:
                    for operation in node.next_operation:
                        operations.append(operation)
                else:
                    operations.append(node.next_operation)
                operation_type = 'trp2'


            else:
                print('You have got a problem with the .next_operation weights')



            for operation in operations:

                child_state = node.take_action(operation)[0]

                check_hash_table = Network.check_hash_key(self, child_state)

                if check_hash_table[0]:
                    child = check_hash_table[1]
                    node.children.append(child)
                    node.children_weights.append(node.next_operation_weight)
                    node.children_operations.append((operation, operation_type))
                   # print()
                   # print('Operation: ', operation)
                   # print('Type: ', operation_type)
                   # print(get_adjacencies.adjacencies_to_genome(node.state), '  ---->    ',
                    #      get_adjacencies.adjacencies_to_genome(child_state))


                else:
                    #remember the child will consist of linear chromosomes only because it is the result of a forced reinsertion
                    child = Node(child_state)
                    hash_key = hash(str(child.state))
                    self.hash_table.update({hash_key: child})
                    # print('#T: ', self.hash_table)
                    node.children.append(child)
                    node.children_weights.append(node.next_operation_weight)
                    node.children_operations.append((operation, operation_type))
                  #  print()
                  #  print('Operation: ', operation)
                  #  print('Type: ', operation_type)
                  #  print(get_adjacencies.adjacencies_to_genome(node.state), '  ---->    ',
                  #        get_adjacencies.adjacencies_to_genome(child_state))

                    Network.build_hash_table(self, child)


        #if the genome has no circular intermediates (i.e. some of its children may have circular chromosomes)
        else:

            operations = node.get_legal_operations(adjacenciesB)

            for operation in operations:

                operation_result = node.take_action(operation)
                child_state = operation_result[0]
                op_type = operation_result[1]


                check_hash_table = Network.check_hash_key(self, child_state)

                if check_hash_table[0]:
                    child = check_hash_table[1]
                    node.children.append(child)

                    # if the operation is a trp0
                    child.find_chromosomes(child.state)
                    if len(child.circular_chromosomes) != 0 :
                        node.children_weights.append(0.5)
                        node.children_operations.append((operation, 'trp0'))
                     #   print()
                     #   print('Operation: ', operation)
                     #   print('Type: ', 'trp0')
                     #   print(get_adjacencies.adjacencies_to_genome(node.state), '  ---->    ',
                     #         get_adjacencies.adjacencies_to_genome(child_state))

                    else:
                        #node.children_weights.append(1)
                        #if op_type == 'fis' or op_type == 'fus' or op_type == 'u_trl':
                        #    operation_type = op_type
                        #else:
                        #    operation_type = node.find_operation_type(operation)

                        if op_type == 'fis':
                            operation_type = op_type
                            op_weight = 2

                        elif op_type == 'fus':
                            operation_type = op_type
                            op_weight = 2

                        elif op_type == 'u_trl':
                            operation_type = op_type
                            op_weight = 1.5

                        else:
                            operation_type = node.find_operation_type(operation)
                            if operation_type == 'inv':
                                op_weight = 1
                            elif operation_type == 'b_trl':
                                op_weight = 1.5
                            else:
                                print("There's a problem at the .find_optype node function")

                        node.children_weights.append(op_weight)

                        node.children_operations.append((operation, operation_type))
                     #   print()
                     #   print('Operation: ', operation)
                     #   print('Type: ', operation_type)
                     #   print('weight: ', op_weight)
                     #   print(get_adjacencies.adjacencies_to_genome(node.state), '  ---->    ',
                     #         get_adjacencies.adjacencies_to_genome(child_state))
                     #   print(node.children_weights)





                else:
                    child = Node(child_state)

                    # check whether a circular chromosome has been created
                    child.find_chromosomes(child.state)


                    # if a circular chromosome has been created:
                    if len(child.circular_chromosomes) != 0:

                        legal_operation = child.get_legal_reinsertion_operation(operation, self.adjacenciesB)

                        if legal_operation:
                            child.next_operation = legal_operation
                            child.next_operation_weight = 0.5
                            hash_key = hash(str(child.state))
                            self.hash_table.update({hash_key: child})
                            # print('#T: ', self.hash_table)
                            node.children.append(child)
                            node.children_operations.append((operation, 'trp0'))
                            node.children_weights.append(0.5)
                         #   print()
                         #   print('Operation: ', operation)
                         #   print('Type: ', 'trp0')
                         #   print(get_adjacencies.adjacencies_to_genome(node.state), '  ---->    ',
                         #         get_adjacencies.adjacencies_to_genome(child_state))

                            Network.build_hash_table(self, child)
                        else:
                            child.next_operation = child.get_illegal_decircularization_operation(self.adjacenciesB)

                            child.next_operation_weight = 1.5
                            hash_key = hash(str(child.state))
                            self.hash_table.update({hash_key: child})
                            # print('#T: ', self.hash_table)
                            node.children.append(child)
                            node.children_operations.append((operation, 'trp0'))
                            node.children_weights.append(0.5)
                           # print()
                           # print('Operation: ', operation)
                           # print('Type: ', 'trp0')
                           # print(get_adjacencies.adjacencies_to_genome(node.state), '  ---->    ',
                           #       get_adjacencies.adjacencies_to_genome(child_state))

                            Network.build_hash_table(self, child)


                    # else if no circular chromosome has been created:
                    else:

                        hash_key = hash(str(child.state))
                        self.hash_table.update({hash_key: child})
                        # print('#T: ', self.hash_table)
                        node.children.append(child)

                        '''
                        if op_type == 'fis' or op_type == 'fus' or op_type == 'u_trl':
                            operation_type = op_type
                        else:
                            operation_type = node.find_operation_type(operation)

                        node.children_weights.append(1)
                        node.children_operations.append((operation, operation_type))
                        print()
                        print('Operation: ', operation)
                        print('Type: ', operation_type)
                        print(get_adjacencies.adjacencies_to_genome(node.stalen(child.circular_chromosomes)te), '  ---->    ',
                              get_adjacencies.adjacencies_to_genome(child_state))
                        
                        '''

                        if op_type == 'fis':
                            operation_type = op_type
                            op_weight = 2

                        elif op_type == 'fus':
                            operation_type = op_type
                            op_weight = 2

                        elif op_type == 'u_trl':
                            operation_type = op_type
                            op_weight = 1.5
                        else:
                            operation_type = node.find_operation_type(operation)
                            if operation_type == 'inv':
                                op_weight = 1
                            elif operation_type == 'b_trl':
                                op_weight = 1.5
                            else:
                                print("There's a problem at the .find_optype node function")

                        node.children_weights.append(op_weight)

                        node.children_operations.append((operation, operation_type))

                        Network.build_hash_table(self, child)



    def check_hash_key(self, child_state):
        key = hash(str(child_state))
        if key in self.hash_table.keys():
            return True, self.hash_table.get(key)
        return False, None

    def build_network(self):
        network = DiGraph()
        nodes = []
        weighted_edges = []
        weights = []

        Network.build_hash_table(self, self.start_node)
        list_of_values = self.hash_table.values()
        for value in list_of_values:
            if value not in nodes:
                nodes.append(value)
        for node in nodes:
            number_of_children = len(node.children)
            network.add_node(node)

            for i in range(0, number_of_children):
                weighted_edges.append((node, node.children[i], node.children_weights[i]))
                weights.append(node.children_weights[i])

        network.add_weighted_edges_from(weighted_edges)




        return network

