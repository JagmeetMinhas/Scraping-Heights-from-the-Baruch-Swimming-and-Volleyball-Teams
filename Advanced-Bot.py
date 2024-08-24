#Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

#Define a function to scrape heights from a given webpage
def scrapeHeights(url):
    #Make a request to the webpage
    webpage = requests.get(url)
    
    #Extract the raw HTML code and find all instances of a td tag with the height class
    sourceCode = BeautifulSoup(webpage.content, 'html.parser')
    heightTags = sourceCode.find_all("td", attrs = {"class": "height"})
    
    #Create a heightList to append all heights
    heightList = []
    
    #Iterate through the height tags, convert, and add them to the list
    #If the there is a blank in the list, append a NaN
    for heightTag in heightTags:
        newTag = heightTag.get_text().replace('-', "")
        if len(newTag) != 0:
            heightList.append((int(newTag[0])*12) + (int(newTag[1:])))
        else: 
            heightList.append(np.nan)
            
    #Return the list of heights     
    return(heightList)

def scrapeNames(url):
    #Make a request to the webpage
    webpage = requests.get(url)
    
    #Extract the raw HTML code and find all instances of a td tag with the player name class
    sourceCode = BeautifulSoup(webpage.content, 'html.parser')
    names = sourceCode.find_all("td", attrs = {"class": "sidearm-table-player-name"})
    
    #Create a nameList to append all the names
    nameList = []

    #Iterate through the name tags, stripping trailing/leading whitespace and add them to the list   
    for name in names:
        nameList.append(name.get_text().strip())
    
    #Return the list of names
    return(nameList)

def getTopandBottom5(dataframe, team):
    #Create a list of the top 5 heights by dropping duplicates and using nlargest and nsmallest to get the top and bottom 5
    #Find all the rows with heights in each list - repeat for all teams
    tallest = dataframe.drop_duplicates(subset = ["Height"])["Height"].nlargest(5).tolist()
    shortest = dataframe.drop_duplicates(subset = ["Height"])["Height"].nsmallest(5).tolist()
    print(f"The tallest people in {team} are...(height, name)")
    #This line will filter for heights in the top 5 using isin to create a filter mask, sort the values, and tranform it into a 2D array using .values.tolist()
    print(dataframe[dataframe['Height'].isin(tallest)].sort_values(by = ["Height"], ascending = False)[["Height", "Name"]].values.tolist())
    
    #Space
    print()
    
    print(f"The smallest people in {team} are...(height, name)")
    #This line will filter for heights in the top 5 using isin to create a filter mask, sort the values, and tranform it into a 2D array using .values.tolist()
    print(dataframe[dataframe['Height'].isin(shortest)].sort_values(by = ["Height"], ascending = True)[["Height", "Name"]].values.tolist())

def main():
    #Create master lists to store all names/heights
    menVolleyballNameList = []
    menVolleyballHeightList = []
    menSwimmingNameList = []
    menSwimmingHeightList = []
    womenVolleyballNameList = []
    womenVolleyballHeightList = []
    womenSwimmingNameList = []
    womenSwimmingHeightList = []
    
    #Create a list of all the team roster links
    menVolleyballTeams = ["https://ccnyathletics.com/sports/mens-volleyball/roster",
                       "https://lehmanathletics.com/sports/mens-volleyball/roster",
                       "https://www.brooklyncollegeathletics.com/sports/mens-volleyball/roster",
                       "https://johnjayathletics.com/sports/mens-volleyball/roster",
                       "https://athletics.baruch.cuny.edu/sports/mens-volleyball/roster",
                       "https://mecathletics.com/sports/mens-volleyball/roster",
                       "https://www.huntercollegeathletics.com/sports/mens-volleyball/roster",
                       "https://yorkathletics.com/sports/mens-volleyball/roster",
                       "https://ballstatesports.com/sports/mens-volleyball/roster"]
    
    womenVolleyballTeams = ["https://bmccathletics.com/sports/womens-volleyball/roster",
                            "https://yorkathletics.com/sports/womens-volleyball/roster",
                            "https://hostosathletics.com/sports/womens-volleyball/roster",
                            "https://bronxbroncos.com/sports/womens-volleyball/roster/2021",
                            "https://queensknights.com/sports/womens-volleyball/roster",
                            "https://augustajags.com/sports/wvball/roster",
                            "https://flaglerathletics.com/sports/womens-volleyball/roster",
                            "https://pacersports.com/sports/womens-volleyball/roster",
                            "https://www.golhu.com/sports/womens-volleyball/roster"]
    
    menSwimmingTeams = ["https://csidolphins.com/sports/mens-swimming-and-diving/roster",
                        "https://yorkathletics.com/sports/mens-swimming-and-diving/roster",
                        "https://athletics.baruch.cuny.edu/sports/mens-swimming-and-diving/roster",
                        "https://www.brooklyncollegeathletics.com/sports/mens-swimming-and-diving/roster",
                        "https://lindenwoodlions.com/sports/mens-swimming-and-diving/roster",
                        "https://mckbearcats.com/sports/mens-swimming-and-diving/roster",
                        "https://ramapoathletics.com/sports/mens-swimming-and-diving/roster",
                        "https://oneontaathletics.com/sports/mens-swimming-and-diving/roster",
                        "https://bubearcats.com/sports/mens-swimming-and-diving/roster/2021-22",
                        "https://albrightathletics.com/sports/mens-swimming-and-diving/roster/2021-22"]
    
    womenSwimmingTeams = ["https://csidolphins.com/sports/womens-swimming-and-diving/roster",
                          "https://queensknights.com/sports/womens-swimming-and-diving/roster",
                          "https://yorkathletics.com/sports/womens-swimming-and-diving/roster",
                          "https://athletics.baruch.cuny.edu/sports/womens-swimming-and-diving/roster/2021-22?path=wswim",
                          "https://www.brooklyncollegeathletics.com/sports/womens-swimming-and-diving/roster",
                          "https://lindenwoodlions.com/sports/womens-swimming-and-diving/roster",
                          "https://mckbearcats.com/sports/womens-swimming-and-diving/roster",
                          "https://ramapoathletics.com/sports/womens-swimming-and-diving/roster",
                          "https://keanathletics.com/sports/womens-swimming-and-diving/roster",
                          "https://oneontaathletics.com/sports/womens-swimming-and-diving/roster"]
    
    #Add the names and heights into the appropriate list
    for team in menVolleyballTeams:
        menVolleyballNameList += scrapeNames(team)
        menVolleyballHeightList += scrapeHeights(team)
        
    for team in womenVolleyballTeams:
        womenVolleyballNameList += scrapeNames(team)
        womenVolleyballHeightList += scrapeHeights(team)
        
    for team in menSwimmingTeams:
        menSwimmingNameList += scrapeNames(team)
        menSwimmingHeightList += scrapeHeights(team)
        
    for team in womenSwimmingTeams:
        womenSwimmingNameList += scrapeNames(team)
        womenSwimmingHeightList += scrapeHeights(team)
    
    #Create the series
    menVolleyballDictionary = {"Name": menVolleyballNameList, "Height": menVolleyballHeightList}
    womenVolleyballDictionary = {"Name": womenVolleyballNameList, "Height": womenVolleyballHeightList}
    menSwimmingDictionary = {"Name": menSwimmingNameList, "Height": menSwimmingHeightList}
    womenSwimmingDictionary = {"Name": womenSwimmingNameList, "Height": womenSwimmingHeightList}
    
    #Convert them to dataframes
    menVolleyballDF = pd.DataFrame(menVolleyballDictionary)
    womenVolleyballDF = pd.DataFrame(womenVolleyballDictionary)
    menSwimmingDF = pd.DataFrame(menSwimmingDictionary)
    womenSwimmingDF = pd.DataFrame(womenSwimmingDictionary)
    
    #Drop NaNs
    menVolleyballDF.dropna(inplace = True)
    womenVolleyballDF.dropna(inplace = True)
    menSwimmingDF.dropna(inplace = True)
    womenSwimmingDF.dropna(inplace = True)
    
    #Transfer the dataframes to csv files
    menVolleyballDF.to_csv("Mens_Volleyball_Heights.csv", index = False)
    womenVolleyballDF.to_csv("Womens_Volleyball_Heights.csv", index = False)
    menSwimmingDF.to_csv("Mens_Swimming_Heights.csv", index = False)
    womenSwimmingDF.to_csv("Womens_Swimming_Heights.csv", index = False)
    
    #Printing averages
    print(f"The average male volleyball player is {menVolleyballDF['Height'].mean():.2f} inches tall.")
    print(f"The average female volleyball player is {womenVolleyballDF['Height'].mean():.2f} inches tall.")
    print(f"The average male swimmer is {menSwimmingDF['Height'].mean():.2f} inches tall.")
    print(f"The average female swimmer is {womenSwimmingDF['Height'].mean():.2f} inches tall.")
    
    #Space
    print()
    
    #Get the tallest people from each sport
    getTopandBottom5(menVolleyballDF, "men's volleyball")
    
    #Space
    print()
    
    getTopandBottom5(womenVolleyballDF, "women's volleyball")
    
    #Space
    print()
    
    getTopandBottom5(menSwimmingDF, "men's swimming")
    
    #Space
    print()
    
    getTopandBottom5(womenSwimmingDF, "women's swimming")
    
    #Output a graph, DO THIS IN COLAB
    #totalDF = pd.concat([menVolleyballDF, menSwimmingDF, womenSwimmingDF, womenVolleyballDF], ignore_index = True)
    #graph = totalDF.plot.bar(y = "Height")
    
#Execute the main program        
main()
