
from typing import List


class Cat:
    """
    I am just a gato
    """
    def __init__(self, name, age):
        """
        Args:
            name:
            age:
        """
        self._name: str = name
        self._age:  int = age

    def sit(self):
        """
        (TODO : add description)

        """
        pass

    def rollOver(self):
        """
        (TODO : add description)

        """
        pass


class Opie(Cat):
    """
    I am Opie the cat
    """
    def __init__(self):
        """
        """
        super().__init__(name='Opie', age=15)

        self.__privateParts: List[str] = []
        self.publicEars:     float     = 1.0
        self._protectedTail: int       = 22

    def publicMethod(self, param1: float = 23.0) -> bool:
        """
        (TODO : add description)

        Args:
            param1:
        Returns:
            bool
        """
        ans: bool = False
        if param1 > 23:
            ans = False

        return ans
