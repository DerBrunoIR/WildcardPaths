import click
from pattern import WildcardPath 
from pathlib import Path
import logging

logging.basicConfig(level=logging.CRITICAL)

@click.command("find")
@click.argument("pathstr")
def split(pathstr: str):
    p = WildcardPath(Path(pathstr))
    click.echo("\n".join(map(str, p.matchingPaths())))

if __name__ == "__main__":
    split()

