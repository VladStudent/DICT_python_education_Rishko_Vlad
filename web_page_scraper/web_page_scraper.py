import os
import string

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.nature.com/nature/articles"


def clean_filename(title):
    """
    Очищення назви файлу:
    - видалення пунктуації
    - заміна пробілів на _
    """

    translator = str.maketrans('', '', string.punctuation)
    clean_title = title.translate(translator)
    clean_title = clean_title.replace(' ', '_')

    return clean_title


def get_article_text(article_url):
    """
    Отримання тексту статті
    """

    response = requests.get(
        article_url,
        headers={'Accept-Language': 'en-US,en;q=0.5'}
    )

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'lxml')

    article_body = soup.find('div', class_=lambda x: x and 'body' in x)

    if article_body:
        return article_body.get_text(strip=True)

    return None


def save_article(page_folder, title, content):
    """
    Збереження статті у txt файл
    """

    filename = clean_filename(title) + ".txt"

    filepath = os.path.join(page_folder, filename)

    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)


def parse_page(page_number, article_type):
    """
    Парсинг однієї сторінки
    """

    params = {
        'sort': 'PubDate',
        'year': '2022',
        'page': page_number
    }

    response = requests.get(
        BASE_URL,
        params=params,
        headers={'Accept-Language': 'en-US,en;q=0.5'}
    )

    if response.status_code != 200:
        print(f"Failed to load page {page_number}")
        return

    soup = BeautifulSoup(response.text, 'lxml')

    articles = soup.find_all('article')

    folder_name = f"Page_{page_number}"

    os.makedirs(folder_name, exist_ok=True)

    for article in articles:

        article_type_tag = article.find(
            'span',
            {'data-test': 'article.type'}
        )

        if not article_type_tag:
            continue

        current_type = article_type_tag.text.strip()

        if current_type != article_type:
            continue

        title_tag = article.find(
            'a',
            {'data-track-action': 'view article'}
        )

        if not title_tag:
            continue

        title = title_tag.text.strip()

        article_link = title_tag.get('href')

        full_link = "https://www.nature.com" + article_link

        article_text = get_article_text(full_link)

        if article_text:
            save_article(folder_name, title, article_text)


def main():

    pages = int(input("Enter number of pages:\n"))
    article_type = input("Enter article type:\n")

    for page in range(1, pages + 1):
        parse_page(page, article_type)

    print("Saved all articles.")


if __name__ == "__main__":
    main()