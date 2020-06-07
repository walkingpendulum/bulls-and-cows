import dataclasses
import itertools
import random
from typing import Tuple, TypeVar, Sequence, Iterable, List, Callable, Generator


@dataclasses.dataclass
class EvaluationResult:
    bulls: int
    cows: int


Symbol = TypeVar("Symbol")
Code = Sequence[Symbol]


def evaluate(ground_truth: Code, code: Code) -> EvaluationResult:
    matches = sum(a == b for a, b in zip(ground_truth, code))
    common = len(set(ground_truth) & set(code))
    return EvaluationResult(bulls=matches, cows=common - matches)


def restrict(
        restrictions: Sequence[Tuple[Code, EvaluationResult]],
        codes: Iterable[Code],
) -> Generator[Code, None, None]:
    def match(x: Code) -> bool:
        for base_code, target_result in restrictions:
            ev_result = evaluate(ground_truth=base_code, code=x)
            if ev_result != target_result:
                return False

        return True

    yield from (code for code in codes if match(x=code))


def ask_user(alphabet: Sequence[Symbol], size: int, input_func: Callable[[str], str] = input) -> Code:
    for _ in range(5):
        try:
            guess = input_func("Guess the number... ")

            assert len(guess) == size, f"Guess should be of size {size}, got {len(guess)}"
            assert set(guess) <= set(alphabet), f"Guess has invalid symbols: {', '.join(set(guess) - set(alphabet))}"
            return guess
        except AssertionError as e:
            print(e.args[0])
            continue
    else:
        raise RuntimeError("Too much failed attempts to ask user to guess.")


def loop(
        ground_truth: Code = None,
        alphabet: Sequence[Symbol] = tuple(map(str, range(10))),
        size: int = 4,
        input_func: Callable[[str], str] = input,
) -> Code:
    if ground_truth is None:
        ground_truth: Code = tuple(random.sample(alphabet, size))
        print(ground_truth)

    all_codes: List[Code] = list(itertools.permutations(alphabet, size))
    restrictions: List[Tuple[Code, EvaluationResult]] = []
    permitted_codes: List[Code] = all_codes
    while len(permitted_codes) > 1:
        guess = ask_user(alphabet=alphabet, size=size, input_func=input_func)
        ev_result = evaluate(ground_truth=ground_truth, code=guess)
        print(ev_result)
        restrictions.append((guess, ev_result))
        permitted_codes = list(restrict(restrictions=restrictions, codes=permitted_codes))
        print(len(permitted_codes), permitted_codes)

    return permitted_codes[0]
