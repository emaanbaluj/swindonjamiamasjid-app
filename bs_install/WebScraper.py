from bs4 import BeautifulSoup
import requests

# Step 1: Open the book (website)
url = 'https://www.swindonmasjid.com'
page = requests.get(url)

# Step 2: Find the small window (iframe) in the book
soup = BeautifulSoup(page.text, 'html.parser')
iframe = soup.find("iframe", {"src": lambda x: x and 'st.php' in x})

if iframe:
    # Step 3: Open the special page
    iframe_url = iframe['src']
    iframe_page = requests.get(iframe_url)

    # Step 4: Look inside the special page for the table
    iframe_soup = BeautifulSoup(iframe_page.text, 'html.parser')
    table = iframe_soup.find("table", {"id": "mytable"})

    if table:
        # Step 5: Read the table to get the prayer times
        rows = table.find_all("tr")
        for row in rows:
            columns = row.find_all(["th", "td"])
            for column in columns:
                print(column.get_text(strip=True), end=" ")
            print()
    else:
        print("Table not found in iframe.")
else:
    print("Iframe not found.")
