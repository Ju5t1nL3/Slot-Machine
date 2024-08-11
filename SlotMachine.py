"""
Allows the user to play a slot machine.
"""

from decimal import *
import time
import random

UP_ONE = "\033[1A"
CLEAR_LINE = "\033[K"

UP_AND_CLEAR = UP_ONE + CLEAR_LINE

MAX_LINES = 3
MIN_BET = 100
MAX_BET = 1000

ROWS = 3
COLUMNS = 3

symbol_count = {
    "A": 1,
    "B": 1,
    "C": 1,
    "D": 2,
    "E": 5,
}

symbol_values = {
    "A": 5,
    "B": 5,
    "C": 5,
    "D": 4,
    "E": 2,
}


def clear_input():
    time.sleep(1)
    print(f"{UP_AND_CLEAR}{UP_AND_CLEAR}{UP_ONE}")


def create_symbols_list(symbols):
    """
    Creates the list of symbols.
    """
    symbols_list = []
    for symbol, count in symbols.items():
        for num in range(count):
            symbols_list.append(symbol)

    return symbols_list


def spin(rows, columns, symbols):
    """
    Spins the slot machine.
    """
    symbols_copy = symbols[:]
    all_columns = []
    for col in range(columns):
        column_list = []
        for row in range(rows):
            random_symbol = random.choice(symbols_copy)
            index = symbols_copy.index(random_symbol)
            popped = symbols_copy.pop(index)
            column_list.append(popped)
        all_columns.append(column_list)

    return all_columns


def print_results(table):
    """
    Prints the results of the slot machine.
    """
    rows = len(table[0])
    for row in range(rows):
        for i, col in enumerate(table):
            if i == 0:
                print(col[row], end="")
            else:
                print(f" | {col[row]}", end="")
        print()


def check_winnings(lines, results,  bet, values):
    """
    Checks how much the user won and returns the winnings, as well as which rows they won.
    """
    winnings = 0
    winning_rows = []
    for line in lines:
        complete_row = True
        symbol = ""
        for i, col in enumerate(results):
            if i == 0:
                symbol = col[line - 1]
            else:
                if col[line - 1] != symbol:
                    complete_row = False
        if complete_row:
            winnings += bet * values[symbol]
            winning_rows.append(line)

    return winnings, winning_rows


def get_deposit():
    """"
    Gets the user's deposit.
    """
    while True:
        try:
            deposit = Decimal(
                input(f"How much money would you like to deposit? "))
            deposit_exponent = deposit.as_tuple().exponent
            if deposit_exponent < -2:
                print("There are too many numbers after the decimal place. Try again.")
                clear_input()
            elif deposit < MIN_BET:
                print(f"Amount must be greater than the minimum bet (${
                      MIN_BET}). Try again.")
                clear_input()
            else:
                return float(deposit)

        except InvalidOperation:
            print("That is not a decimal. Try again.")
            clear_input()


def get_lines():
    """
    Gets which lines the user wants to bet on.
    """
    while True:
        try:
            lines = input(f"Which lines would you like to bet on (1 - {str(
                MAX_LINES)}? Put a space between each line number e.g., 1 4 5: ").strip().split(" ")
            if all(1 <= int(line) <= MAX_LINES for line in lines):
                lines = [int(line) for line in lines]
                return lines, len(lines)
            else:
                print(
                    f"You can only bet on 1 - {str(MAX_LINES)} lines. Try again.")
                clear_input()

        except ValueError:
            print("That is not an integer. Try again.")
            clear_input()


def get_bet():
    """
    Gets the amount the user wants to bet on per line.
    """
    while True:
        try:
            bet = Decimal(input(f"How much money would you like to bet on each line (${\
                          MIN_BET} - ${MAX_BET})? "))
            bet_exponent = bet.as_tuple().exponent
            if bet_exponent < -2:
                print("There are too many numbers after the decimal place. Try again.")
                clear_input()
            elif bet < MIN_BET or bet > MAX_BET:
                print(f"Amount must be between {\
                      MIN_BET} and {MAX_BET}. Try again.")
                clear_input()

            else:
                return float(bet)

        except InvalidOperation:
            print("That is not a decimal. Try again.")
            clear_input()


def check_bet(deposit, lines):
    """
    Checks if the bet is valid.
    """
    while True:
        bet = get_bet()
        if bet * lines > deposit:
            print(f"You did not deposit enough money to make that bet. Try again.")
            clear_input()
        else:
            return bet


def one_round(deposit):
    """
    Plays one round of the slot machine
    """
    lines, total_lines = get_lines()
    bet = check_bet(deposit, total_lines)
    total_bet = bet * total_lines
    print(f"You are betting ${bet:.2f} on each line.\nLines:", *
          lines, f"(Total: {total_lines})\nTotal Bet: ${total_bet:.2f}")
    symbols = create_symbols_list(symbol_count)
    results = spin(ROWS, COLUMNS, symbols)
    print_results(results)
    winnings, winning_rows = check_winnings(lines, results, bet, symbol_values)
    net = winnings - total_bet
    if net < 0:
        net_temp = f"-${abs(net)}"
    else:
        net_temp = f"${str(net)}"
    print(f"You won ${winnings}. Net earnings: {\
          net_temp}\nWinning rows: ", *winning_rows)
    return net


def main():
    """
    Runs the program
    """
    answer = "y"
    deposit = get_deposit()
    while answer == "y":
        net = one_round(deposit)
        deposit += net
        print(f"Total Balance: ${deposit:.2f}")
        if deposit <= 0:
            print("You are out of money.")
            break
        while True:
            answer = input(
                "Would you like to continue playing? (Y/N): ").lower().strip()
            if answer == "y" or answer == "n":
                break
            else:
                print("That is not an accepted answer. Try again.")
                clear_input()

    print(f"You left with ${deposit:.2f}")


main()  # starts program
