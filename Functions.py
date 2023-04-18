from datetime import datetime
import matplotlib.pyplot as plt

def read_daily_prices(filename):
    prices = {}

    date_str = filename.split('_')[-1].split('.')[0]
    date = datetime.strptime(date_str, '%Y-%m-%d')

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            card_name, price = line.split(':')
            card_name = card_name.strip()
            price = price.strip()

            if price not in ("No prices found", "Could not find any prices"):
                price = float(price[1:])
                prices[card_name] = (date, price)

    return prices


def aggregate_historical_prices(daily_files):
    historical_prices = {}

    for daily_file in daily_files:
        daily_prices = read_daily_prices(daily_file)

        for card_name, (date, price) in daily_prices.items():
            if card_name not in historical_prices:
                historical_prices[card_name] = []

            historical_prices[card_name].append((date, price))

    return historical_prices


def write_historical_prices(historical_prices, output_file):
    with open(output_file, 'w') as file:
        for card_name, prices in historical_prices.items():
            file.write(f'{card_name}:\n')

            for date, price in prices:
                date_str = date.strftime('%Y-%m-%d')
                file.write(f'  {date_str}: ${price:.2f}\n')

            file.write('\n')


def read_historical_prices(filename):
    historical_prices = {}

    with open(filename, 'r') as file:
        card_name = None
        prices = []

        for line in file:
            line = line.strip()

            if not line:
                if card_name:
                    historical_prices[card_name] = prices
                    card_name = None
                    prices = []
                continue

            if not card_name:
                card_name = line[:-1]  # Remove the trailing colon
            else:
                date_str, price_str = line.split(':')
                date = datetime.strptime(date_str.strip(), '%Y-%m-%d')
                price = float(price_str.strip()[1:])  # Remove the dollar sign before converting to float
                prices.append((date, price))

    return historical_prices


def plot_historical_prices(historical_prices):
    num_cards = len(historical_prices)
    num_columns = 4
    num_rows = (num_cards + num_columns - 1) // num_columns

    fig, axes = plt.subplots(num_rows, num_columns, figsize=(20, num_rows * 5))
    fig.tight_layout(pad=5.0)

    for i, (card_name, prices) in enumerate(historical_prices.items()):
        row, col = divmod(i, num_columns)
        ax = axes[row, col]

        dates, price_values = zip(*prices)
        ax.plot(dates, price_values)
        ax.set_title(card_name)
        ax.set_xlabel('Date')
        ax.set_ylabel('Price (USD)')
        ax.tick_params(axis='x', rotation=45)

    # Remove empty subplots if there are any
    if num_cards % num_columns != 0:
        for j in range(num_cards, num_rows * num_columns):
            row, col = divmod(j, num_columns)
            fig.delaxes(axes[row, col])

    plt.savefig('charts/all_charts.png', bbox_inches='tight')
    plt.close(fig)