import glob

from Functions import read_daily_prices, aggregate_historical_prices, write_historical_prices


if __name__ == '__main__':
    daily_files = glob.glob('card_prices_*.txt')
    historical_prices = aggregate_historical_prices(daily_files)

    output_file = 'historical_card_prices.txt'
    write_historical_prices(historical_prices, output_file)

    print(f'Aggregated historical prices saved to {output_file}')
