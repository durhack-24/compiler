from abc import ABC, abstractmethod
from dataclasses import dataclass


class Node(ABC):
    @abstractmethod
    def eval(self, context: dict[int, int | list[int]]):
        pass


class Value(Node, ABC):
    pass


@dataclass
class Label(Node):
    label: str

    def eval(self, context: dict[int, int | list[int]]):
        pass


@dataclass
class Variable(Value):
    index: int

    def eval(self, context: dict[int, int | list[int]]):
        return context[self.index]


@dataclass
class Constant(Value):
    value: int

    def eval(self, context: dict[int, int | list[int]]):
        return self.value


@dataclass
class Add(Node):
    dest: Variable
    src: Value

    def eval(self, context: dict[int, int | list[int]]):
        a = self.dest.eval(context)
        b = self.src.eval(context)
        context[self.dest.index] = a + b


@dataclass
class Sub(Node):
    dest: Variable
    src: Value

    def eval(self, context: dict[int, int | list[int]]):
        a = self.dest.eval(context)
        b = self.src.eval(context)
        context[self.dest.index] = a - b


@dataclass
class Mul(Node):
    dest: Variable
    src: Value

    def eval(self, context: dict[int, int | list[int]]):
        a = self.dest.eval(context)
        b = self.src.eval(context)
        context[self.dest.index] = a * b


@dataclass
class Div(Node):
    dest: Variable
    src: Value

    def eval(self, context: dict[int, int | list[int]]):
        a = self.dest.eval(context)
        b = self.src.eval(context)
        context[self.dest.index] = int(a // b)


@dataclass
class Mod(Node):
    dest: Variable
    src: Value

    def eval(self, context: dict[int, int | list[int]]):
        a = self.dest.eval(context)
        b = self.src.eval(context)
        context[self.dest.index] = a % b


@dataclass
class Exp(Node):
    dest: Variable
    src: Value

    def eval(self, context: dict[int, int | list[int]]):
        a = self.dest.eval(context)
        b = self.src.eval(context)
        context[self.dest.index] = a ** b


@dataclass
class Mov(Node):
    dest: Variable
    src: Value

    def eval(self, context: dict[int, int | list[int]]):
        context[self.dest.index] = self.src.eval(context)


@dataclass
class And(Node):
    dest: Variable
    src: Value

    def eval(self, context: dict[int, int | list[int]]):
        a = self.dest.eval(context)
        b = self.src.eval(context)
        context[self.dest.index] = a and b


@dataclass
class Or(Node):
    dest: Variable
    src: Value

    def eval(self, context: dict[int, int | list[int]]):
        a = self.dest.eval(context)
        b = self.src.eval(context)
        context[self.dest.index] = a or b


@dataclass
class Not(Node):
    dest: Variable

    def eval(self, context: dict[int, int | list[int]]):
        context[self.dest.index] = not self.dest.eval(context)


@dataclass
class Xor(Node):
    dest: Variable
    src: Value

    def eval(self, context: dict[int, int | list[int]]):
        a = self.dest.eval(context)
        b = self.src.eval(context)
        context[self.dest.index] = (a and not b) or (not a and b)


@dataclass
class Print(Node):
    value: Value

    def eval(self, context: dict[int, int | list[int]]):
        value = self.value.eval(context)
        if isinstance(value, int):
            print(value)
            return
        print(''.join(map(chr, value)))


@dataclass
class Input(Node):
    dest: Variable

    def eval(self, context: dict[int, int | list[int]]):
        target = []
        for char in input():
            target.append(ord(char))
        context[self.dest.index] = target + [0]


@dataclass
class GetArr(Node):
    dest: Variable
    index: Value
    array: Variable

    def eval(self, context: dict[int, int | list[int]]):
        index = self.index.eval(context)
        array = self.array.eval(context)
        if isinstance(array, int):
            array = [array]
        if len(array) <= index:
            context[self.dest.index] = 0
            return
        context[self.dest.index] = array[index]


@dataclass
class SetArr(Node):
    array: Variable
    index: Value
    value: Value

    def eval(self, context: dict[int, int | list[int]]):
        index = self.index.eval(context)
        value = self.value.eval(context)
        if self.array.index not in context:
            context[self.array.index] = [0] * index
        if isinstance(context[self.array.index], int):
            context[self.array.index] = [context[self.array.index]]
        if len(context[self.array.index]) <= index:
            context[self.array.index] += [0] * (index - len(context[self.array.index]) + 1)
        context[self.array.index][index] = value


class Jump(Exception):
    def __init__(self, label):
        self.label = label


@dataclass
class Goto(Node):
    label: int

    def eval(self, context: dict[int, int | list[int]]):
        raise Jump(self.label)


@dataclass
class JumpIf(Node):
    condition: Value
    label: int

    def eval(self, context: dict[int, int | list[int]]):
        if self.condition.eval(context):
            raise Jump(self.label)
