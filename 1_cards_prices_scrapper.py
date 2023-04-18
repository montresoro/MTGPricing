import requests
from datetime import datetime
import statistics

def get_card_prices(card_name, max_results=10):

    query = card_name.replace(' ', '+')
    url = f'https://api.scryfall.com/cards/search?q={query}'

    response = requests.get(url)

    prices = []
    if response.status_code == 200:
        # Load the JSON data
        data = response.json()
        cards = data.get('data', [])

        for card in cards:
            if card['name'].lower() == card_name.lower():
                usd_price = card.get('prices', {}).get('usd', None)
                prices.append(usd_price)
                # Stop after max_results
                if len(prices) >= max_results:
                    break
    return prices

def load_card_list(filename):
    with open(filename, 'r') as file:
        card_names = [line.strip() for line in file.readlines()]
    return card_names

if __name__ == '__main__':
    card_list_file = 'card_list.txt'
    card_names = load_card_list(card_list_file)

    timestamp = datetime.now().strftime('%Y-%m-%d')
    output_file = f'card_prices_{timestamp}.txt'

    with open(output_file, 'w') as file:
        for card_name in card_names:
            prices = get_card_prices(card_name, max_results=10)

            if prices:
                float_prices = [float(price) for price in prices if price is not None]

                # Calculate the median price
                median_price = statistics.median(float_prices) if float_prices else None

                file.write(f'{card_name}: ${median_price:.2f}\n' if median_price is not None else f'{card_name}: No prices found\n')
            else:
                file.write(f'{card_name}: Could not find any prices\n')

            file.write('\n')

    print(f'Results saved to {output_file}')