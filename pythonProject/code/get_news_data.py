from bs4 import BeautifulSoup
import requests
import re
import textwrap

CLEANCC             = re.compile(r'[\r\n\t]')  # Control characters to eliminate
CLEANTAG            = re.compile('<.*?>')      # Any HTML tag to eliminate

def cleancc(raw_html: str) -> str:
    """
    Removes control characters from raw_html

    :param raw_html: String with embedded control characters
    :return: String without control characters

    From: https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
    """
    return CLEANCC.sub('', raw_html)

def cleantag(line: str) -> str:
    """Removes any HTML tag"""
    return CLEANTAG.sub('', line)

news_groups = 0  # Count of news postings
news_lines  = 0  # Total lines of news text

# Extract text, href, and description from news page.

response = requests.get("https://www.dangribbin.com/news")
web_page = response.text
html = BeautifulSoup(web_page, "html.parser")

with open("news.txt", mode="w", encoding="utf8") as news_file:

    outer_table = html.find("table", height="460")
    inner_row = outer_table.find("tr", height="300")
    next_td = inner_row.next_element.next_element
    next_td = next_td.next_sibling.next_element.next_element
    central_table = next_td.next_element.next_element

    # Process first news header and text
    # Each table row contains two inner tables
    next_table_row = central_table.tr  # First table row
    # The first inner table contains heading and date posted
    news_groups += 1  # Count news group
    header_row = next_table_row.td.table.tr  # ignore <tbody> between <table> and <tr> tag
    heading = header_row.td.span.text
    news_file.write(f"{heading}\n")
    posted = cleancc(header_row.td.next_sibling.next_element.text)  # Strip leading and trailing \n \t
    news_file.write(f"{posted}\n")  # Date of posting
    # The second inner table contains text posting
    posting = list(central_table.tr.td.table.next_sibling.next_element.tr.td.span.stripped_strings)
    for line in posting:
        if line [ 0:5 ] == "_____":
            continue  # Ignore separator line
        else:
            news_file.write(f"{line}\n")
            news_lines += 1  # Count news lines
        # endif
    # end for loop

    # Get next news posting
    next_table_row = next_table_row.next_sibling.next_element
    while next_table_row.name == "tr":
        news_groups += 1  # Count news group
        header_row = next_table_row.td.table.tr
        heading = header_row.td.span.text
        news_file.write(f"\n{heading}\n")
        posted = cleancc(header_row.td.next_sibling.next_element.text)
        news_file.write(f"{posted}\n")  # Date of posting
        posting = list(next_table_row.td.table.next_sibling.next_element.tr.td.span.stripped_strings)
        for line in posting:
            if line[0:5] == "_____":
                continue            # Ignore line
            else:
                news_file.write(f"{line}\n")
                news_lines += 1  # Count news lines
            # endif
        # end for loop
        next_table_row = next_table_row.next_sibling.next_element
    # end while loop


print("")
print(f"{news_groups} news groups")
print(f"{news_lines}  news lines")


