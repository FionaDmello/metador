import json
import sys
from pathlib import Path
from typing import Any, List, Mapping, Optional, Union

import jsonschema
from jsonschema.exceptions import ValidationError

from .log import log

#: JSON primitives
JSON_v = Union[None, bool, int, float, str]
#: Superficial JSON type (not recursive!) to have at least some annotations
UnsafeJSON = Union[JSON_v, List[JSON_v], Mapping[str, Any]]

#: recursive type alias for JSON (the one we'd like to use, but makes problems)
# JSON = Union[None, bool, int, float, str, List["JSON"], Mapping[str, "JSON"]]


def load_json(filename: Path) -> UnsafeJSON:
    with open(filename, "r") as file:
        return json.load(file)


def validate_json(instance: UnsafeJSON, schema: UnsafeJSON) -> Optional[str]:
    """Validate JSON against JSON Schema, on success return None, otherwise the error."""

    try:
        jsonschema.validate(instance, schema)
        return None
    except ValidationError as e:
        return e.message


def critical_exit(msg: str) -> None:
    log.critical(msg)
    sys.exit(1)
