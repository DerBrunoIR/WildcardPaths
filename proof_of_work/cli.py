from wildcard_search import SearchController
import click
import os

search = SearchController()

@click.command()
@click.argument("wpath")
def ls(wpath: str):
    paths = search.search(wpath)
    if len(paths) == 0:
        click.echo("Nothing found!")
    else:
        for p in paths:
            click.echo(p)
    return 

def cd(wpath: str):
    paths = search.search(wpath)
    if len(paths) == 0:
        click.echo("Nothing found!")
    elif len(paths) == 1:
        click.echo(f"cd {paths[0]}")
        os.chdir(paths[0])
    else:
        for p in paths:
            click.echo(p)
        click.echo("Too many possible paths!")
    return 



if __name__ == "__main__":
    ls()
