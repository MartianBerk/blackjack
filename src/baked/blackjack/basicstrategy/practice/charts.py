from baked.blackjack.basicstrategy.practice.hands import FullPractice
from baked.blackjack.basicstrategy.service import Service as BasicStrategyService
from baked.blackjack.model.model import Play


def full_practice_chart():
    practice = FullPractice()
    service = BasicStrategyService()

    chart = []
    header = []
    row = []

    render_card = lambda c: str(c.value) if c.value < 10 else ("T" if c.value < 11 else "A")
    render_cards = lambda c1, c2: f"{render_card(c1)}{render_card(c2)}"
    render_play = lambda p: {Play.HIT: "H", Play.STAND: "S", Play.SPLIT: "P", Play.DOUBLE: "D", Play.SURRENDER: "X"}[p]

    for player_hand, dealer in practice:
        if header is not None:
            header.append(render_card(dealer))

        if header and len(header) == 10:
            chart.append(header)
            header = None

        row.append(
            f"{render_cards(*player_hand)}:{render_play(service.get_play(player_hand, dealer))}"
        )

        if len(row) == 10:
            chart.append(row)
            row = []

    return chart
