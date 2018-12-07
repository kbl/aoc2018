from aoc2018 import readlines
from aoc2018.day07e1 import Step as S, lines, Steps as Ss, parse, enqueue_next_steps


CONSTANT_STEP_TIME = 60
NO_WORKERS = 5


class Step(S):
    def __init__(self, name, requires=None):
        super(Step, self).__init__(name, requires)
        self.required_time = ord(name) - 64


class Steps(Ss):
    def __init__(self):
        super(Steps, self).__init__()

    def __getitem__(self, key):
        if key in self.steps:
            return self.steps[key]
        node = Step(key)
        self.steps[key] = node
        return node


class Elf:
    def __init__(self, id):
        self.id = id
        self.works_on = None
        self.busy_for = 0

    def start(self, step):
        self.works_on = step
        self.busy_for = CONSTANT_STEP_TIME + step.required_time

    def tick(self):
        if self.is_busy():
            self.busy_for -= 1

    def finished_step(self):
        if self.is_idle():
            return

        done = self.busy_for == 0
        if done:
            item = self.works_on
            self._reset()
            return item

    def _reset(self):
        self.works_on = None
        self.busy_for = 0

    def is_idle(self):
        return self.works_on is None

    def is_busy(self):
        return not self.is_idle()


class Workers:
    def __init__(self, count):
        self.time = 0
        self.elves = [Elf(i) for i in range(count)]

    def tick(self):
        self.time += 1
        for e in self.elves:
            if e.is_busy():
                e.tick()

    def header(self):
        format_string  = '%5s' + '%9s' * len(self.elves) + '%27s%27s'
        values = ['Time'] + ['Worker %d' % (i + 1) for i in range(len(self.elves))] + ['Done', 'Queue']
        return format_string % tuple(values)


    def status(self, sequence, step_queue=None):
        format_string  = '%5s' + '%9s' * len(self.elves) + '%27s%27s'

        def step(e):
            if e.is_busy():
                return e.works_on.name
            return '.'

        sequence = ''.join([s.name for s in sequence])
        step_queue = ''.join([s.name for s in step_queue]) if step_queue else ''

        values = [self.time] + [step(e) for e in self.elves] + [sequence, step_queue]

        e1 = self.elves[0].works_on.name if self.elves[0].is_busy() else '.'
        e2 = self.elves[1].works_on.name if self.elves[1].is_busy() else '.'
        return format_string % tuple(values)

    def just_finished_steps(self):
        just_finished_steps = []

        for elf in self.elves:
            finished_step = elf.finished_step()
            if finished_step:
                just_finished_steps.append(finished_step)

        return sorted(just_finished_steps)

    def pick_tasks(self, tasks):
        for e in self.elves:
            if tasks and e.is_idle():
                task = tasks.pop()
                e.start(task)

    def busy(self):
        return any([e.is_busy() for e in self.elves])


if __name__ == '__main__':
    steps = parse(lines, Steps())
    steps = parse(readlines(), Steps())
    sequence = []
    step_queue = steps.ready_to_go(sequence)
    workers = Workers(NO_WORKERS)

    print(workers.header())

    while workers.busy() or step_queue:
        just_finished_steps = workers.just_finished_steps()
        sequence.extend(just_finished_steps)

        for step in just_finished_steps:
            enqueue_next_steps(step, sequence, step_queue)

        workers.pick_tasks(step_queue)
        print(workers.status(sequence, step_queue))
        workers.tick()

    print(workers.status(sequence))
    print(workers.time - 1, ''.join([s.name for s in sequence]))
