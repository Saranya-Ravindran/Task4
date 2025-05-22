import requests
from bs4 import BeautifulSoup
import pandas as pd
base_url = "https://www.fanrank.org/ranking/india-sports-rankings-"

all_data = []
for page in range(1, 19): 
    url = f"{base_url}{page}"
    print(f"Scraping: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve page {page}")
        continue
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    if not table:
        print(f"No table found on page {page}")
        continue
    rows = table.tbody.find_all("tr") if table.tbody else table.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 4:
            sport = cols[0].get_text(strip=True)
            format_ = cols[1].get_text(strip=True)
            gender = cols[2].get_text(strip=True)
            rank = cols[3].get_text(strip=True)
            all_data.append({
                "Sport": sport,
                "Format": format_,
                "Gender": gender,
                "Rank": rank
            })
df = pd.DataFrame(all_data)
df.to_excel("india_sports_rankings.xlsx", index=False)
print(" Scraping complete! Data saved to Excel.")
# type: ignore