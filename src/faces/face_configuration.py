from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FaceConfiguration:
    happy_path: Path
    sad_path: Path
    diameter: int
