#Import libraries
import requests
from bs4 import BeautifulSoup

#Predefine scraping functions
def scrapeWebpage(url, teamName):
    #Make GET request, parse HTML, and find table data
    webpage = requests.get(url)
    
    sourceCode = BeautifulSoup(webpage.content, 'html.parser')
    tableRows = sourceCode.find_all("tr")
    
    heights = []
    
    for row in tableRows:
        height = row.find_all("td", attrs = {"class":"height"})
        if len(height) != 0:
            #Convert the height from a feet and inches format to an inches format
            heights.append((int(height[0].get_text()[0]) * 12) + int(height[0].get_text()[2:]))

    averageHeight = sum(heights)/len(heights)

    return (f"The average height of the {teamName} team is {averageHeight:.2f} inches.")
  
def main():
    pageDict = {"Men's Swimming":"https://athletics.baruch.cuny.edu/sports/mens-swimming-and-diving/roster",
                "Men's Volleyball" : "https://athletics.baruch.cuny.edu/sports/mens-volleyball/roster", 
                "Women's Swimming": "https://athletics.baruch.cuny.edu/sports/womens-swimming-and-diving/roster",
                "Women's Volleyball": "https://athletics.baruch.cuny.edu/sports/mens-volleyball/roster"}
    
    for label, page in pageDict.items():
        print(scrapeWebpage(page, label))    
main()
