from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FaceConfiguration:
    happy_path: Path
    angry_path: Path
    diameter: int
