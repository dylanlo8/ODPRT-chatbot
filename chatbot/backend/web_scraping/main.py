from script import scrape_nested_links


def main():
    urls = ["https://nus.edu.sg/research/odprt-home"]
    for url in urls:
        scrape_nested_links(url, depth=2)


if __name__ == "__main__":
    main()
