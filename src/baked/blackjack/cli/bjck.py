import click

from baked.blackjack.basicstrategy.service import Chart, Service as BasicStrategy
from baked.blackjack.cli.practice import strategy_decks, strategy_practice


@click.group()
def bjck():
    pass


@bjck.command()
@click.argument("chart")
def chart(chart: str):
    bs = BasicStrategy()
    chart = bs.get_chart(Chart(chart.upper()))
    for row in chart:
        print("\t".join(row))


@bjck.command()
@click.option("--double-down", default=True)
@click.option("--double-after-split", default=False)
@click.option("--surrender", default=False)
@click.option("--ignore", default="")
@click.option("--decks", default=0)
def strategy(double_down: bool, double_after_split: bool, surrender: bool, ignore: str, decks: int):
    if decks:
        strategy_decks(double_down, double_after_split, surrender, ignore, decks)
    else:
        strategy_practice(double_down, double_after_split, surrender, ignore)


if __name__ == "__main__":
    bjck()
