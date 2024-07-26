import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os

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


elif answer.lower() == 'plan':
    print("Alright, gimme ur username: ")
    username = input()
    base_url = f"https://myanimelist.net/animelist/{username}?status=6"
    print("================================")

    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', class_='list-table')
    data_items_json = table.get('data-items')

    data_items_json = data_items_json.replace('&quot;', '"')
    data_items = json.loads(data_items_json)

    base_anime_url = 'https://myanimelist.net/'
    titles_and_links = []

    for item in data_items:
        title = item['anime_title']
        relative_url = item['anime_url']
        full_url = f"{base_anime_url}{relative_url.strip('/')}"
        titles_and_links.append((title, full_url))

    print('\n================================')
    print(f"Here is the list of anime you have in {username}'s watch list: ")
    for i, (title, link) in enumerate(titles_and_links, start=1):
        print(f"{i}. {title}")

    print('\n================================')
    print("Let's see how good these anime are")
    print("================================\n")

    print("Calculating the recommendations...")


    
    listOfAnime=[]
    #[0][0] tu black lagoon, [0][1] tu linknya
    for title, link in titles_and_links:
        print ('Searching for: ', title)
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')

        width = float(soup.find('div', class_='recommended__bar')['style'].split(':')[1].split('%')[0])
        width = round(width, 2)
        listOfAnime.append([width, title])

print("================================")
print("Here is the list of anime you have searched: ")
df = pd.DataFrame(listOfAnime, columns=['Satisfaction', 'Title'])
df = df.sort_values(by='Satisfaction', ascending=False)
print(df)

print("================================")
print("Do you want to save the result to a CSV file so u won't lose it? (y/n)")
answer = input()

if answer.lower() == 'y':
    df.to_csv('anime_satisfaction.csv', mode='a', header=not os.path.exists('anime_satisfaction.csv'), index=False)
    print("The result has been appended to anime_satisfaction.csv")
else:
    print("Alright, the result is not saved")

print("Thank you for using MyAnimeList Scraper by Raion! Have a nice day!")