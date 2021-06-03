import os
from pathlib import Path 

class TestPcaps:
    def __init__(self) -> None:
        self.path = os.path.join(Path(__file__).resolve().parent)