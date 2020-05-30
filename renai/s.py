from bs4 import BeautifulSoup
import requests

url = "https://osustats.click/BananaFace765"
content = requests.get(url)

soup = BeautifulSoup(content.text, "html.parser")



print(soup.select("PlayerCard__value"))

