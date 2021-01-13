import requests
from bs4 import BeautifulSoup
from _datetime import date
import progressbar
import time
import os
import pandas as pd

class WNBAWrapper:

    def __init__(self):
        self.url = 'https://www.basketball-reference.com'
        self.full_url = ''
        self.folder_location = os.getcwd() + '/Data/'

    def getBoxScore(self):

        #columns that will be used in your csv file
        columns = ['gmDate', 'seasonType', 'season', 'teamWins', 'teamLosses', 'teamAbbr', 'teamLoc', 'teamRslt',
                   'teamDayOff', 'teamPTS', 'teamAST', 'teamTO', 'teamMin',
                   'teamSTL', 'teamBLK', 'teamPF', 'teamFGA', 'teamFGM', 'teamFG%',
                   'team2PA', 'team2PM', 'team2P%', 'team3PA', 'team3PM', 'team3P%',
                   'teamFTA', 'teamFTM', 'teamFT%', 'teamORB', 'teamDRB', 'teamTRB',
                   'teamTREB%', 'teamASST%',
                   'teamTS%', 'teamEFG%', 'teamOREB%', 'teamDREB%', 'teamTO%',
                   'teamSTL%', 'teamBLK%', 'teamBLKR', 'teamPPS', 'teamFIC',
                   'teamFIC40', 'teamOrtg', 'teamDrtg', 'teamEDiff', 'teamPlay%',
                   'teamAR', 'teamPoss', 'teamAST/TO', 'teamPace', 'teamSTL/TO', 'opptWins',
                   'opptLosses', 'opptAbbr', 'opptLoc', 'opptRslt',
                   'opptDayOff', 'opptPTS', 'opptAST', 'opptTO', 'opptMin', 'opptSTL', 'opptBLK',
                   'opptPF', 'opptFGA', 'opptFGM', 'opptFG%', 'oppt2PA', 'oppt2PM',
                   'oppt2P%', 'oppt3PA', 'oppt3PM', 'oppt3P%', 'opptFTA', 'opptFTM',
                   'opptFT%', 'opptORB', 'opptDRB', 'opptTRB', 'opptTREB%', 'opptASST%',
                   'opptTS%', 'opptEFG%',
                   'opptOREB%', 'opptDREB%', 'opptTO%', 'opptSTL%', 'opptBLK%',
                   'opptBLKR', 'opptPPS', 'opptFIC', 'opptFIC40', 'opptOrtg',
                   'opptDrtg', 'opptEDiff', 'opptPlay%', 'opptAR', 'opptAST/TO',
                   'opptSTL/TO', 'opptPoss', 'opptPace', 'matchWinner']

        first_year = 2020
        last_year = 2020

        os.chdir(self.folder_location)

        #loop over the years
        while first_year <= last_year:

            #last game date of a team
            last_game = {'ATL': '', 'CHI': '', 'CON': '', 'CHA': '', 'CLE': '', 'DAL': '', 'DET': '', 'HOU': '',
                         'IND': '', 'LAS': '', 'LVA': '', 'MIA': '', 'MIN': '', 'NYL': '', 'ORL': '', 'PHO': '',
                         'POR': '', 'SAC': '', 'SAS': '', 'SEA': '', 'TUL': '', 'UTA': '', 'WAS': ''}

            #total wins of a team
            wins = {'ATL': 0, 'CHI': 0, 'CON': 0, 'CHA': 0, 'CLE': 0, 'DAL': 0, 'DET': 0, 'HOU': 0,
                    'IND': 0, 'LAS': 0, 'LVA': 0, 'MIA': 0, 'MIN': 0, 'NYL': 0, 'ORL': 0, 'PHO': 0,
                    'POR': 0, 'SAC': 0, 'SAS': 0, 'SEA': 0, 'TUL': 0, 'UTA': 0, 'WAS': 0}

            #total losses of a team
            losses = {'ATL': 0, 'CHI': 0, 'CON': 0, 'CHA': 0, 'CLE': 0, 'DAL': 0, 'DET': 0, 'HOU': 0,
                      'IND': 0, 'LAS': 0, 'LVA': 0, 'MIA': 0, 'MIN': 0, 'NYL': 0, 'ORL': 0, 'PHO': 0,
                      'POR': 0, 'SAC': 0, 'SAS': 0, 'SEA': 0, 'TUL': 0, 'UTA': 0, 'WAS': 0}

            bar = progressbar.ProgressBar(max_value = progressbar.UnknownLength)
            
            data = pd.DataFrame(columns = columns)

            seasonType = 'Regular'

            print("\nCollecting the data from the " +str(first_year)+ " season. Please wait!")

            self.full_url = self.url + '/wnba/years/' + str(first_year) + '-schedule.html'
            request = requests.get(self.full_url)
            
            if request.status_code == 200:
                soup = BeautifulSoup(request.text, 'html.parser')

                #get the boxscore table
                boxscore_table = soup.find('table', {'id': 'schedule'})
                table_body = boxscore_table.find('tbody')
                table_trs = table_body.findAll('tr')
                index = 0

                #loop over the rows
                #each row is a game in a season
                for tr in table_trs:
                                       
                    #get teams abbreviations
                    teams_abbr = tr.findAll('td', {'class': 'left'})

                    if teams_abbr:

                        #away team
                        team_away_abbr_anchor = teams_abbr[0].find('a')
                        team_away_abbr_anchor = team_away_abbr_anchor['href']
                        team_away_abbr_formated = str(team_away_abbr_anchor).split('/', 4)[3]
                        data.loc[index, 'teamAbbr'] = team_away_abbr_formated
                        data.loc[index, 'teamLoc'] = 'Away'

                        #home team
                        team_home_abbr_anchor = teams_abbr[1].find('a')
                        team_home_abbr_anchor = team_home_abbr_anchor['href']
                        team_home_abbr_formated = str(team_home_abbr_anchor).split('/', 4)[3]
                        data.loc[index, 'opptAbbr'] = team_home_abbr_formated
                        data.loc[index, 'opptLoc'] = 'Home'

                        data.loc[index, 'season'] = str(first_year)
                        data.loc[index, 'seasonType'] = seasonType

                        #get teams total points
                        teams_total_points = tr.findAll('td', {'class': 'right'})
                        total_points_away = teams_total_points[0].get_text()
                        total_points_home = teams_total_points[1].get_text()

                        data.loc[index, 'opptWins'] = wins[team_home_abbr_formated]
                        data.loc[index, 'opptLosses'] = losses[team_home_abbr_formated]
                        data.loc[index, 'teamWins'] = wins[team_away_abbr_formated]
                        data.loc[index, 'teamLosses'] = losses[team_away_abbr_formated]

                        if total_points_home > total_points_away:
                            wins[team_home_abbr_formated] += 1
                            losses[team_away_abbr_formated] += 1
                            data.loc[index, 'teamRslt'] = 'Loss'
                            data.loc[index, 'opptRslt'] = 'Win'
                            data.loc[index, 'matchWinner'] = team_home_abbr_formated
                        else:
                            losses[team_home_abbr_formated] += 1
                            wins[team_away_abbr_formated] += 1
                            data.loc[index, 'teamRslt'] = 'Win'
                            data.loc[index, 'opptRslt'] = 'Loss'
                            data.loc[index, 'matchWinner'] = team_away_abbr_formated

                        #get game date
                        game_date = tr.find('th', {'class': 'left'})
                        game_date = game_date['csk']
                        game_date = game_date[:-4]
                        game_year = game_date[:4]
                        game_month = game_date[4:6]
                        game_day = game_date[6:]

                        #format game date to a date type
                        game_date_formated = date(int(game_year), int(game_month), int(game_day))
                        data.loc[index, 'gmDate'] = game_date_formated

                        #first game of the season (home team)
                        if last_game[team_home_abbr_formated] == '':
                            last_game[team_home_abbr_formated] = game_date_formated
                            data.loc[index, 'opptDayOff'] = 0
                        else:
                            last_date = last_game[team_home_abbr_formated]
                            days_off = game_date_formated - last_date
                            data.loc[index, 'opptDayOff'] = int(days_off.days) - 1

                            #replace the last game date for the current date
                            last_game[team_home_abbr_formated] = game_date_formated

                        #first game of the season (away team)
                        if last_game[team_away_abbr_formated] == '':
                            last_game[team_away_abbr_formated] = game_date_formated
                            data.loc[index, 'teamDayOff'] = 0
                        else:
                            last_date = last_game[team_away_abbr_formated]
                            days_off = game_date_formated - last_date
                            data.loc[index, 'teamDayOff'] = int(days_off.days) - 1

                            #replace the last game date for the current date
                            last_game[team_away_abbr_formated] = game_date_formated

                        #boxscore link
                        tablescore_cell = tr.find('td', {'class': 'center'})

                        if tablescore_cell:
                            #get the boxscore link of a game
                            cell_anchor = tablescore_cell.find('a');
                            cell_anchor = cell_anchor['href']

                            boxscore_game = requests.get(self.url + cell_anchor)
                            
                            if boxscore_game.status_code == 200:
                                
                                #first table = away team
                                #second table = home team
                                soup_boxscore = BeautifulSoup(boxscore_game.text, 'html.parser')
                                tables_score = soup_boxscore.findAll('table', {'class': 'suppress_all'})

                                if tables_score:

                                    #away team stats
                                    table_footer = tables_score[0].find('tfoot')
                                    table_footer_tr = table_footer.find('tr')
                                    table_footer_td = table_footer_tr.findAll('td')

                                    data.loc[index, 'teamMin'] = self.checkNumber(table_footer_td[0].get_text())
                                    data.loc[index, 'teamFGM'] = self.checkNumber(table_footer_td[1].get_text())
                                    data.loc[index, 'teamFGA']  = self.checkNumber(table_footer_td[2].get_text())
                                    data.loc[index, 'teamFG%']  = "%0.2f" % (self.checkNumber(table_footer_td[1].get_text()) / self.checkNumber((table_footer_td[2].get_text())))
                                    data.loc[index, 'team3PM'] = self.checkNumber(table_footer_td[3].get_text())
                                    data.loc[index, 'team3PA'] = self.checkNumber(table_footer_td[4].get_text())
                                    try:
                                        data.loc[index, 'team3P%'] = "%0.2f" % (self.checkNumber(table_footer_td[3].get_text()) / self.checkNumber(table_footer_td[4].get_text()))
                                    except ZeroDivisionError:
                                        data.loc[index, 'team3P%'] = 0.0
                                    data.loc[index, 'team2PM'] = self.checkNumber(table_footer_td[1].get_text()) - self.checkNumber(table_footer_td[3].get_text())
                                    data.loc[index, 'team2PA'] = self.checkNumber(table_footer_td[2].get_text()) - self.checkNumber(table_footer_td[4].get_text())
                                    data.loc[index, 'team2P%'] = "%0.2f" % (self.checkNumber(table_footer_td[1].get_text()) - self.checkNumber(table_footer_td[3].get_text()) / self.checkNumber(table_footer_td[2].get_text()) - self.checkNumber(table_footer_td[4].get_text()))
                                    data.loc[index, 'teamFTM'] = self.checkNumber(table_footer_td[5].get_text())
                                    data.loc[index, 'teamFTA'] = self.checkNumber(table_footer_td[6].get_text())
                                    try:
                                        data.loc[index, 'teamFT%'] = "%0.2f" % (self.checkNumber(table_footer_td[5].get_text()) / self.checkNumber(table_footer_td[6].get_text()))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamFT%'] = 0.0
                                    data.loc[index, 'teamORB'] = self.checkNumber(table_footer_td[7].get_text())
                                    data.loc[index, 'teamTRB'] = self.checkNumber(table_footer_td[8].get_text())
                                    data.loc[index, 'teamDRB'] = self.checkNumber(table_footer_td[8].get_text()) - self.checkNumber(table_footer_td[7].get_text()) 
                                    data.loc[index, 'teamAST'] = self.checkNumber(table_footer_td[9].get_text())
                                    data.loc[index, 'teamSTL'] = self.checkNumber(table_footer_td[10].get_text())
                                    data.loc[index, 'teamBLK'] = self.checkNumber(table_footer_td[11].get_text())
                                    data.loc[index, 'teamTO'] = self.checkNumber(table_footer_td[12].get_text())
                                    data.loc[index, 'teamPF'] = self.checkNumber(table_footer_td[13].get_text())
                                    data.loc[index, 'teamPTS'] = self.checkNumber(table_footer_td[14].get_text())
                                    

                                    #home team stats
                                    table_footer = tables_score[1].find('tfoot')
                                    table_footer_tr = table_footer.find('tr')
                                    table_footer_td = table_footer_tr.findAll('td')

                                    data.loc[index, 'opptMin'] = self.checkNumber(table_footer_td[0].get_text())
                                    data.loc[index, 'opptFGM'] = self.checkNumber(table_footer_td[1].get_text())
                                    data.loc[index, 'opptFGA']  = self.checkNumber(table_footer_td[2].get_text())
                                    try:
                                        data.loc[index, 'opptFG%']  = "%0.2f" % (self.checkNumber(table_footer_td[1].get_text()) / self.checkNumber(table_footer_td[2].get_text()))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptFG%']  = 0.0
                                    data.loc[index, 'oppt3PM'] = self.checkNumber(table_footer_td[3].get_text())
                                    data.loc[index, 'oppt3PA'] = self.checkNumber(table_footer_td[4].get_text())
                                    try:
                                        data.loc[index, 'oppt3P%'] = "%0.2f" % (self.checkNumber(table_footer_td[3].get_text()) / self.checkNumber(table_footer_td[4].get_text()))
                                    except ZeroDivisionError:
                                        data.loc[index, 'oppt3P%'] = 0.0
                                    data.loc[index, 'oppt2PM'] = self.checkNumber(table_footer_td[1].get_text()) - self.checkNumber(table_footer_td[3].get_text())
                                    data.loc[index, 'oppt2PA'] = self.checkNumber(table_footer_td[2].get_text()) - self.checkNumber(table_footer_td[4].get_text())
                                    data.loc[index, 'oppt2P%'] = "%0.2f" % (self.checkNumber(table_footer_td[1].get_text()) - self.checkNumber(table_footer_td[3].get_text()) / self.checkNumber(table_footer_td[2].get_text()) - self.checkNumber(table_footer_td[4].get_text()))
                                    data.loc[index, 'opptFTM'] = self.checkNumber(table_footer_td[5].get_text())
                                    data.loc[index, 'opptFTA'] = self.checkNumber(table_footer_td[6].get_text())
                                    try:
                                        data.loc[index, 'opptFT%'] = "%0.2f" % (self.checkNumber(table_footer_td[5].get_text()) / self.checkNumber(table_footer_td[6].get_text()))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptFT%'] = 0.0
                                    data.loc[index, 'opptORB'] = self.checkNumber(table_footer_td[7].get_text())
                                    data.loc[index, 'opptTRB'] = self.checkNumber(table_footer_td[8].get_text())
                                    data.loc[index, 'opptDRB'] = self.checkNumber(table_footer_td[8].get_text()) - self.checkNumber(table_footer_td[7].get_text()) 
                                    data.loc[index, 'opptAST'] = self.checkNumber(table_footer_td[9].get_text())
                                    data.loc[index, 'opptSTL'] = self.checkNumber(table_footer_td[10].get_text())
                                    data.loc[index, 'opptBLK'] = self.checkNumber(table_footer_td[11].get_text())
                                    data.loc[index, 'opptTO'] = self.checkNumber(table_footer_td[12].get_text())
                                    data.loc[index, 'opptPF'] = self.checkNumber(table_footer_td[13].get_text())
                                    data.loc[index, 'opptPTS'] = self.checkNumber(table_footer_td[14].get_text())

                                    #away team advanced stats
                                    try:
                                        data.loc[index, 'teamTREB%'] = "%0.2f" % ((float(data.loc[index, 'teamTRB']) * 100)/(float(data.loc[index, 'teamTRB']) + float(data.loc[index, 'opptTRB'])))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamTREB%'] = 0.0
                                    try:
                                        data.loc[index, 'teamASST%'] = "%0.2f" % (float(data.loc[index, 'teamAST'])/float(data.loc[index, 'teamFGM']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamASST%'] = 0.0
                                    try:
                                        data.loc[index, 'teamTS%'] = "%0.2f" % (float(data.loc[index, 'teamPTS'])/(2 * float(data.loc[index, 'teamFGA']) + (float(data.loc[index, 'teamFTA']) * 0.44)))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamTS%'] = 0.0
                                    try:
                                        data.loc[index, 'teamEFG%'] = "%0.2f" % ((float(data.loc[index, 'teamFGM']) + (float(data.loc[index, 'team3PM'])/2))/float(data.loc[index, 'teamFGA']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamEFG%'] = 0.0
                                    try:
                                        data.loc[index, 'teamOREB%'] = "%0.2f" % ((float(data.loc[index, 'teamORB']) * 100)/(float(data.loc[index, 'teamORB']) + float(data.loc[index, 'opptDRB'])))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamOREB%'] = 0.0
                                    try:
                                        data.loc[index, 'teamDREB%'] = "%0.2f" % ((float(data.loc[index, 'teamDRB']) * 100)/(float(data.loc[index, 'teamDRB']) + float(data.loc[index, 'opptORB'])))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamDREB%'] = 0.0
                                    try:
                                        data.loc[index, 'teamTO%'] = "%0.2f" % ((float(data.loc[index, 'teamTO']) * 100)/(float(data.loc[index, 'teamFGA']) + (0.44 * float(data.loc[index, 'teamFTA'])) + float(data.loc[index, 'teamTO'])))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamTO%'] = 0.0
                                    try:
                                        data.loc[index, 'teamPoss'] = "%0.2f" % (float(data.loc[index, 'teamFGA']) - (float(data.loc[index, 'teamORB'])/(((float(data.loc[index, 'teamORB']) + float(data.loc[index, 'opptDRB']))) * (float(data.loc[index, 'teamFGA']) - float(data.loc[index, 'teamFGM'])) * 1.07 + float(data.loc[index, 'teamTO']) + (0.4 * float(data.loc[index, 'teamFTA'])))))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamPoss'] = 0.0
                                    try:
                                        data.loc[index, 'teamSTL%'] = "%0.2f" % ((float(data.loc[index, 'teamSTL']) * 100)/float(data.loc[index, 'teamPoss']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamSTL%'] = 0.0
                                    try:
                                        data.loc[index, 'teamBLK%'] = "%0.2f" % ((float(data.loc[index, 'teamBLK']) * 100)/float(data.loc[index, 'teamPoss']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamBLK%'] = 0.0
                                    try:
                                        data.loc[index, 'teamBLKR'] = "%0.2f" % ((float(data.loc[index, 'teamBLK']) * 100)/float(data.loc[index, 'oppt2PA']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamBLKR'] = 0.0
                                    try:
                                        data.loc[index, 'teamPPS'] = "%0.2f" % (float(data.loc[index, 'teamPTS'])/float(data.loc[index, 'teamFGA']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamPPS'] = 0.0
                                    try:
                                        data.loc[index, 'teamFIC'] = "%0.2f" % (float(data.loc[index, 'teamPTS']) + float(data.loc[index, 'teamORB']) + (0.75 * float(data.loc[index, 'teamDRB'])) + float(data.loc[index, 'teamAST']) + float(data.loc[index, 'teamSTL']) + float(data.loc[index, 'teamBLK']) - (0.75 * float(data.loc[index, 'teamFGA'])) - (0.375 * float(data.loc[index, 'teamFTA'])) - float(data.loc[index, 'teamTO']) - float(data.loc[index, 'teamPF'])/2)
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamFIC'] = 0.0
                                    try:
                                        data.loc[index, 'teamFIC40'] = "%0.2f" % ((float(data.loc[index, 'teamFIC']) * 40 * 5)/float(data.loc[index, 'teamMin']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamFIC40'] = 0.0
                                    try:
                                        data.loc[index, 'teamOrtg'] = "%0.2f" % ((float(data.loc[index, 'teamPTS']) * 100)/float(data.loc[index, 'teamPoss']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamOrtg'] = 0.0
                                    try:
                                        data.loc[index, 'teamDrtg'] = "%0.2f" % ((float(data.loc[index, 'opptPTS']) * 100)/float(data.loc[index, 'teamPoss']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamDrtg'] = 0.0
                                    try:
                                        data.loc[index, 'teamEDiff'] = "%0.2f" % (float(data.loc[index, 'teamOrtg']) - float(data.loc[index, 'teamDrtg']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamEDiff'] = 0.0
                                    try:
                                        data.loc[index, 'teamPlay%'] = "%0.2f" % (float(data.loc[index, 'teamFGM']) / (float(data.loc[index, 'teamFGA']) - float(data.loc[index, 'teamORB']) + float(data.loc[index, 'teamTO'])))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamPlay%'] = 0.0
                                    try:
                                        data.loc[index, 'teamAR'] = "%0.2f" % ((float(data.loc[index, 'teamAST']) * 100)/(float(data.loc[index, 'teamFGA']) - (0.44 * float(data.loc[index, 'teamFTA'])) + float(data.loc[index, 'teamAST']) + float(data.loc[index, 'teamTO'])))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamAR'] = 0.0
                                    try:
                                        data.loc[index, 'teamAST/TO'] = "%0.2f" % (float(data.loc[index, 'teamAST']) / float(data.loc[index, 'teamTO']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamAST/TO'] = 0.0
                                    try:
                                        data.loc[index, 'teamPace'] = "%0.2f" % ((float(data.loc[index, 'teamPoss']) * 48 * 5) / float(data.loc[index, 'teamMin']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamPace'] = 0.0
                                    try:
                                        data.loc[index, 'teamSTL/TO'] = "%0.2f" % (float(data.loc[index, 'teamSTL']) / float(data.loc[index, 'teamTO']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamSTL/TO'] = 0.0
                                        
                                    #home team advanced stats
                                    try:
                                        data.loc[index, 'opptTREB%'] = "%0.2f" % ((float(data.loc[index, 'opptTRB']) * 100)/(float(data.loc[index, 'opptTRB']) + float(data.loc[index, 'teamTRB'])))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptTREB%'] = 0.0
                                    try:
                                        data.loc[index, 'opptASST%'] = "%0.2f" % (float(data.loc[index, 'opptAST'])/float(data.loc[index, 'opptFGM']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptASST%'] = 0.0
                                    try:
                                        data.loc[index, 'opptTS%'] = "%0.2f" % (float(data.loc[index, 'opptPTS'])/(2 * float(data.loc[index, 'opptFGA']) + (float(data.loc[index, 'opptFTA']) * 0.44)))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptTS%'] = 0.0
                                    try:
                                        data.loc[index, 'opptEFG%'] = "%0.2f" % ((float(data.loc[index, 'opptFGM']) + (float(data.loc[index, 'oppt3PM'])/2))/float(data.loc[index, 'opptFGA']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptEFG%'] = 0.0
                                    try:
                                        data.loc[index, 'opptOREB%'] = "%0.2f" % ((float(data.loc[index, 'opptORB']) * 100)/(float(data.loc[index, 'opptORB']) + float(data.loc[index, 'teamDRB'])))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptOREB%'] = 0.0
                                    try:
                                        data.loc[index, 'opptDREB%'] = "%0.2f" % ((float(data.loc[index, 'opptDRB']) * 100)/(float(data.loc[index, 'opptDRB']) + float(data.loc[index, 'teamORB'])))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptDREB%'] = 0.0
                                    try:
                                        data.loc[index, 'opptTO%'] = "%0.2f" % ((float(data.loc[index, 'opptTO']) * 100)/(float(data.loc[index, 'opptFGA']) + (0.44 * float(data.loc[index, 'opptFTA'])) + float(data.loc[index, 'opptTO'])))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptTO%'] =  0.0
                                    try:
                                        data.loc[index, 'opptPoss'] = "%0.2f" % (float(data.loc[index, 'opptFGA']) - (float(data.loc[index, 'opptORB'])/(float(data.loc[index, 'opptORB']) + float(data.loc[index, 'opptDRB']))) * (float(data.loc[index, 'opptFGA']) - float(data.loc[index, 'opptFGM'])) * 1.07 + float(data.loc[index, 'opptTO']) + (0.4 * float(data.loc[index, 'opptFTA'])))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptPoss'] = 0.0
                                    try:
                                        data.loc[index, 'opptSTL%'] = "%0.2f" % ((float(data.loc[index, 'opptSTL']) * 100)/float(data.loc[index, 'opptPoss']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptSTL%'] = 0.0
                                    try:
                                        data.loc[index, 'opptBLK%'] = "%0.2f" % ((float(data.loc[index, 'opptBLK']) * 100)/float(data.loc[index, 'opptPoss']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptBLK%'] = 0.0
                                    try:
                                        data.loc[index, 'opptBLKR'] = "%0.2f" % ((float(data.loc[index, 'opptBLK']) * 100)/float(data.loc[index, 'team2PA']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptBLKR'] = 0.0
                                    try:
                                        data.loc[index, 'opptPPS'] = "%0.2f" % (float(data.loc[index, 'opptPTS'])/float(data.loc[index, 'opptFGA']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptPPS'] = 0.0
                                    try:
                                        data.loc[index, 'opptFIC'] = "%0.2f" % (float(data.loc[index, 'opptPTS']) + float(data.loc[index, 'opptORB']) + (0.75 * float(data.loc[index, 'opptDRB'])) + float(data.loc[index, 'opptAST']) + float(data.loc[index, 'opptSTL']) + float(data.loc[index, 'opptBLK']) - (0.75 * float(data.loc[index, 'opptFGA'])) - (0.375 * float(data.loc[index, 'opptFTA'])) - float(data.loc[index, 'opptTO']) - float(data.loc[index, 'opptPF'])/2)
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptFIC'] = 0.0
                                    try:
                                        data.loc[index, 'opptFIC40'] = "%0.2f" % ((float(data.loc[index, 'opptFIC']) * 40 * 5)/float(data.loc[index, 'opptMin']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptFIC40'] = 0.0
                                    try:
                                        data.loc[index, 'opptOrtg'] = "%0.2f" % ((float(data.loc[index, 'opptPTS']) * 100)/float(data.loc[index, 'opptPoss']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptOrtg'] = 0.0
                                    try:
                                        data.loc[index, 'opptDrtg'] = "%0.2f" % ((float(data.loc[index, 'teamPTS']) * 100)/float(data.loc[index, 'opptPoss']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptDrtg'] = 0.0
                                    try:
                                        data.loc[index, 'opptEDiff'] = "%0.2f" % (float(data.loc[index, 'opptOrtg']) - float(data.loc[index, 'opptDrtg']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptEDiff'] = 0.0
                                    try:
                                        data.loc[index, 'opptPlay%'] = "%0.2f" % (float(data.loc[index, 'opptFGM']) / (float(data.loc[index, 'opptFGA']) - float(data.loc[index, 'opptORB']) + float(data.loc[index, 'opptTO'])))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptPlay%'] = 0.0
                                    try:
                                        data.loc[index, 'opptAR'] = "%0.2f" % ((float(data.loc[index, 'opptAST']) * 100)/(float(data.loc[index, 'opptFGA']) - (0.44 * float(data.loc[index, 'opptFTA'])) + float(data.loc[index, 'opptAST']) + float(data.loc[index, 'opptTO'])))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptAR'] = 0.0
                                    try:
                                        data.loc[index, 'opptAST/TO'] = "%0.2f" % (float(data.loc[index, 'opptAST']) / float(data.loc[index, 'opptTO']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptAST/TO'] = 0.0
                                    try:
                                        data.loc[index, 'opptPace'] = "%0.2f" % ((float(data.loc[index, 'opptPoss']) * 48 * 5) / float(data.loc[index, 'opptMin']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptPace'] = 0.0
                                    try:
                                        data.loc[index, 'opptSTL/TO'] = "%0.2f" % (float(data.loc[index, 'opptSTL']) / float(data.loc[index, 'opptTO']))
                                    except ZeroDivisionError:
                                        data.loc[index, 'opptSTL/TO'] = 0.0
                            else:
                                print("Error: " + request.status_code)
                                exit()
                    else:
                        #reached the playoffs label on the table
                        seasonType = 'Playoffs'

                    index += 1
                    time.sleep(0.2)
                    bar.update(index+1)
            else:
                print("Error: " + request.status_code)
                exit()
        
            print("\nSaving the data from the " + str(first_year) + " season!\n")
            data.to_csv(str(first_year) + "_officialBoxScore.csv", index=False)
            first_year += 1

    #check if a value is empty
    #if it is we return 0.0
    def checkNumber(self, number):
        if number == '':
            return 0.0
        else:
            return float(number)

if __name__ == "__main__":
    wrapper = WNBAWrapper()
    wrapper.getBoxScore()