import requests
from bs4 import BeautifulSoup
import sqlite3

urls = []
with open("urls.txt") as f:
    urls = [e.strip() for e in f.readlines()]

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
}

conn = sqlite3.connect("database.db")
c = conn.cursor()

for i, url in enumerate(urls):
    response = requests.get(url + "0", headers=headers)
    html = response.text

    soup = BeautifulSoup(html, "lxml")
    heading = soup.find("h1", class_="page__heading").text

    c.execute("INSERT INTO category(id, name) VALUES(?, ?)", [i, heading])
    conn.commit()

    for j in range(0, 2000):
        response = requests.get(url + str(j), headers=headers)
        html = response.text

        if "The source of signal is not available" in html:
            break

        soup = BeautifulSoup(html, "lxml")
        results = soup.find_all("button", class_="b-play station_play")

        for element in results:
            img_url = element["radioimg"]
            name = element["radioname"]
            stream_url = element["stream"]

            c.execute("INSERT INTO station(category_id, name, stream_url, img_url) VALUES(?, ?, ?, ?)",
                        [i, name, stream_url, img_url])
        conn.commit()

conn.close()
