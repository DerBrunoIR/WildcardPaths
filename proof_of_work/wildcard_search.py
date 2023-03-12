import os

"""
    wildcard_match 
    --------------
    pattern: str
    test: str
    return: bool
    Tests weather the wildcard filled pattern does match the given test string.
"""
def wildcard_match(pattern: str, test: str, ignoreCase=False) -> bool:
    def cmpChars(c1, c2):
        if ignoreCase:
            return c1.upper() == c2.upper()
        return c1 == c2

    if len(test) == 0:
        return len(pattern) == 0 or all([x == "*" for x in pattern])
    elif len(pattern) == 0:
        return False

    return max(
            cmpChars(pattern[0], test[0]) and wildcard_match(pattern[1:], test[1:], ignoreCase=ignoreCase),
            pattern[0] == '*' and wildcard_match(pattern[1:], test, ignoreCase=ignoreCase),
            pattern[0] == '*' and wildcard_match(pattern, test[1:], ignoreCase=ignoreCase),
            pattern[0] == '*' and wildcard_match(pattern[1:], test[1:], ignoreCase=ignoreCase), 
            )

"""
    matching_paths
    --------------
    root: str 
    path: str  This can contain wildcards, eg. './file*/*/a_unique_file.txt'
    returns All existing paths that match the given path

"""
def matching_paths(root: str, wpath: str) -> list[str]:
    assert os.path.exists(root)
    res = []
    pattern = wpath.split("/")[0]
    matches = [
           os.path.join(root, x) for x in os.listdir(root) if wildcard_match(pattern, x)
           ]
    nextPath = "/".join(wpath.split("/")[1:])
    # anchor
    if nextPath == "":
        return matches

    # recursion
    res = []
    for new_root in matches:
        if os.path.isdir(new_root):
            res += matching_paths(new_root, nextPath)

    return res
    
"""
    SearchController
    ----------------
    A Controller-Class to execute wildcard searchs
"""
class SearchController:
    def __init__(self, root: str = os.curdir):
        assert os.path.exists(root)
        self.root = root

    def search(self, wpath: str):
        return matching_paths(self.root, wpath)

if __name__ == "__main__":
    print(matching_paths("/home/bruno/Uni/21 WinterSemester", "Ein*/*woche*"))
