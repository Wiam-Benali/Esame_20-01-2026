from dataclasses import dataclass

@dataclass
class Artist:
    id : int
    name : str
    num_album: int

    def __str__(self):
        return f"{self.id}, {self.name}, {self.num_album}"

    def __hash__(self):
        return hash(self.id)