from bs4 import BeautifulSoup
import requests
import re

# Dan's events web page was laid out uwing tables
# This python program searches for the event Location,
# the Venue, the Data, and the link for more information,
# and writes the event data to the events.csv data file

response = requests.get("https://www.dangribbin.com/events/1")  # Connect to Dan's Events page
dg_events_web_page = response.text                              # Get web page contents
html = BeautifulSoup(dg_events_web_page, "html.parser")         # Parse HTML

pattern = re.compile(r"[\d]+$")                                 # Event number from event/##

with open("events.csv", mode="w") as events_file:
    outer_table = html.find("table", width="647")  # Find outer table
    table_rows = outer_table.find_all('tr', height="300")  # Find tably rows with height = 300
    for table_row in table_rows:
        row_height = table_row.get("height")
        if row_height == "300":
            # Find second TD with width="400"
            second_td = table_row.td.next_sibling.next_element.next_element
            inner_table = second_td.table
            inner_table_contents = inner_table.contents
            for item in inner_table_contents:
                if item.name == "tr":
                    height = item.get("height")
                    if height == "12":
                        pass
                        #Extract column headings from nested td
                        # header_columns = item.find_all("td")
                        # for header_column in header_columns:
                        #     column_heading = header_column.span.text
                        #     if column_heading != "View":
                        #         events_file.write(f"{column_heading}|")
                        #     else:
                        #         events_file.write(f"{column_heading}\n")
                        #     endif
                        # end for
                    else:
                        # Extract event data
                        data_columns = item.find_all("td")
                        if len(data_columns) == 4:
                            location  = data_columns[0].span.span.text
                            venue     = data_columns[1].text
                            date      = data_columns[2].text
                            view_info = data_columns[3].a["href"]
                            event     = re.search(pattern, view_info).group()  # Event number
                            events_file.write(f"{event}|{location}|{venue}|{date}|{event}\n")
                            print(f"{event} ", end='')
                        # endif data_columns
                    # endif height
                # endif item.name
            # end for item
        # end if row_height
    # end for table_row
    print("")
