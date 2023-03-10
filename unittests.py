from wildcard_search import wildcard_match, matching_paths
import os

def test(func):
    def wrapper(*args, **kwargs):
        print("running test:", func.__name__)
        return func(*args, **kwargs)
    return wrapper

@test
def test_wildcard_match():
    assert wildcard_match("abc", "abc")
    assert wildcard_match("abc*", "abcdefg")
    assert wildcard_match("*abc", "aaabc")
    assert wildcard_match("ab*ab", "abababababab")
    assert wildcard_match("a*", "b") == False
    assert wildcard_match("**", "")
    assert wildcard_match("*ddd", "ddde", ignoreCase=True) == False
    assert wildcard_match("*dDd", "ddd", ignoreCase=True)
    assert wildcard_match("b*", "bin")

@test
def test_matching_paths():
    df = lambda path, pattern: set([
        os.path.join(path, x) for x in os.listdir(path) if wildcard_match(pattern, x)
        ])
    test = lambda root, path: set(matching_paths(root, path))

    assert test("/", "b*") == df("/", "b*")
    assert test("/", "b*/w*") == df("/bin", "w*").symmetric_difference(df("/boot/", "w*"))




def main():
    test_wildcard_match()
    test_matching_paths()
    
    

if __name__ == "__main__":
    main()
