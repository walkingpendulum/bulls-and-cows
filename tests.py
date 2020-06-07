from typing import List

from main import loop, evaluate, EvaluationResult


class Gun:
    def __init__(self, *bullets: str):
        self.bullets: List[str] = list(bullets)[::-1]

    def __call__(self, prompt: str) -> str:
        return self.bullets.pop()

    def assert_empty(self) -> None:
        assert not self.bullets


def test_guess_1675():
    gun = Gun("1234", "5678", "5276", "5637")
    result = loop(ground_truth="1675", input_func=gun)

    gun.assert_empty()
    assert result == tuple("1675")


def test_evaluate():
    assert evaluate("1234", "1234") == EvaluationResult(bulls=4, cows=0)
    assert evaluate("1234", "1675") == EvaluationResult(bulls=1, cows=0)
