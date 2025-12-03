from bs4 import BeautifulSoup
import requests


def get_event_data(event_number: int):
    """
    Gets information for event

    :param event_number: Number of event
    :return: Nothing; Prints extracted information.
    """

    web_page = f"https://www.dangribbin.com/event/{event_number}"
    print(f"Web page: {web_page}")

    response = requests.get(web_page)              # Connect to Dan Gribbin event information page
    contents = response.text                       # Get web page contents
    html = BeautifulSoup(contents, "html.parser")  # Parse web page HTML

    outer_table = html.find('table', width="647")
    table_rows = outer_table.find_all('tr')
    for table_row in table_rows:
        tr_height = table_row.get('height')
        # print(f"tr_height: {tr_height}")
        # Get event section, categories and information
        if tr_height == "300":
            td = table_row.next_element.next_element
            td = td.next_sibling.next_element.next_element
            inner_table = td.next_element.next_element
            trs = inner_table.find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                for td in tds:
                    td_attrs = td.attrs
                    # Get Section name
                    if "colspan" in td_attrs:
                        section_name = td.text
                        # General Overview, Venue Info, Misc. Info
                        # print(f"{section_name}")  # Not written to CSV file
                    else:  # Not a td with colspan
                        td_width = td.get('width')
                        if td_width == "195":  # Left column with category
                            category = td.text  # Not written to CSV file
                            # Venue:,Date:,Time:,
                            # Address:,City:,State:,Zip Code:,Country:,Website:,Telephone:,
                            # Cover Charge:,Age Requirement:
                        elif td_width == "200":  # Right column with information
                            if category == "Website:":
                                # Extract website link if present
                                website_link = td.findAll('a')
                                if website_link:              # Has anchor tag
                                    info = td.a['href']       # Get website link
                                else:
                                    info = "NONE"             # Website link absent
                                # endif
                            else:  # Not a website link
                                info = td.span.text
                                # Write info for category with "|" unless last category.
                                # if category == "Age Requirement:":
                                #     event_file.write(f"\n")  # Last event info
                                # else:
                                #     event_file.write(f"|")  # Append '|' instead of ','
                                # # endif check for last event line
                            # endif category check for website
                            # print(f"  {category:<16} {info}")
                            event_file.write(f"{info}|")
                        # endif td_width
                    # endif td_attr check for section in td with colspan
                # event_file.write(f"\n")  # End of event information
                # end for td
            # end for tr
    # end for table_row

    # Get Footer Press:, Directions, and Other information
    # Footer information written to separate event_footer_#.txt
    footer_file = f"event_footer_{event_number}.txt"
    event_footer = open(footer_file, mode="w", encoding="utf8")
    footer_row = html.find('tr', height='105')
    footer_cols = footer_row.find_all('td')
    for footer_column in footer_cols:
        column_width = footer_column.get('width')
        if column_width == "400":  # Center column
            footer_rows = footer_column.find_all('tr')
            for row in footer_rows:
                footer_category = row.td.text
                delimiter = footer_category.find(":")
                footer_category = footer_category[:delimiter]
                event_footer.write(f"{footer_category}:\n")
                # print(f"{footer_category}:")
                footer_information = row.td.span.text
                # print(f"{footer_information}")
                event_footer.write(f"{footer_information}\n")
            # end for row
        # endif column width
    # end for footer_column
    event_footer.close()

    # end event_file

# Loop over selected event pages
# Open event_info.csv file for writing
event_file = open("event_info.csv", mode="w")
for event in range(84):
    event_file.write(f"{event}|")  # Event number
    get_event_data(event)
    event_file.write(f"\n")         # End of specific event data
event_file.close()
