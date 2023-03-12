# WildcardPaths
## about 
Hello, this is a small project of mine i wanted to share.
I dont like the unix command find because of his large amount of options that i've always to lookup.
Those are in my opinion just overkill, if you just want to get file paths for certain files that match a simple pattern.
I developed this little cli application to help me. It's not perfect but perhaps your are excited.
# what is this project about?
An example query:
```
find "./*a*/file#
```
would return all paths from files inside a directory that contains an 'a' in his name and contains a file whose name start with "file" and end with a digit.
\
If there are multiple paths inside your file structure that match the given criteria you will endup with a list of possible paths.
\
Note: the *"* are inside *zsh* mandatory to signal zsh not to replace those by wildard matching.

## improve speed while using long wildcard paths
You could do theoretically something like this
```
find "/start/*/*/*/*/*/my_folder"
```
and it would work, but depending on how large your file structure is it could take some time.
\
You can improve the speed by adding some more information to reduce the search space:
```
find "/start/a?b*/*/folder/*u*/folder2/myfolder"
``` 
This works because the algortihm uses a top-down approach where it filters non matching folders early.

## example
![image](https://user-images.githubusercontent.com/95578637/224540445-3144e657-e48b-49e0-b67c-6a4e5aa6cd9e.png)
\
*Note: i aliased find with `python3 .../find.py`*

# Wildcards 

| Wildcard | Description | Supported |
|--------- | ----------- | --------- |
| * | zero or more characters | yes |
| ? | exactly one character | yes |
| # | excatly one number | yes |
| ** | zero or more folders with any name | NO | 

# Windows, Mac, ...
This has been developed so far only on ubuntu 22.04.
So other system might not work. 

# TODO
Things that could be improved
- the cli interface is very simple
- some way to add cli autocomplete
- add windows compatibility

# Disclaimer
- this is my first public contribution
