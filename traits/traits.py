from flexget import plugin
from flexget.event import event
from flexget.utils import qualities
from flexget.utils.qualities import QualityComponent
from loguru import logger
from typing import List


logger = logger.bind(name="traits")


class Traits:
    """
    Override FlexGet's built-in quality requirement types with new ones.

    Example:

    traits:
      audio:
        opus:
          value: 25
          regexp: opus(?:[1-7]\\.[01])?
    """

    schema = {
        "type": "object",
        "properties": {
            "audio": {"$ref": "#/$defs/qualities"},
            "codec": {"$ref": "#/$defs/qualities"},
            "color_range": {"$ref": "#/$defs/qualities"},
            "resolution": {"$ref": "#/$defs/qualities"},
            "source": {"$ref": "#/$defs/qualities"},
        },
        "additionalProperties": False,
        "$defs": {
            "qualities": {
                "type": "object",
                "minProperties": 1,
                "additionalProperties": {
                    "type": "object",
                    "properties": {
                        "value": {"type": "integer"},
                        "regexp": {"type": "string"},
                        "modifier": {"type": "integer"},
                    },
                    "required": ["value"],
                    "additionalProperties": False,
                },
            },
        },
    }

    def __init__(self) -> None:
        self._custom_qualities = {}
        self._original_qualities = {}
        for type in ["audio", "codec", "color_range", "resolution", "source"]:
            self._original_qualities[type] = getattr(qualities, f"_{type}s", []).copy()

    def on_task_start(self, task, config) -> None:
        self._custom_qualities = {}
        for type, components in config.items():
            if getattr(qualities, f"_{type}s", None):
                self._custom_qualities[type] = [
                    QualityComponent(
                        type,
                        props.get("value"),
                        name,
                        props.get("regexp", name),
                        props.get("modifier", None),
                        props.get("defaults", None),
                    )
                    for name, props in components.items()
                ]

                setattr(qualities, f"_{type}s", self._custom_qualities[type])

        count = self._update_registry(self._custom_qualities.values())
        logger.debug("Registry updated with {} custom qualities", count)

    def on_task_exit(self, task, config) -> None:
        for type in config.keys():
            if getattr(qualities, f"_{type}s", None):
                setattr(qualities, f"_{type}s", self._original_qualities[type])

        count = self._update_registry(self._original_qualities.values())
        logger.debug("Registry updated with {} original qualities", count)

    on_task_abort = on_task_exit

    def _update_registry(self, values: List[List[QualityComponent]]) -> int:
        registry = {v.name: v for v in (y for x in values for y in x)}
        setattr(qualities, "_registry", registry)
        return len(registry)


@event("plugin.register")
def register_plugin() -> None:
    plugin.register(Traits, "traits", api_ver=2)
    logger.info("Plugin registered")
