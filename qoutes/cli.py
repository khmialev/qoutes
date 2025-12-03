import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Quotes.toscrape.com scraper"
    )

    parser.add_argument(
        "--config",
        default="config.json",
        help="Path to config.json (default: config.json)",
    )

    parser.add_argument(
        "--pages",
        type=int,
        help="Override number of pages to scrape",
    )

    parser.add_argument(
        "--output",
        help="Override output JSON file path",
    )

    parser.add_argument(
        "--author",
        help="Author name to search quotes for",
    )

    return parser.parse_args()
