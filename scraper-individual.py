import sys
import urllib.request
import pandas as pd
from bs4 import BeautifulSoup

def save_to_csv(data):
    df_players_stats = pd.DataFrame(data)
    df_players_stats.columns = [
        'name',
        'crossing',
        'finishing',
        'heading_accuracy',
        'short_passing',
        'volleys',
        'dribbling',
        'curve',
        'fk_accuracy',
        'long_passing',
        'ball_control',
        'acceleration',
        'sprint_speed',
        'agility',
        'reactions',
        'balance',
        'shot_power',
        'jumping',
        'stamina',
        'strength',
        'long_shots',
        'aggression',
        'interceptions',
        'positioning',
        'vision',
        'penalties',
        'composure',
        'defensive_awareness',
        'standing_tackle',
        'slide_tackle',
        'gk_diving',
        'gk_handling',
        'gk_kicking',
        'gk_positioning',
        'gk_reflexes',
        'best_position',
        'club_position',
        'best_overall_rating'
    ]

    df_players_stats.to_csv('players.csv', sep=';')

if __name__ == '__main__':
    sofifa = 'https://sofifa.com/'
    offset_url = '?offset='
    offset = 0

    # This scraper goes to the player details page for each page.
    numOfPlayersToScrap = 60 
    
    players = []

    clean_positions = False

    for arg in sys.argv:
        if arg == '-c':
            clean_positions = True
    
    index = 0
    while len(players) < numOfPlayersToScrap:
        sofifa_request = urllib.request.Request(sofifa + offset_url + str(offset), headers={'User-Agent': 'Mozilla/5.0'})
        page = urllib.request.urlopen(sofifa_request)
        soup = BeautifulSoup(page, features='lxml')
    
        players_table = soup.find('tbody', class_='list')
        for player in players_table.findAll('tr'):
            cells = player.findAll('td')
            player_website_url = cells[1].find('a', role='tooltip')['href']
            player_website_request = urllib.request.Request(sofifa + player_website_url, headers={'User-Agent': 'Mozilla/5.0'})
    
            page_player = urllib.request.urlopen(player_website_request)
            soup_player = BeautifulSoup(page_player, features='lxml')
    
            info = soup_player.find('div', class_='info')
            name = info.find('h1').text
            name = name.split('(')[0].strip()
    
            player = [name]
    
            body = soup_player.find('body')
            centers = body.findAll('div', class_='center')
    
            player_info = centers[4].find('div', class_='col col-12')
            player_info_columns = player_info.findAll('div', class_='block-quarter', recursive=False)
            club_position = player_info_columns[2].find('span', class_='pos').text
    
            player_stats = centers[5].find('div', class_='col col-12')
            player_stats_columns = player_stats.findAll('div', class_='block-quarter', recursive=False)
            del player_stats_columns[-1]
            for column in player_stats_columns:
                stats = column.findAll('ul', class_='pl')
                for stats_group in stats:
                    lis = stats_group.findAll('li')
                    for li in lis:
                        value = li.find('span').text
                        player.append(value)
    
            player_stats_graph = centers[5].find('div', class_='col col-4')
            ul = player_stats_graph.find('ul', class_='pl', recursive=False)
            lis = ul.findAll('li', recursive=False)
            best_position = lis[0].find('span').text
    
            ## EA FIFA positions:
            ## Attack:
            ##   ST - striker
            ##   CF - centre forward
            ##   LW/RW - reft/right winger
            ## Midfield:
            ##   LM/RM - left/right midfielder
            ##   CAM - central attacking midfielder
            ##   CM - centre midfielder
            ##   CDM - centre defensive midfielder
            ## Defense:
            ##   LWB/RWB - left/right wing back
            ##   LB/RB - left/right back
            ##   CB - centre back
            ## Goalkeeper:
            ##   GK - goalkeeper
            ## Other:
            ##   SUB - substitute
            ##   RES - reserve
    
            if clean_positions:
            # Clean club position:
                match club_position:
                    case 'LS' | 'ST' | 'RS':
                        club_position = 'Striker'
                    case 'LF' | 'CF' | 'RF':
                        club_position = 'Forward'
                    case 'LW' | 'RW':
                        club_position = 'Attacking winger'
                    case 'LM' | 'RM':
                        club_position = 'Midfield winger'
                    case 'LAM' | 'CAM' | 'RAM':
                        club_position = 'Attacking midfielder'
                    case 'LM' | 'CM' | 'RM':
                        club_position = 'Midfielder'
                    case 'LDM' | 'CDM' | 'RDM':
                        club_position = 'Defensive midfielder'
                    case 'LWB' | 'RWB':
                        club_position = 'Wingback'
                    case 'LB' | 'RB':
                        club_position = 'Fullback'
                    case 'LCB' | 'CB' | 'RCB':
                        club_position = 'Centre-back'
                    case 'GK':
                        club_position = 'Goalkeeper'
                    case 'SUB':
                        club_position = 'Substitute'
                    case 'RES':
                        club_position = 'Reserve'
    
                ## Clean best position:
                match best_position:
                    case 'LS' | 'ST' | 'RS':
                        best_position = 'Striker'
                    case 'LF' | 'CF' | 'RF':
                        best_position = 'Forward'
                    case 'LW' | 'RW':
                        best_position = 'Attacking winger'
                    case 'LM' | 'RM':
                        best_position = 'Midfield winger'
                    case 'LAM' | 'CAM' | 'RAM':
                        best_position = 'Attacking midfielder'
                    case 'LM' | 'CM' | 'RM':
                        best_position = 'Midfielder'
                    case 'LDM' | 'CDM' | 'RDM':
                        best_position = 'Defensive midfielder'
                    case 'LWB' | 'RWB':
                        best_position = 'Wingback'
                    case 'LB' | 'RB':
                        best_position = 'Fullback'
                    case 'LCB' | 'CB' | 'RCB':
                        best_position = 'Centre-back'
                    case 'GK':
                        best_position = 'Goalkeeper'

            player.append(club_position)
            player.append(best_position)
    
            best_overall_rating = lis[1].find('span').text
            player.append(best_overall_rating)
            
            print(index, player)
            players.append(player)
            index = index + 1
        offset = offset + 60
        save_to_csv(players)
