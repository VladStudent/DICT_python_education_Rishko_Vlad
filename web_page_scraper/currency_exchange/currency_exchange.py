import requests


def get_rates(base_currency):
    """
    Отримання курсів валют із FloatRates
    """

    url = f"http://www.floatrates.com/daily/{base_currency.lower()}.json"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    return response.json()


def main():

    base_currency = input().lower()

    rates_data = get_rates(base_currency)

    if rates_data is None:
        print("Error while loading exchange rates.")
        return

    cache = {}

    if base_currency != "usd" and "usd" in rates_data:
        cache["usd"] = rates_data["usd"]["rate"]

    if base_currency != "eur" and "eur" in rates_data:
        cache["eur"] = rates_data["eur"]["rate"]

    while True:

        target_currency = input().lower()

        if target_currency == "":
            break

        amount = float(input())

        print("Checking the cache...")

        if target_currency in cache:

            print("It is in the cache!")

            rate = float(cache[target_currency])

        else:

            print("Sorry, but it is not in the cache!")

            if target_currency not in rates_data:
                print("Currency not found.")
                continue

            rate = float(rates_data[target_currency]["rate"])

            cache[target_currency] = rate

        result = round(amount * rate, 2)

        print(f"You received {result} {target_currency.upper()}.")

    if __name__ == "__main__":
        main()