#! /usr/bin/env python3

"""Agentomics: Common Data Types

A library of commonly used data types that emulate strong runtime type-
checking to guarantee safety and correctness of simulations

Author: Akhil Karra
"""

from dataclasses import dataclass


class TypedArray:
    """Custom array datatype that typechecks every element added or set"""
    def __init__(self, type_check, series_name: str | None = None, var_name: str | None = None):
        self.type_check = type_check
        self.series_name: str | None = series_name
        self.var_name: str | None = var_name
        self._array = []

    def _type_check(self, item):
        if not isinstance(item, self.type_check):
            raise TypeError(f"Item must be of type {self.type_check.__name__}")

    def append(self, item):
        self._type_check(item)
        self._array.append(item)

    def set_array(self, L: list):
        map(self._type_check, L)
        self._array = L

    def to_list(self, elementary_types=False):
        if elementary_types:
            return [x.to_val() for x in self._array]
        else:
            return self._array

    def __getitem__(self, index):
        if isinstance(index, slice):
            return TypedArray(self.type_check, self._array[index])
        return self._array[index]

    def __setitem__(self, index, item):
        self._type_check(item)
        self._array[index] = item

    def __add__(self, other):
        if not isinstance(other, TypedArray):
            raise TypeError("Can only concatenate with another TypedArray")
        # Check that all items in the other list are of the correct type
        map(self._type_check, other)
        # Return a new TypedArray with the combined items
        new_list = TypedArray(self.type_check)
        new_list._array = self._array + other._array
        return new_list

    def __eq__(self, other):
        if isinstance(other, list):
            return self._array == other
        if isinstance(other, TypedArray):
            return self._array == other._array
        return NotImplemented  # For unsupported types

    def __bool__(self):
        return bool(self._array)

    def __len__(self):
        return len(self._array)

    def __repr__(self):
        return repr(self._array)

    def print_subfields(self):
        print(f"{self.var_name} ({self.series_name}):")
        for item in self._array:
            print(f"  - {item}")


@dataclass(frozen=True)
class NonnegFloat:
    """Custom nonnegative float datatype to ensure that LLMs return
    reasonable nonnegative values to the recurring global state"""
    value: float

    def __post_init__(self):
        if self.value < 0.0:
            raise ValueError("Floating point number must be nonnegative")

    def __repr__(self):
        return repr(self.value)

    def to_val(self):
        return self.value


@dataclass(frozen=True)
class Percent:
    """Custom percent datatype to ensure that LLMs return reasonable
    percentage values to the recurring global state."""
    value: float
    name: str | None = None

    def __post_init__(self):
        if not (0.0 <= abs(self.value) <= 1.0):
            raise ValueError("Invalid percentage input")

    def __repr__(self):
        return repr(self.value * 100.0) + "%"

    def to_val(self):
        return self.value


@dataclass(frozen=True)
class NonnegPercent:
    """Custom nonnegative percent datatype to ensure that LLMs return reasonable
    percentage values to the recurring global state."""
    value: float

    def __post_init__(self):
        if not (0.0 <= self.value <= 1.0):
            raise ValueError("Invalid nonnegative percentage input")

    def __repr__(self):
        return repr(self.value * 100.0) + "%"

    def to_val(self):
        return self.value
