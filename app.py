import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__)



@app.route('/', methods=['GET'])
def scrape_prayer_times():
    url = 'https://www.swindonmasjid.com'
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')
    iframe = soup.find("iframe", {"src": lambda x: x and 'st.php' in x})

    prayer_times = []
    if iframe:
        iframe_url = iframe['src']
        if not iframe_url.startswith('http'):
            iframe_url = url + iframe_url  # Ensure the URL is absolute

        iframe_page = requests.get(iframe_url)

        iframe_soup = BeautifulSoup(iframe_page.text, 'html.parser')
        table = iframe_soup.find("table", {"id": "mytable"})

        if table:
            rows = table.find_all("tr")[1:]  # Skip the header row
            for row in rows:
                columns = row.find_all(["th", "td"])
                if len(columns) >= 3:  # Ensure there are enough columns
                    prayer = columns[0].get_text(strip=True)
                    start = columns[1].get_text(strip=True)
                    jamaah = columns[2].get_text(strip=True) if len(columns) > 1 else None
                    prayer_times.append({ 'Start': start, 'Prayer': prayer, 'Jamaah': jamaah})

    return prayer_times

if __name__ == '__main__':
    app.run(debug=True)
