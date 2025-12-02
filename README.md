# Dan Gribbin Web Site
## Redesign of existing web site

### Background

### Scraping the Data

### Creating Web Pages

### Generating Web Pages

### Results

### Comparison Statistics

### Data Files

## Conclusion

The hardest part of this project was "scraping" the data from the original HTML 
files. Tables were nested inside tables; only by identifying the specific height or 
width attributes in the table **<tr>** rows, **<th>** headings, and **<td>** data columns 
was it finally possible to identify the and extract relevant data. 

Links to audio files for listening and purchasing were sometimes broken, making 
automation extraction difficult. Each album and song links needed to be 
validated. Song lyrics were extracted into individual text files, and identified by 
song number. Events were likewise extracted into individual text files and 
identified by event number.

## Future Work

Missing from the web site is the ability of the owner to add songs, events, links, 
and pictures. New add_song.html, add_event.html, add_link.html, and 
add_image.html web pages with input forms would need to be written, with 
additional Python functions designed to extract the information and append them 
to existing data files.

Finally, the entire web site with web pages, styles, data files, and Python code 
would need to be transported to a web server that supports dynamic data.
