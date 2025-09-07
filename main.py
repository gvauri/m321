import travel as t
import cargo

while True:
    t.travel_position_and_mine(49900, 76828, laser_amplifier=1, laser=0.5)
    t.travell_position_and_sell_all(12641, 5554, "20-B")
    if cargo.get_hold_size() - cargo.get_free_hold() > 10:
        t.travell_and_sell_all()

# while True:
#     t.travel_and_buy()
#     t.travel_and_sell()

# while True:
#     t.travel_position_and_buy(5342, -5666, what="GOLD")
#     t.travell_and_sell_all()
