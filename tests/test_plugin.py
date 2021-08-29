import pytest

from flexget.utils import qualities
from flexget.utils.qualities import QualityComponent
from flexget.utils.qualities import Requirements
from jsonschema import Draft4Validator as validator
from typing import Any
from typing import Generator
from typing import List
from typing import Tuple

from .test_example import patterns
from .utils import load_yaml_file
from traits.traits import Traits


@pytest.fixture(scope="module")
def config() -> dict[str, Any]:
    return load_yaml_file("examples/traits.yaml").get("traits")


def quality_asserts(
    quality_components: dict[str, QualityComponent]
) -> Generator[Tuple[int, List[int]], None, None]:
    for type, components in quality_components.items():
        _qualities = [id(x) for x in getattr(qualities, f"_{type}s", [])]
        for _id in [id(x) for x in components]:
            yield (_id, _qualities)


@pytest.fixture(scope="module")
def task() -> Traits:
    return Traits()


def test_on_task_start(task, config) -> None:
    task.on_task_start(None, config)
    for (original, current) in quality_asserts(task._original_qualities):
        assert original not in current


@pytest.mark.parametrize("pattern", patterns(), ids=str)
def test_requirements_allows(pattern) -> None:
    assert Requirements(pattern.name).allows(str(pattern))


def test_on_task_exit(task, config) -> None:
    task.on_task_exit(None, config)
    for (original, current) in quality_asserts(task._original_qualities):
        assert original in current


def test_schema_definition(task, config) -> None:
    validator.check_schema(task.schema)
    validator(task.schema).validate(config)
