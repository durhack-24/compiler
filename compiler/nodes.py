from abc import ABC, abstractmethod
from dataclasses import dataclass


class Node(ABC):
    @abstractmethod
    def eval(self, context: dict[int, int | list[int]]):
        pass


class Value(Node, ABC):
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
class Print(Node):
    value: Value

    def eval(self, context: dict[int, int | list[int]]):
        value = self.value.eval(context)
        if isinstance(value, int):
            print(value)
            return
        print(''.join(map(chr, value)))


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
