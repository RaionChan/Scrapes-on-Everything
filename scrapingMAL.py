import requests
from bs4 import BeautifulSoup
import pandas as pd

print("Welcome to MyAnimeList Scraper!\nIt's hilarious because I need it to checked all of 'em effortlessly\nWell, here it is!")
print("But beefore we start, let me ask, u wanna searh them manually or using ur plan to watch list? (manual/plan)")
answer = input()

if answer.lower() == 'manual':
    print("Alright, let's start searching manually!")
    print("================================")

    listOfAnime=[]

    while True:
        search_term = input("Enter the search term: ")
        base_url = f"https://myanimelist.net/search/all?q={search_term}&cat=all"

        response = requests.get(base_url)

        soup = BeautifulSoup(response.content, 'html.parser')

        titles = []
        link = []

        results = soup.find_all('div', class_='title')
        for result in results:
            title = result.find('a').text
            titles.append(title)

            picked = result.find('a')['href']
            link.append(picked)

        df = pd.DataFrame({'Title': titles})
        print(df)

        print("\n================================\nPick what you want: ")
        pickedItem=int(input())
        selectedLink=link[pickedItem]
        selectedTitle=titles[pickedItem]

        print("You selected: ", link[pickedItem])

        print("================================")
        response = requests.get(selectedLink)

        soup = BeautifulSoup(response.content, 'html.parser')

        print("Hmmm, let's see if it's worth watching based on recommendations: ")
        recommended = soup.find_all('div', class_='recommended')
        rec = int(recommended[0].find('strong').text)
        print("People who are recommended it: ", rec)

        notrecommended = soup.find_all('div', class_='not-recommended')
        notrec = int(notrecommended[0].find('strong').text)
        print("People who are not recommended it: ", notrec)

        mixedfeelings = soup.find_all('div', class_='mixed-feelings')
        mix = int(mixedfeelings[0].find('strong').text)
        print("People who have mixed feeling: ", mix)



        width = float(soup.find('div', class_='recommended__bar')['style'].split(':')[1].split('%')[0])
        width = round(width, 2)
        print("\n","\nSooo, do you want to watch it cause the satisfactions is: \n", width, "%")

        listOfAnime.append([width, selectedTitle])
        
        print("================================")
        print("Do you want to search again? (y/n)")
        answer = input()
        if answer.lower() != 'y':
            break
        else:
            continue

    print("================================")
    print("Here is the list of anime you have searched: ")
    df = pd.DataFrame(listOfAnime, columns=['Satisfaction', 'Title'])
    print(df)
    print("Thank you for using MyAnimeList Scraper! Have a nice day!")

elif answer.lower() == 'plan':
    print("Alright, gimme ur username: ")
    username = input()
    base_url = f"https://myanimelist.net/animelist/{username}?status=6"
    print("================================")

    response = requests.get(base_url)

    soup = BeautifulSoup(response.content, 'html.parser')

    titles = []
    link = []

    results = soup.find_all('a', class_='list-tables')
    for result in results:
        title = result.text
        titles.append(title)

        picked = result['href']
        link.append(picked)

    df = pd.DataFrame({'Title': titles})
    print(df)





