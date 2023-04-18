from Functions import read_historical_prices, plot_historical_prices

if __name__ == '__main__':
    aggregated_file = 'historical_card_prices.txt'
    historical_prices = read_historical_prices(aggregated_file)

    plot_historical_prices(historical_prices)
    print('Charts saved to the "charts" folder')
