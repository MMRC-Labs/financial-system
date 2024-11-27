import requests
from bs4 import BeautifulSoup

url = "https://bondcalculator.jse.co.za/BondSingle.aspx?calc=Spot"

response = requests.get(url)

print(response.status_code)

# if response.status_code == 200: 
# # Parse the HTML content 
#     soup = BeautifulSoup(response.content, 'html.parser') 
#     # Find and print specific elements 
#     title = soup.find('title').get_text() 
#     print("Title of the page:", title) 
#     # Example of finding all paragraph tags 
#     paragraphs = soup.find_all('p') 
#     for p in paragraphs: 
#         print(p.get_text()) 
# else: print("Failed to retrieve the webpage. Status code:", response.status_code)