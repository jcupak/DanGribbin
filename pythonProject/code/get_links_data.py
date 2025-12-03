from bs4 import BeautifulSoup
import requests
import re

# Extract text, href, and description from all five (5) links.

response = requests.get("https://www.dangribbin.com/links")
web_page = response.text
html = BeautifulSoup(web_page, "html.parser")

pattern = re.compile(r"[\d]*[_][\d]*\.jpg$")

with open("album_info_links.csv", mode="w") as links_file:

    tables = html.find_all("table", width="647")
    for table in tables:
        table_rows = table.find_all('tr', height="300")
        for table_row in table_rows:
            row_height = table_row.get("height")
            if row_height == "300":
                # Find second TD with width="400"
                second_td = table_row.td.next_sibling.next_element.next_element
                td_width = second_td.get("width")
                inner_table = second_td.table
                spans = inner_table.find_all("span")
                for span in spans:
                    span_class = span.get("class")
                    if span_class[0] == "header3":
                        # Extract link text and href
                        link_name = span.text
                        links_file.write(f"{link_name}|")
                        span_link = span.fetchPrevious("a") # Enclosing <a> tag
                        link_href = span_link[0]["href"]
                        links_file.write(f"{link_href}|")
                    elif span_class[0] == "greyed":
                        # Extract link information
                        link_info = span.text
                        links_file.write(f"{link_info}\n")
                    # endif
                # end for span
            # endif row_height is 300
        # end for next_table_row
    # end table

