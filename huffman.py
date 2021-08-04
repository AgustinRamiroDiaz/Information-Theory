# %%
import heapq
from dataclasses import dataclass
from math import log
# %%


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

    def average_length_per_symbol(self):
        """
        It equals the sum of all nodes in the tree minus 1,
        therefore one can sum up all but the leaves (or sum up all but the root)
        """
        nodes_stack = [self]
        result = 0
        while nodes_stack:
            node = nodes_stack.pop(-1)
            if node.value == None:
                result += node.frequency

                if node.left_node:
                    nodes_stack.append(node.left_node)
                if node.right_node:
                    nodes_stack.append(node.right_node)

        return result


# %%
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


# %%
message = 'una frase para explorar la compresion optima'

character_probability = {character: message.count(
    character)/len(message) for character in set(message)}

probability_distribution = [message.count(
    character)/len(message) for character in set(message)]

# %%


def calculate_entropy(probability_distribution):
    probability_times_information = [probability * log(probability, 2)
                                     for probability in probability_distribution]

    entropy = -sum(probability_times_information)
    return entropy

# %%


tree = huffman_tree(character_probability)


encode_dictionary = tree.to_dictionary()
decode_dictionary = {value: key for key, value in encode_dictionary.items()}

average_length_per_symbol = sum([len(encode_dictionary[character]) * probability for character, probability in character_probability.items()])
entropy = calculate_entropy(probability_distribution)
assert(entropy <= average_length_per_symbol)    # But should be close

assert(abs(average_length_per_symbol - tree.average_length_per_symbol()) < 0.001)

# %%


def en_d_ecode(message, dictionary):
    result = []
    temporary = ''
    for letter in message:
        temporary += letter
        if temporary in dictionary:
            result.append(dictionary[temporary])
            temporary = ''

    return ''.join(result)


# %%
encoded_message = en_d_ecode(message, encode_dictionary)
decoded_message = en_d_ecode(encoded_message, decode_dictionary)

assert(message == decoded_message)
print(decoded_message)
print(encoded_message)

