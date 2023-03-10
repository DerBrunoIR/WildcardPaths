import re 
from pathlib import Path 
from typing import Type, Any


class Pattern:
    """
    Interface for classes that want to implement any sort of textual comparison.
    All methods will raise a NotImplementedError when not implemented by a subclass.
    
    Methods
    -------
    match 
    __eq__

    """
    def match(self, _: str) -> bool:
        raise NotImplementedError()

    def __eq__(self, _) -> bool:
        raise NotImplementedError()


class Regex(Pattern):
    """
    This class allows to match regex patterns on given text.

    Attributes
    ----------
    pattern: re.Pattern 
        A compiled regex pattern 

    Methods
    -------
    __init__(self, pattern: str, flags: int = 0)
        undefined behaivoir if pattern isn't a regex string 
        flags is passed via re.compile(..., flags=flags)

    match(self, test: str) -> bool
        True if there was any match. 

    __eq__(self, other: Pattern) -> bool 
        True if other is instanciated with the same pattern and flags.

    """
    pattern: re.Pattern

    def __init__(self, pattern: str, flags: int=0):
        self.pattern = re.compile(pattern, flags=flags)

    def match(self, test: str) -> bool:
        match = self.pattern.match(test)
        return match is not None
    
    def __eq__(self, other: Pattern):
        if isinstance(other, Regex):
            return self.pattern == other.pattern 
        return False


class Wildcard(Pattern):
    """ 
    Wildcard implements wildcard like matching via the Regex Pattern class.
    Limitations are @_convertToRegex section.
    
    Methods 
    -------
    __new__(cls, pattern: str)
        creates an instance of the Regex class with the converted regex pattern. 

    _convertToRegex(pattern: str) -> str 
        converts a given wildcard string into regex pattern 
        working Wildcards:
            '*' - zero or more characters
            '?' - one character
            '#' - one number
        Implemention is inspired by "https://www.wikiwand.com/de/Wildcard_(Informatik)"

    """
    def __new__(cls, pattern: str) -> Regex:
        regex = cls._convertToRegex(pattern)
        return Regex(regex)

    @staticmethod
    def _convertToRegex(pattern: str) -> str:
        assert re.match(r"^[\d\w\s\*\?\#]+", pattern), pattern
        converted = pattern
        substitude = [
                    ("?", "."),
                    ("*", ".*"),
                    ("#", "\\d"),
                ]
        for (pat, repl) in substitude:
            converted = converted.replace(pat, repl)

        return converted


class PatternArray(Pattern):
    """ 
    This class allowes check weather a list of patterns match elements wise a given list of strings.
    
    Attributes 
    ----------
    patterns: list[Pattern] 
        list of patterns 

    Methods 
    ------- 
    __init__(self, patterns: list[Any])
        initiate with a list of patterns IMPLEMENTING the 'Pattern' interface!

    match(self, tests: list[str]) -> bool 
        This method checks weather all strings in the list match the pattern at the same index.

    __len__(self) -> int 
        returns the length of the pattern list

    __eq__(self, other: Pattern) -> bool
        returns True if other is an instance of PatternArray and both 'patterns' are equal

    """
    patterns: list[Any]

    def __init__(self, patterns: list[Any]):
        self.patterns = patterns 

    def match(self, tests: list[str]) -> bool:
        return all((
                pat.match(test) for (test, pat) in zip(tests, self.patterns)
            ))

    def __len__(self) -> int:
        return len(self.patterns)

    def __eq__(self, other: Pattern) -> bool:
        if isinstance(other, PatternArray):
            return self.patterns == other.patterns 
        return False
        

class WildcardPath:
    """
    This class allows to get all matching paths from the given wildcard path.

    Attribtues 
    ----------
    root: Path 
        represents the left part of the wildcard path where no wildcards are used.

    pattern: PatternArray 
        stores the selector elements as 'Wildcard's inside of an 'PatternArray'.
        A selector is the right part of an wildcard path which contains wildcards.

    Methods 
    -------
    __init__(self, path: Path)
        Initiate this a WildcardPath with a path, that can contain wildcard characters '*', '?' and '#'. More infomation at 'Wildcard'.

    matchingPaths(self)
        returns all matching paths 

    Static Methods  # mybe move them to a separate class? 
    --------------
    _extractRoot(path: Path) -> Path 
        returns the root path of the given wildcard path

    _extractSelector(path: Path) -> list[str]
        returns the selector of the given wildcard path

    _containsWildcards(path: Path) -> bool 
        returns weather the given path contains any wildcard characters

    _listPaths(root: Path, depth: int) -> list[Path] 
        returns all paths where depth is equal to the number of Path.parts relative to the root path.


    """
    pattern: PatternArray
    root: Path

    def __init__(self, path: Path):
        path = path.resolve()
        self.root = self._extractRoot(path)
        selector = self._extractSelector(path)
        self.pattern = PatternArray([Regex(x) for x in selector])

    @staticmethod 
    def _extractRoot(path: Path) -> Path:
        root = path
        while WildcardPath._containsWildcards(root):
            root = root.parent
        return root

    @staticmethod
    def _extractSelector(path: Path) -> list[str]:
        selector = []
        while WildcardPath._containsWildcards(path):
            selector.append(path.parts[-1])
            path = path.parent 
        return selector

    @staticmethod 
    def _containsWildcards(path: Path) -> bool:
        path_string = "".join(path.parts)
        match = re.search(r"[\*\?\#]", path_string)
        return match is not None
    
    @staticmethod 
    def _listPaths(root: Path, depth: int) -> list[Path]:
        queue: list[Path] = [root]
        while len(queue[-1].parts) <= depth:
            path = queue.pop(0)
            folders = (x for x in path.iterdir() if x.is_dir())
            queue.extend(folders)
        res = []
        for folder in queue:
            res.extend(folder.iterdir())
        return res

    def matchingPaths(self) -> list[Path]: 
        root = self.root 
        paths = self._listPaths(root, len(self.pattern))
        return list(
                filter(
                    lambda x: self.pattern.match(list(x.parts)), paths)
                )

        


