import heapq
from dataclasses import dataclass


@dataclass
class Node:
    value: type
    frequency: type
    left_node: type = None
    right_node: type = None

    def __lt__(self, other):
        return self.frequency <= other.frequency

    def __add__(self, other):
        total_frequency = self.frequency + other.frequency
        return Node(None, total_frequency, self, other)

    def to_string(self, depth=0):
        indent = '-' * depth
        if self.value != None:
            return f'{indent} {self.frequency}: {self.value}\n'

        return f'{indent}{self.frequency}\n' + self.left_node.treeToString(depth + 1) + self.right_node.treeToString(depth + 1)

    def to_dictionary(self):
        # It's a stack to populate the dictionary in a depth first aproach
        nodes_stack = [(self, '')]
        result_dictionary = {}
        while nodes_stack:
            node, prefix = nodes_stack.pop(-1)
            if node.value != None:
                assert(node.value not in result_dictionary)
                result_dictionary[node.value] = prefix
            else:
                nodes_stack.append((node.left_node, prefix + '0'))
                nodes_stack.append((node.right_node, prefix + '1'))

        return result_dictionary



def huffman_tree(value_frequency_dictionary: dict):
    priority_queue = [Node(value, frequency)
                      for value, frequency in value_frequency_dictionary.items()]
    heapq.heapify(priority_queue)
    while len(priority_queue) > 1:
        less_frequent_node, second_less_frequent_node = heapq.heappop(
            priority_queue), heapq.heappop(priority_queue)
        heapq.heappush(priority_queue, less_frequent_node +
                       second_less_frequent_node)

    return priority_queue[0]


text = 'una frase para explorar la compresion optima'

character_frequency = {character: text.count(
    character) for character in set(text)}

tree = huffman_tree(character_frequency)

print(tree.to_dictionary())

# TODO: add metrics like entropy to test implementation