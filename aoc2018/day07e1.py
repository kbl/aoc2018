from aoc2018 import readlines

lines = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""".split("\n")


class Step:
    def __init__(self, name, requires=None):
        self.name = name
        self.requires = []
        self.required_by = []
        if requires:
            self.requires.extend(requires)

    def after(self, other_node):
        self.requires.append(other_node)

    def before(self, other_node):
        self.required_by.append(other_node)

    def __repr__(self):
        if self.requires:
            return 'Step(%r, %r)' % (self.name, self.requires)
        return 'Step(%r)' % self.name

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return self.name == other.name


class Steps(dict):
    def __init__(self):
        self.steps = {}

    def __getitem__(self, key):
        if key in self.steps:
            return self.steps[key]
        node = Step(key)
        self.steps[key] = node
        return node

    def __len__(self):
        return len(self.steps)

    def values(self):
        return self.steps.values()

    def ready_to_go(self, already_finished):
        step_queue = []
        for step in self.steps.values():
            if all([r in already_finished for r in step.requires]):
                step_queue.append(step)
        return step_queue


def parse(lines, steps):
    for line in lines:
        line = line.split(' ')
        steps[line[7]].after(steps[line[1]])
        steps[line[1]].before(steps[line[7]])
    return steps


def enqueue_next_steps(ready_step, sequence, queue):
    for future_step in ready_step.required_by:
        already_done = future_step in sequence
        already_enqueued = future_step in queue
        all_required_steps_done = all([required_step in sequence for required_step in future_step.requires])
        if not already_done and not already_enqueued and all_required_steps_done:
            queue.append(future_step)
    queue.sort(reverse=True)


if __name__ == '__main__':
    steps = parse(readlines(), Steps())
    sequence = []

    queue = steps.ready_to_go(sequence)

    while queue:
        next_step = queue.pop()
        sequence.append(next_step)
        enqueue_next_steps(next_step, sequence, queue)

    print(''.join([s.name for s in sequence]))
