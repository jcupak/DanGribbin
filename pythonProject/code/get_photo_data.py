from bs4 import BeautifulSoup
import requests
import re

SEPARATOR = "|"  # Instead of a comma, because descriptions contain a comma
photos_filename = f"photos.csv"  # Album tracks file
photos_file = open(photos_filename, "w")

def get_photo_data(photo_number: int):
    """
    Extract photo filename, title, copyright year,
    the photographer/artist, and the description.

    :param photo_number: The number of the photos web page
    :return: nothing

    NOTE: The source photos/# web page is laid out as nested tables.
    Knowledge of the table column width and class is essential
    to finding and extracting the photo data.


    AUTHOR:  John J Cupak Jr

    EMAIL:   john.cupak@me.com

    CREATED: 2023-02-13
    """

    # Each photo and its information is on their own page
    photo_web_page = f"https://www.dangribbin.com/photos/{photo_number}"
    print(f"\nChecking {photo_web_page}")

    response = requests.get(photo_web_page)        # Where to go for photo data
    contents = response.text                       # Get photo web page contents
    html = BeautifulSoup(contents, "html.parser")  # Parse HTML

    # Part 1: Extract image name
    # Find all table <tr> row tags with height values
    table_trs = html.find_all('tr', height=True)
    for table_tr in table_trs:

        tr_height = table_tr["height"]            # Get tr height attribute

        # Check if table row height is 300
        if tr_height == "300":
            # print(f"TR Height: {tr_height}")      # Show tr height attribute
            table_td = table_tr.td.next_sibling.next_element.next_element

            td_width = table_td["width"]
            # print(f"TD Width:  {td_width}")

            # print(f"TD: {table_td.img['src']}")
            image_link = table_td.img["src"]  # Get image source
            # print(f"Image Link: {image_link}")

            # Write photo number to file
            photos_file.write(f"{photo_number}{SEPARATOR}")

            # Extract just image name using matching pattern
            pattern = r"[\d]*[_][\d]*\.jpg$"
            image_file = re.search(pattern, image_link).group()
            photos_file.write(f"{image_file}{SEPARATOR}")
            print(f"Image File:          {image_file}")

            # Find all <span> tags
            spans = table_td.find_all('span')
            for span in spans:
                span_class = span.get('class')[ 0 ]
                # print(f"span Class: {span_class}")
                if span_class == "header1":
                    span_label = span.string  # What is the header?
                    if span_label == "Title: ":
                        # Extract image title from next span
                        title = span.next_sibling.string
                        photos_file.write(f"{title}{SEPARATOR}")
                        print(f"Title:               {title}")
                    elif span_label == "Copyright: ":
                        # Extract image copyright year from next span
                        copyright_year = span.next_sibling.string
                        photos_file.write(f"{copyright_year}{SEPARATOR}")
                        print(f"Copyright:           {copyright_year}")
                    elif span_label == "Photographer/Artist: ":
                        # Extract image photographer/artist from next span
                        photographer_artist = span.next_sibling.string
                        photos_file.write(f"{photographer_artist}{SEPARATOR}")
                        print(f"Photographer/Artist: {photographer_artist}")
                    elif span_label == "Description: ":
                        # Extract image description from next span after break tag
                        description = span.next_sibling.next_sibling.string
                        photos_file.write(f"{description}")
                        print(f"Description:         {description}")
                    # endif span label
                # endif span header1 class
            photos_file.write(f"\n")  # End of photo information
            # end for spans loop
        # endif table <tr> row height is 300
    # end for table row

# end get_photo_data function


# Skip photo page 0, but extract all information from remaining 48 photo pages
for photo in range(1,49):
    get_photo_data(photo)
photos_file.close()
