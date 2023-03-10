from pattern import Regex, Wildcard, PatternArray, WildcardPath
from pathlib import Path


def testRegex():
    p1 = Regex(r"\d{5}-\w{0,4}[abc]")
    assert p1.match("12345-wwwwc")
    assert p1.match("1235-wwwwc") == False

def testWildcard():
    # test Wildcard._convertToRegex
    assert Wildcard._convertToRegex("*#?") == r".*\d.", Wildcard._convertToRegex("*#?")

    p1 = Wildcard("*123#?")
    assert p1.match("abc1234b")
    assert p1.match("12300")
    assert p1.match("1230") == False
    assert p1.match("123a") == False

def testPatternArray():
    p1 = PatternArray(["a*", "*b", "?c?"])
    assert p1.match(["auu", "ccb", "acb"])
    
def testWildcardPath():
    p1 = WildcardPath(Path("./abc/a*b/b*c/*"))
    assert p1.root == Path("./abc/")
    assert p1.pattern == PatternArray(["a.*b", "b.*c", ".*"])



if __name__ == "__main__":
    testRegex()
    testWildcard()
