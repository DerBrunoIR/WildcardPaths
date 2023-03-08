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
            cmpChars(pattern[0], test[0]) and wildcard_match(pattern[1:], test[1:]),
            pattern[0] == '*' and wildcard_match(pattern[1:], test),
            pattern[0] == '*' and wildcard_match(pattern, test[1:]),
            pattern[0] == '*' and wildcard_match(pattern[1:], test[1:]), 
            )

   
def matching_paths(root: str, path: str):
    assert os.path.exists(root)
    res = []
    pattern = path.split("/")[0]
    matches = [
           os.path.join(root, x) for x in os.listdir(root) if wildcard_match(pattern, x)
           ]
    nextPath = "/".join(path.split("/")[1:])
    # anchor
    if nextPath == "":
        return matches

    # recursion
    res = []
    for new_root in matches:
        if os.path.isdir(new_root):
            res += matching_paths(new_root, nextPath)

    return res
    

if __name__ == "__main__":
    print(matching_paths("/home/bruno/Uni/21 WinterSemester", "Ein*/*woche*"))
