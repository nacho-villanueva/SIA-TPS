from typing import Callable, TypeVar, Generic, Union

ParametersType = TypeVar('ParametersType')
ReturnType = TypeVar('ReturnType')

# Nefasto, pero es lo que hay.
FunctionType1 = Callable[[ParametersType], ReturnType]
FunctionType2 = Callable[[ParametersType, ParametersType], ReturnType]
FunctionType = Union[FunctionType1, FunctionType2]


class Function(Generic[ParametersType, ReturnType]):
    def __init__(self, f: FunctionType, df: FunctionType):
        self.f = f
        self.df = df
