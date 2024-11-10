# Amazon Price Tracker
  
This is a Python project that retrieves the price of a product from Amazon based on the provided URL and converts it to your desired currency. The program fetches the product price and provides the converted value using the specified exchange rate.

## Features

- **Price Fetching**: Fetches the price of a product from Amazon using the product URL.
- **Currency Conversion**: Converts the price to any desired currency using live exchange rates.
- **Simple Command Line Interface (CLI)**: Use the script from the command line with minimal setup.

## Requirements

Before running the project, ensure you have the following installed:

- Python 3.x
- `requests` library (for making HTTP requests)
- `BeautifulSoup` from `bs4` (for scraping the Amazon page)
- `(any currency API you want)` (for currency conversion)

!! Notes !!
This script may not work for all Amazon product pages, as the structure of the page may change over time.
Make sure to respect Amazon's usage terms when scraping their site.
