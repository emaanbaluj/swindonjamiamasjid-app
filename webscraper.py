from bs4 import BeautifulSoup
import requests

def scrape_prayer_times():
    url = 'https://www.swindonmasjid.com'
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')
    iframe = soup.find("iframe", {"src": lambda x: x and 'st.php' in x})

    prayer_times = []
    if iframe:
        iframe_url = iframe['src']
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
                    prayer_times.append({'Prayer': prayer, 'Start': start, 'Jamaah': jamaah})

    return prayer_times

# Example usage
prayer_times = scrape_prayer_times()
for pt in prayer_times:
    print(pt)
