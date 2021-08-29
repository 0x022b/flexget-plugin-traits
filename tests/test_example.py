import pytest

from flexget.utils.qualities import QualityComponent
from typing import Generator
from typing import Tuple

from .utils import load_yaml_file


class QualityComponentMock(QualityComponent):
    def __init__(self, type: str, value: int, name: str, regexp: str) -> None:
        super().__init__(type, value, name, regexp)
        self._raw_regexp = regexp

    def __repr__(self) -> str:
        return "<{}(value={},name={},regexp={})>".format(
            self.type.title(), self.value, self.name, self._raw_regexp
        )

    def __str__(self) -> str:
        return f"{self.name}"


class QualityTestPattern:
    def __init__(self, type: str, name: str, pattern: str) -> None:
        self.type = type
        self.name = name
        self.pattern = pattern

    def __repr__(self) -> str:
        return "<{}(name={},pattern={})>".format(
            self.type.title(), self.name, self.pattern
        )

    def __str__(self) -> str:
        return f"{self.pattern}"


def patterns() -> Generator[QualityTestPattern, None, None]:
    content = load_yaml_file("tests/configuration.yaml")
    for type, quality in content.get("patterns").items():
        values = dict(content.get("defaults"))
        for name, identifiers in quality.items():
            for identifier in identifiers:
                values[type] = identifier
                for template in content.get("templates"):
                    if f"{{{type}}}" in template:
                        p = (
                            template.replace(".", " ")
                            .replace("-", "/")
                            .replace("{{audio}}", values["audio"])
                            .replace("{{codec}}", values["codec"])
                            .replace("{{color_range}}", values["color_range"])
                            .replace("{{resolution}}", values["resolution"])
                            .replace("{{source}}", values["source"])
                        )
                        yield QualityTestPattern(type, name, p.replace("/", " "))
                        p = p.replace("/", "-")
                        yield QualityTestPattern(type, name, p.replace(" ", "."))
                        yield QualityTestPattern(type, name, p.replace(" ", "-"))


def qualities() -> Generator[QualityComponentMock, None, None]:
    content = load_yaml_file("examples/traits.yaml")
    for type, quality in content["traits"].items():
        for name, props in quality.items():
            yield QualityComponentMock(
                type, props.get("value", 0), name, props.get("regexp", name)
            )


def quality_test_params() -> Generator[
    Tuple[QualityComponentMock, QualityTestPattern], None, None
]:
    for quality in qualities():
        for pattern in patterns():
            if quality.type == pattern.type:
                yield (quality, pattern)


@pytest.mark.parametrize("quality, pattern", quality_test_params(), ids=str)
def test_quality(quality, pattern) -> None:
    match = quality.regexp.search(pattern.pattern)
    if quality.name == pattern.name:
        assert match, f"'{quality}' should match '{pattern}'"
    else:
        assert not match, f"'{quality}' should not match '{pattern}'"
