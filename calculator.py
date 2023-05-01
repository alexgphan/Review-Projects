"""
=== Basic Calculator ===
Takes in an equation in the form of a string
and returns the answer as a float.

=== Recommended Starter Project ===
"""

import math
from typing import Any


class Calculator:

    def __init__(self) -> None:
        self.answer = 0

    """Creates a calculator with some basic functions between two 
    numbers while storing the most recent value as an answer.
    
    === Public Attributes ===
    answer:
        The most recent answer to a question.
    """

    # def __init__(self) -> None:
    #     self.answer = 0

    def clear(self) -> None:
        self.answer = 0

    def addition(self, first_num, second_num=None):
        """Returns <first_num> plus <second_num>.
        """
        if second_num is None:
            self.answer += first_num
            return self.answer
        else:
            self.answer = second_num + first_num
            return self.answer

    def subtraction(self, first_num, second_num=None):
        """Returns answer - first_num or first_num - second_num.
        """
        if second_num is None:
            self.answer -= first_num
            return self.answer
        else:
            self.answer = second_num - first_num
            return self.answer

    def multiplication(self, first_num, second_num=None):
        """Returns <first_num> or current answer multiplied with second_num.
        """
        if second_num is None:
            self.answer *= first_num
            return self.answer
        else:
            self.answer = second_num * first_num
            return self.answer

    def divide(self, first_num, second_num=None):
        """Returns current answer or <first_num> divided <second_num>.
        """
        if second_num is None:
            self.answer /= first_num
            return self.answer
        else:
            self.answer = first_num / second_num
            return self.answer

    def square_root(self, num=None):
        """Return the square_root of answer or of <num>"""
        if num is None:
            self.answer = math.sqrt(self.answer)
            return self.answer
        else:
            self.answer = math.sqrt(num)
            return self.answer

    def to_power(self, first_num, second_num=None):
        """Return the current answer or whatever num you chose to
        raise to the power of <power>.
        """
        if second_num is None:
            self.answer ^= first_num
            return self.answer
        else:
            self.answer = first_num ** second_num
            return self.answer


class Stack:
    """A basic Stack class mostly used to
    help with the calculate function
    """

    def __init__(self):
        """Initializes the stack.
        """
        self.stack = []

    def push(self, value: Any) -> None:
        """Adds the value to the top of the stack.
        """
        self.stack.append(value)

    def pop(self) -> Any:
        """Removes the top value from the stack and returns it.
        """
        removed_value = self.stack.pop()
        return removed_value

    def is_empty(self) -> bool:
        """Returns whether the stack is empty.
        """
        return self.stack == []


def calculate(str_input: str) -> float:
    """Takes an equation input and applies pemdas multiple times until a single
    integer remains.

    >>> calculate('5+5')
    10.0
    >>> calculate('7*10+30')
    100.0
    >>> calculate('7*10+30/10')
    73.0
    >>> calculate('-7^3')
    -343.0
    >>> calculate('-5.5*74')
    -407.0
    >>> calculate('5*(45+5)')
    250.0
    >>> calculate('108*(-1000-100/10)^3')
    -111272508000.0
    >>> calculate('(100+(30*4))')
    220.0
    >>> calculate('(100+(-40*3^(2^2)-100)/334)')
    90.0
    """
    chunks_of_nums_and_ops = []
    curr_value = 0.0
    previous_value = None
    for value in str_input:
        if value == '-':
            if not isinstance(previous_value, float) or curr_value == 0.0:
                chunks_of_nums_and_ops.append('-')
                curr_value = 1.0
            else:
                curr_value = 0.0
                chunks_of_nums_and_ops.append(value)
        elif value in '+/()*^':
            curr_value = 0.0
            chunks_of_nums_and_ops.append(value)
        elif value == '.':
            chunks_of_nums_and_ops[-1] += value
        else:
            previous_value = curr_value
            if curr_value == 0.0:
                chunks_of_nums_and_ops.append(value)
            else:
                chunks_of_nums_and_ops[-1] += value
            curr_value += float(value)

    # We need to check if it is a single number by
    # figuring out if there are any operators within.

    if '(' in chunks_of_nums_and_ops:
        start_point = chunks_of_nums_and_ops.index('(')

        # Issue with this is that nested brackets would mess with the end point.
        # Maybe create a stack that would keep track of
        # what depth the current bracket is at and then find the matching one
        # Maybe have to use the stack method, if so I need to get the index of
        # each bracket part.

        stack = Stack()
        stack.push('(')
        end_point = None

        for i in range(start_point + 1, len(chunks_of_nums_and_ops)):
            if not stack.is_empty():
                if chunks_of_nums_and_ops[i] == '(':
                    stack.push('(')
                elif chunks_of_nums_and_ops[i] == ')':
                    stack.pop()
                    end_point = i

        portion_of_equation = chunks_of_nums_and_ops[start_point + 1: end_point]
        recursable_portion = ''
        for snippet in portion_of_equation:
            recursable_portion += snippet
        replacement = str(calculate(recursable_portion))
        chunks_of_nums_and_ops[start_point] = replacement

        # Can't do a regular increasing index because removing values changes
        # the overall index.

        while end_point > start_point:
            chunks_of_nums_and_ops.pop(end_point)
            end_point -= 1

    elif '^' in chunks_of_nums_and_ops:
        location_of_exponent = chunks_of_nums_and_ops.index('^')

        power = chunks_of_nums_and_ops[location_of_exponent + 1]

        chunks_of_nums_and_ops[location_of_exponent - 1] = str(
            float(chunks_of_nums_and_ops[location_of_exponent - 1]) **
            float(power))

        # Remove has issues for duplicates since it removes the first instance.
        # That's why we shall use pop.

        chunks_of_nums_and_ops.pop(location_of_exponent + 1)
        chunks_of_nums_and_ops.pop(location_of_exponent)

    elif '*' in chunks_of_nums_and_ops:
        location_of_multiply = chunks_of_nums_and_ops.index('*')

        multiplier = chunks_of_nums_and_ops[location_of_multiply + 1]

        chunks_of_nums_and_ops[location_of_multiply - 1] = str(
            float(chunks_of_nums_and_ops[location_of_multiply - 1]) *
            float(multiplier))

        chunks_of_nums_and_ops.pop(location_of_multiply + 1)
        chunks_of_nums_and_ops.pop(location_of_multiply)

    elif '/' in chunks_of_nums_and_ops:
        location_divide = chunks_of_nums_and_ops.index('/')

        divider = chunks_of_nums_and_ops[location_divide + 1]

        chunks_of_nums_and_ops[location_divide - 1] = str(
            float(chunks_of_nums_and_ops[location_divide - 1]) / float(divider))

        chunks_of_nums_and_ops.pop(location_divide + 1)
        chunks_of_nums_and_ops.pop(location_divide)

    elif '+' in chunks_of_nums_and_ops:
        location_add = chunks_of_nums_and_ops.index('+')

        added_value = chunks_of_nums_and_ops[location_add + 1]

        chunks_of_nums_and_ops[location_add - 1] = str(float(
            chunks_of_nums_and_ops[location_add - 1]) + float(added_value))

        chunks_of_nums_and_ops.pop(location_add + 1)
        chunks_of_nums_and_ops.pop(location_add)
    elif '-' in chunks_of_nums_and_ops:
        locate_minus = chunks_of_nums_and_ops.index('-')

        subtracted_value = chunks_of_nums_and_ops[locate_minus + 1]

        chunks_of_nums_and_ops[locate_minus - 1] = str(float(
            chunks_of_nums_and_ops[locate_minus - 1]) - float(subtracted_value))

        chunks_of_nums_and_ops.pop(locate_minus + 1)
        chunks_of_nums_and_ops.pop(locate_minus)

    # After one operator check we want to see if there is only an int within the
    recursable_str = ''
    for values in chunks_of_nums_and_ops:
        recursable_str += values
    if len(chunks_of_nums_and_ops) == 1:
        return float(chunks_of_nums_and_ops[0])
    else:
        return calculate(recursable_str)


if __name__ == '__main__':
    print('Type an equation with no whitespace.')
    equation = input('Equation: ')
    print('The answer to your equation %s is %f' % (equation,
                                                    calculate(equation)))
