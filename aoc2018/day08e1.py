from aoc2018 import readlines


line = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"


class Node:
    def __init__(self, index):
        self.index = index
        self.children = []
        self.metadata = []

    def add_metadata(self, metadata):
        self.metadata = metadata
    
    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return "Node(%r, %r, %r)" % (self.index, self.children, self.metadata)

    def value(self):
        if self.children:
            value = 0
            for m in self.metadata:
                index = m - 1
                if index >= len(self.children):
                    continue
                value += self.children[index].value()
            return value

        return sum(self.metadata)
        

def parse(line):
    numbers = list(map(int, line.split()))
    print(numbers)

    def build_node(index, numbers):
        node = Node(index)

        num_children = numbers[0]
        metadata_size = numbers[1]
        consumed_numbers = 2

        for i in range(num_children):
            child_node, child_consumed = build_node(index + consumed_numbers, numbers[consumed_numbers:])
            consumed_numbers += child_consumed
            node.add_child(child_node)

        node.add_metadata(numbers[consumed_numbers:consumed_numbers + metadata_size])
        consumed_numbers += metadata_size

        return node, consumed_numbers

    return build_node(0, numbers)


if __name__ == '__main__':
    line = list(readlines())[0]
    tree, consumed = parse(line)
    print(line.split(), consumed)
    nodes = [tree]
    summed_metadata = 0
    while nodes:
        node = nodes.pop()
        nodes.extend(node.children)
        summed_metadata += sum(node.metadata)

    print(summed_metadata)
    print(tree.value())

