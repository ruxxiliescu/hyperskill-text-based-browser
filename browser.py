import argparse
import os
import requests

from collections import deque
from bs4 import BeautifulSoup
from colorama import Fore

links_contents = {}


def access_links(input_url):
    if "https://" not in input_url:
        response = requests.get("https://" + input_url)
    else:
        response = requests.get(input_url)

    if response.status_code != 200:
        print(f'The URL returned {response.status_code}.')
        return None

    return response


def save_contents(directory_path, input_url):
    contents = parse_content(input_url)
    input_url = input_url.split(".")[0]
    with open(f"{directory_path}/{input_url}", "w") as file:
        file.write(contents)

    return contents


def parse_content(input_url):
    saved = ""
    lookup = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li']
    response = access_links(input_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for tag in soup.find_all(lookup):
        if tag.name == 'a':
            saved += f"{Fore.BLUE + tag.text}"
        else:
            saved += f"{tag.text}"

    return saved


def main():
    stack_pages = deque()

    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    args = parser.parse_args()

    if not os.access(args.directory, os.F_OK):
        os.mkdir(args.directory)

    while True:
        url = input()
        if "." in url:
            if url in links_contents:
                print(links_contents[url])
            else:
                links_contents[url] = save_contents(args.directory, url)
                stack_pages.append(links_contents[url])
                print(parse_content(url))
        elif url == "exit":
            break
        elif url == "back":
            if len(stack_pages) > 1:
                stack_pages.pop()
                print(stack_pages[-1])
            else:
                continue
        else:
            print("Invalid URL")


if __name__ == "__main__":
    main()
