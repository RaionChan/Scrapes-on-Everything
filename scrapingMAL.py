import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os

try:
    print("Welcome to MyAnimeList Scraper!\nIt's hilarious because I need it to checked all of 'em effortlessly\nBtw, it is calculated by the precentage of how much recommended vs not recommended and mixed feeling by reviewers\nWell, here it is!\n\n")
    print("Now, let me ask, wanna searh them manually or using ur plan to watch list? (manual/plan)")
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
        print("Alright, gimme the username: ")
        username = input()
        base_url = f"https://myanimelist.net/animelist/{username}?status=6"

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
        print(f"Here is the list of anime in {username}'s plan to watch: ")
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
            recommended = soup.find_all('div', class_='recommended')
            rec = int(recommended[0].find('strong').text)

            notrecommended = soup.find_all('div', class_='not-recommended')
            notrec = int(notrecommended[0].find('strong').text)

            mixedfeelings = soup.find_all('div', class_='mixed-feelings')
            mix = int(mixedfeelings[0].find('strong').text)
            listOfAnime.append([width, title, rec, notrec, mix])

    df = pd.DataFrame(listOfAnime, columns=['Satisfaction', 'Title', 'Recommended', 'Not Recommended', 'Mixed Feelings'])
    df = df.sort_values(by='Satisfaction', ascending=False)
    print("================================")
    print("Here is the list of anime you have searched: ")
    print(df)

    print("Let's check whether u already have the file or not")
    if os.path.exists('anime_satisfaction.csv'):
        print("You already have the file anime_satisfaction.csv")
        file_there = True
    else:
        print("You don't have the file anime_satisfaction.csv")
        file_there = False

    print("================================")
    if file_there:
        print("Do you want to overwrite the file or append them from your old file? (overwrite/append) ")
        answer = input()

        if answer.lower() == 'overwrite':
            df.to_csv('anime_satisfaction.csv', index=False)
            print("The result has been saved to anime_satisfaction.csv")
        elif answer.lower() == 'append':
            old_df = pd.read_csv('anime_satisfaction.csv')
            new_df = pd.concat([old_df, df], ignore_index=True)
            new_df.to_csv('anime_satisfaction.csv', index=False)
            print("The result has been appended to anime_satisfaction.csv")
            
    else:
        print("Do you want to save the result to a CSV file so u won't lose it? (y/n)")
        answer = input()

        if answer.lower() == 'y':
            df.to_csv('anime_satisfaction.csv', index=False)
            print("The result has been saved to anime_satisfaction.csv")
        else:
            print("Alright, the result is not saved")

    print("Thank you for using MyAnimeList Recommendation Anime by Raion! Have a great day!")

except Exception as e:
    print("An error occurred: ", e)
    print("Try again as I instructed :( U r making me sad")