import requests
from bs4 import BeautifulSoup
from _datetime import date
import progressbar
import time
import pandas as pd

class WNBAWrapper:

    def __init__(self):
        self.url = 'https://www.basketball-reference.com'
        self.full_url = ''

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

        first_year = 2019
        last_year = 2019

        last_game = {'ATL': '', 'CHI': '', 'CON': '', 'CHA': '', 'CLE': '', 'DAL': '', 'HOU': '',
                    'IND': '', 'LAS': '', 'LVA': '', 'MIA': '', 'MIN': '', 'NYL': '', 'PHO': '',
                    'POR': '', 'SAC': '', 'SAS': '', 'SEA': '', 'TUL': '', 'UTA': '', 'WAS': ''}

        wins = {'ATL': 0, 'CHI': 0, 'CON': 0, 'CHA': 0, 'CLE': 0, 'DAL': 0, 'HOU': 0,
                'IND': 0, 'LAS': 0, 'LVA': 0, 'MIA': 0, 'MIN': 0, 'NYL': 0, 'PHO': 0,
                'POR': 0, 'SAC': 0, 'SAS': 0, 'SEA': 0, 'TUL': 0, 'UTA': 0, 'WAS': 0}

        losses = {'ATL': 0, 'CHI': 0, 'CON': 0, 'CHA': 0, 'CLE': 0, 'DAL': 0, 'HOU': 0,
                  'IND': 0, 'LAS': 0, 'LVA': 0, 'MIA': 0, 'MIN': 0, 'NYL': 0, 'PHO': 0,
                  'POR': 0, 'SAC': 0, 'SAS': 0, 'SEA': 0, 'TUL': 0, 'UTA': 0, 'WAS': 0}

        while first_year <= last_year:

            #start_time = time.time()
            bar = progressbar.ProgressBar(max_value = progressbar.UnknownLength)
            
            data = pd.DataFrame(columns = columns)

            seasonType = 'Regular'

            print("\nCollecting the data from the " +str(first_year)+ " season. Please wait!")

            self.full_url = self.url + '/wnba/years/' + str(first_year) + '-schedule.html'
            request = requests.get(self.full_url)
            
            if request.status_code == 200:
                soup = BeautifulSoup(request.text, 'html.parser')

                boxscore_table = soup.find('table', {'id': 'schedule'})
                table_body = boxscore_table.find('tbody')
                table_trs = table_body.findAll('tr')
                index = 0

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
                            last_game[team_home_abbr_formated] == game_date_formated

                        #first game of the season (away team)
                        if last_game[team_away_abbr_formated] == '':
                            last_game[team_away_abbr_formated] = game_date_formated
                            data.loc[index, 'teamDayOff'] = 0
                        else:
                            last_date = last_game[team_away_abbr_formated]
                            days_off = game_date_formated - last_date
                            data.loc[index, 'teamDayOff'] = int(days_off.days) - 1

                            #replace the last game date for the current date
                            last_game[team_away_abbr_formated] == game_date_formated

                        #boxscore link
                        tablescore_cell = tr.find('td', {'class': 'center'})

                        if tablescore_cell:
                            cell_anchor = tablescore_cell.find('a');
                            cell_anchor = cell_anchor['href']

                            boxscore_game = requests.get(self.url + cell_anchor)
                            
                            if boxscore_game.status_code == 200:
                                
                                #first table = away team
                                #second table = home team
                                soup_boxscore = BeautifulSoup(boxscore_game.text, 'html.parser')
                                tables_score = soup_boxscore.findAll('table', {'class': 'suppress_all'})

                                #away team stats
                                table_footer = tables_score[0].find('tfoot')
                                table_footer_tr = table_footer.find('tr')
                                table_footer_td = table_footer_tr.findAll('td')

                                data.loc[index, 'teamMin'] = table_footer_td[0].get_text()
                                data.loc[index, 'teamFGM'] = table_footer_td[1].get_text()
                                data.loc[index, 'teamFGA']  = table_footer_td[2].get_text()
                                data.loc[index, 'teamFG%']  = "%0.2f" % (float(table_footer_td[1].get_text()) / float(table_footer_td[2].get_text()))
                                data.loc[index, 'team3PM'] = table_footer_td[3].get_text()
                                data.loc[index, 'team3PA'] = table_footer_td[4].get_text()
                                data.loc[index, 'team3P%'] = "%0.2f" % (float(table_footer_td[3].get_text()) / float(table_footer_td[4].get_text()))
                                data.loc[index, 'team2PM'] = int(table_footer_td[1].get_text()) - int(table_footer_td[3].get_text())
                                data.loc[index, 'team2PA'] = int(table_footer_td[2].get_text()) - int(table_footer_td[4].get_text())
                                data.loc[index, 'team2P%'] = "%0.2f" % (float(int(table_footer_td[1].get_text()) - int(table_footer_td[3].get_text())) / float(int(table_footer_td[2].get_text()) - int(table_footer_td[4].get_text())))
                                data.loc[index, 'teamFTM'] = table_footer_td[5].get_text()
                                data.loc[index, 'teamFTA'] = table_footer_td[6].get_text()
                                data.loc[index, 'teamFT%'] = "%0.2f" % (float(table_footer_td[5].get_text()) / float(table_footer_td[6].get_text()))
                                data.loc[index, 'teamORB'] = table_footer_td[7].get_text()
                                data.loc[index, 'teamTRB'] = table_footer_td[8].get_text()
                                data.loc[index, 'teamDRB'] = int(table_footer_td[8].get_text()) - int(table_footer_td[7].get_text()) 
                                data.loc[index, 'teamAST'] = table_footer_td[9].get_text()
                                data.loc[index, 'teamSTL'] = table_footer_td[10].get_text()
                                data.loc[index, 'teamBLK'] = table_footer_td[11].get_text()
                                data.loc[index, 'teamTO'] = table_footer_td[12].get_text()
                                data.loc[index, 'teamPF'] = table_footer_td[13].get_text()
                                data.loc[index, 'teamPTS'] = table_footer_td[14].get_text()
                                

                                #home team stats
                                table_footer = tables_score[1].find('tfoot')
                                table_footer_tr = table_footer.find('tr')
                                table_footer_td = table_footer_tr.findAll('td')

                                data.loc[index, 'opptMin'] = table_footer_td[0].get_text()
                                data.loc[index, 'opptFGM'] = table_footer_td[1].get_text()
                                data.loc[index, 'opptFGA']  = table_footer_td[2].get_text()
                                data.loc[index, 'opptFG%']  = "%0.2f" % (float(table_footer_td[1].get_text()) / float(table_footer_td[2].get_text()))
                                data.loc[index, 'oppt3PM'] = table_footer_td[3].get_text()
                                data.loc[index, 'oppt3PA'] = table_footer_td[4].get_text()
                                data.loc[index, 'oppt3P%'] = "%0.2f" % (float(table_footer_td[3].get_text()) / float(table_footer_td[4].get_text()))
                                data.loc[index, 'oppt2PM'] = int(table_footer_td[1].get_text()) - int(table_footer_td[3].get_text())
                                data.loc[index, 'oppt2PA'] = int(table_footer_td[2].get_text()) - int(table_footer_td[4].get_text())
                                data.loc[index, 'oppt2P%'] = "%0.2f" % (float(int(table_footer_td[1].get_text()) - int(table_footer_td[3].get_text())) / float(int(table_footer_td[2].get_text()) - int(table_footer_td[4].get_text())))
                                data.loc[index, 'opptFTM'] = table_footer_td[5].get_text()
                                data.loc[index, 'opptFTA'] = table_footer_td[6].get_text()
                                data.loc[index, 'opptFT%'] = "%0.2f" % (float(table_footer_td[5].get_text()) / float(table_footer_td[6].get_text()))
                                data.loc[index, 'opptORB'] = table_footer_td[7].get_text()
                                data.loc[index, 'opptTRB'] = table_footer_td[8].get_text()
                                data.loc[index, 'opptDRB'] = int(table_footer_td[8].get_text()) - int(table_footer_td[7].get_text()) 
                                data.loc[index, 'opptAST'] = table_footer_td[9].get_text()
                                data.loc[index, 'opptSTL'] = table_footer_td[10].get_text()
                                data.loc[index, 'opptBLK'] = table_footer_td[11].get_text()
                                data.loc[index, 'opptTO'] = table_footer_td[12].get_text()
                                data.loc[index, 'opptPF'] = table_footer_td[13].get_text()
                                data.loc[index, 'opptPTS'] = table_footer_td[14].get_text()

                                #away team advanced stats
                                data.loc[index, 'teamTREB%'] = "%0.2f" % ((float(data.loc[index, 'teamTRB']) * 100)/(float(data.loc[index, 'teamTRB']) + float(data.loc[index, 'opptTRB'])))
                                data.loc[index, 'teamASST%'] = "%0.2f" % (float(data.loc[index, 'teamAST'])/float(data.loc[index, 'teamFGM']))
                                data.loc[index, 'teamTS%'] = "%0.2f" % (float(data.loc[index, 'teamPTS'])/(2 * float(data.loc[index, 'teamFGA']) + (float(data.loc[index, 'teamFTA']) * 0.44)))
                                data.loc[index, 'teamEFG%'] = "%0.2f" % ((float(data.loc[index, 'teamFGM']) + (float(data.loc[index, 'team3PM'])/2))/float(data.loc[index, 'teamFGA']))
                                data.loc[index, 'teamOREB%'] = "%0.2f" % ((float(data.loc[index, 'teamORB']) * 100)/(float(data.loc[index, 'teamORB']) + float(data.loc[index, 'opptDRB'])))
                                data.loc[index, 'teamDREB%'] = "%0.2f" % ((float(data.loc[index, 'teamDRB']) * 100)/(float(data.loc[index, 'teamDRB']) + float(data.loc[index, 'opptORB'])))
                                data.loc[index, 'teamTO%'] = "%0.2f" % ((float(data.loc[index, 'teamTO']) * 100)/(float(data.loc[index, 'teamFGA']) + (0.44 * float(data.loc[index, 'teamFTA'])) + float(data.loc[index, 'teamTO'])))
                                data.loc[index, 'teamPoss'] = "%0.2f" % (float(data.loc[index, 'teamFGA']) - (float(data.loc[index, 'teamORB'])/(float(data.loc[index, 'teamORB']) + float(data.loc[index, 'opptDRB']))) * (float(data.loc[index, 'teamFGA']) - float(data.loc[index, 'teamFGM'])) * 1.07 + float(data.loc[index, 'teamTO']) + (0.4 * float(data.loc[index, 'teamFTA'])))
                                data.loc[index, 'teamSTL%'] = "%0.2f" % ((float(data.loc[index, 'teamSTL']) * 100)/float(data.loc[index, 'teamPoss']))
                                data.loc[index, 'teamBLK%'] = "%0.2f" % ((float(data.loc[index, 'teamBLK']) * 100)/float(data.loc[index, 'teamPoss']))
                                data.loc[index, 'teamBLKR'] = "%0.2f" % ((float(data.loc[index, 'teamBLK']) * 100)/float(data.loc[index, 'oppt2PA']))
                                data.loc[index, 'teamPPS'] = "%0.2f" % (float(data.loc[index, 'teamPTS'])/float(data.loc[index, 'teamFGA']))
                                data.loc[index, 'teamFIC'] = "%0.2f" % (float(data.loc[index, 'teamPTS']) + float(data.loc[index, 'teamORB']) + (0.75 * float(data.loc[index, 'teamDRB'])) + float(data.loc[index, 'teamAST']) + float(data.loc[index, 'teamSTL']) + float(data.loc[index, 'teamBLK']) - (0.75 * float(data.loc[index, 'teamFGA'])) - (0.375 * float(data.loc[index, 'teamFTA'])) - float(data.loc[index, 'teamTO']) - float(data.loc[index, 'teamPF'])/2)
                                data.loc[index, 'teamFIC40'] = "%0.2f" % ((float(data.loc[index, 'teamFIC']) * 40 * 5)/float(data.loc[index, 'teamMin']))
                                data.loc[index, 'teamOrtg'] = "%0.2f" % ((float(data.loc[index, 'teamPTS']) * 100)/float(data.loc[index, 'teamPoss']))
                                data.loc[index, 'teamDrtg'] = "%0.2f" % ((float(data.loc[index, 'opptPTS']) * 100)/float(data.loc[index, 'teamPoss']))
                                data.loc[index, 'teamEDiff'] = "%0.2f" % (float(data.loc[index, 'teamOrtg']) - float(data.loc[index, 'teamDrtg']))
                                data.loc[index, 'teamPlay%'] = "%0.2f" % (float(data.loc[index, 'teamFGM']) / (float(data.loc[index, 'teamFGA']) - float(data.loc[index, 'teamORB']) + float(data.loc[index, 'teamTO'])))
                                data.loc[index, 'teamAR'] = "%0.2f" % ((float(data.loc[index, 'teamAST']) * 100)/(float(data.loc[index, 'teamFGA']) - (0.44 * float(data.loc[index, 'teamFTA'])) + float(data.loc[index, 'teamAST']) + float(data.loc[index, 'teamTO'])))
                                data.loc[index, 'teamAST/TO'] = "%0.2f" % (float(data.loc[index, 'teamAST']) / float(data.loc[index, 'teamTO']))
                                data.loc[index, 'teamPace'] = "%0.2f" % ((float(data.loc[index, 'teamPoss']) * 48 * 5) / float(data.loc[index, 'teamMin']))
                                data.loc[index, 'teamSTL/TO'] = "%0.2f" % (float(data.loc[index, 'teamSTL']) / float(data.loc[index, 'teamTO']))

                                #home team advanced stats
                                data.loc[index, 'opptTREB%'] = "%0.2f" % ((float(data.loc[index, 'opptTRB']) * 100)/(float(data.loc[index, 'opptTRB']) + float(data.loc[index, 'teamTRB'])))
                                data.loc[index, 'opptASST%'] = "%0.2f" % (float(data.loc[index, 'opptAST'])/float(data.loc[index, 'opptFGM']))
                                data.loc[index, 'opptTS%'] = "%0.2f" % (float(data.loc[index, 'opptPTS'])/(2 * float(data.loc[index, 'opptFGA']) + (float(data.loc[index, 'opptFTA']) * 0.44)))
                                data.loc[index, 'opptEFG%'] = "%0.2f" % ((float(data.loc[index, 'opptFGM']) + (float(data.loc[index, 'oppt3PM'])/2))/float(data.loc[index, 'opptFGA']))
                                data.loc[index, 'opptOREB%'] = "%0.2f" % ((float(data.loc[index, 'opptORB']) * 100)/(float(data.loc[index, 'opptORB']) + float(data.loc[index, 'teamDRB'])))
                                data.loc[index, 'opptDREB%'] = "%0.2f" % ((float(data.loc[index, 'opptDRB']) * 100)/(float(data.loc[index, 'opptDRB']) + float(data.loc[index, 'teamORB'])))
                                data.loc[index, 'opptTO%'] = "%0.2f" % ((float(data.loc[index, 'opptTO']) * 100)/(float(data.loc[index, 'opptFGA']) + (0.44 * float(data.loc[index, 'opptFTA'])) + float(data.loc[index, 'opptTO'])))
                                data.loc[index, 'opptPoss'] = "%0.2f" % (float(data.loc[index, 'opptFGA']) - (float(data.loc[index, 'opptORB'])/(float(data.loc[index, 'opptORB']) + float(data.loc[index, 'opptDRB']))) * (float(data.loc[index, 'opptFGA']) - float(data.loc[index, 'opptFGM'])) * 1.07 + float(data.loc[index, 'opptTO']) + (0.4 * float(data.loc[index, 'opptFTA'])))
                                data.loc[index, 'opptSTL%'] = "%0.2f" % ((float(data.loc[index, 'opptSTL']) * 100)/float(data.loc[index, 'opptPoss']))
                                data.loc[index, 'opptBLK%'] = "%0.2f" % ((float(data.loc[index, 'opptBLK']) * 100)/float(data.loc[index, 'opptPoss']))
                                data.loc[index, 'opptBLKR'] = "%0.2f" % ((float(data.loc[index, 'opptBLK']) * 100)/float(data.loc[index, 'team2PA']))
                                data.loc[index, 'opptPPS'] = "%0.2f" % (float(data.loc[index, 'opptPTS'])/float(data.loc[index, 'opptFGA']))
                                data.loc[index, 'opptFIC'] = "%0.2f" % (float(data.loc[index, 'opptPTS']) + float(data.loc[index, 'opptORB']) + (0.75 * float(data.loc[index, 'opptDRB'])) + float(data.loc[index, 'opptAST']) + float(data.loc[index, 'opptSTL']) + float(data.loc[index, 'opptBLK']) - (0.75 * float(data.loc[index, 'opptFGA'])) - (0.375 * float(data.loc[index, 'opptFTA'])) - float(data.loc[index, 'opptTO']) - float(data.loc[index, 'opptPF'])/2)
                                data.loc[index, 'opptFIC40'] = "%0.2f" % ((float(data.loc[index, 'opptFIC']) * 40 * 5)/float(data.loc[index, 'opptMin']))
                                data.loc[index, 'opptOrtg'] = "%0.2f" % ((float(data.loc[index, 'opptPTS']) * 100)/float(data.loc[index, 'opptPoss']))
                                data.loc[index, 'opptDrtg'] = "%0.2f" % ((float(data.loc[index, 'teamPTS']) * 100)/float(data.loc[index, 'opptPoss']))
                                data.loc[index, 'opptEDiff'] = "%0.2f" % (float(data.loc[index, 'opptOrtg']) - float(data.loc[index, 'opptDrtg']))
                                data.loc[index, 'opptPlay%'] = "%0.2f" % (float(data.loc[index, 'opptFGM']) / (float(data.loc[index, 'opptFGA']) - float(data.loc[index, 'opptORB']) + float(data.loc[index, 'opptTO'])))
                                data.loc[index, 'opptAR'] = "%0.2f" % ((float(data.loc[index, 'opptAST']) * 100)/(float(data.loc[index, 'opptFGA']) - (0.44 * float(data.loc[index, 'opptFTA'])) + float(data.loc[index, 'opptAST']) + float(data.loc[index, 'opptTO'])))
                                data.loc[index, 'opptAST/TO'] = "%0.2f" % (float(data.loc[index, 'opptAST']) / float(data.loc[index, 'opptTO']))
                                data.loc[index, 'opptPace'] = "%0.2f" % ((float(data.loc[index, 'opptPoss']) * 48 * 5) / float(data.loc[index, 'opptMin']))
                                data.loc[index, 'opptSTL/TO'] = "%0.2f" % (float(data.loc[index, 'opptSTL']) / float(data.loc[index, 'opptTO']))

                            else:
                                print("Error: " + request.status_code)
                                exit()
                    else:
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

if __name__ == "__main__":
    wrapper = WNBAWrapper()
    wrapper.getBoxScore()