import requests
from bs4 import BeautifulSoup

class WNBAWrapper:

    def __init__(self):
        self.url = 'https://www.basketball-reference.com'
        self.full_url = ''

    def getBoxScore(self):
        first_year = 1997
        last_year = 1997

        days_off = {'ATL': '', 'CHI': '', 'CON': '', 'CHA': '', 'CLE': '', 'HOU': '',
                    'IND': '', 'LAS': '', 'MIA': '', 'MIN': '', 'NYL': '', 'PHO': '',
                    'POR': '', 'SAC': '', 'SAS': '', 'SEA': '', 'TUL': '', 'UTA': '', 'WAS': ''}

        last_game = {'ATL': '', 'CHI': '', 'CON': '', 'CHA': '', 'CLE': '', 'HOU': '',
                    'IND': '', 'LAS': '', 'MIA': '', 'MIN': '', 'NYL': '', 'PHO': '',
                    'POR': '', 'SAC': '', 'SAS': '', 'SEA': '', 'TUL': '', 'UTA': '', 'WAS': ''}

        wins = {'ATL': 0, 'CHI': 0, 'CON': 0, 'CHA': 0, 'CLE': 0, 'HOU': 0,
                'IND': 0, 'LAS': 0, 'MIA': 0, 'MIN': 0, 'NYL': 0, 'PHO': 0,
                'POR': 0, 'SAC': 0, 'SAS': 0, 'SEA': 0, 'TUL': 0, 'UTA': 0, 'WAS': 0}

        losses = {'ATL': 0, 'CHI': 0, 'CON': 0, 'CHA': 0, 'CLE': 0, 'HOU': 0,
                  'IND': 0, 'LAS': 0, 'MIA': 0, 'MIN': 0, 'NYL': 0, 'PHO': 0,
                  'POR': 0, 'SAC': 0, 'SAS': 0, 'SEA': 0, 'TUL': 0, 'UTA': 0, 'WAS': 0}

        while first_year <= last_year:
            
            self.full_url = self.url + '/wnba/years/' + str(first_year) + '-schedule.html'
            request = requests.get(self.full_url)
            
            if request.status_code == 200:
                soup = BeautifulSoup(request.text, 'html.parser')

                boxscore_table = soup.find('table', {'id': 'schedule'})
                table_body = boxscore_table.find('tbody')
                table_trs = table_body.findAll('tr')
                
                for tr in table_trs:
                                       
                    #get teams abbreviations
                    teams_abbr = tr.findAll('td', {'class': 'left'})
                    
                    #away team
                    team_away_abbr_anchor = teams_abbr[0].find('a')
                    team_away_abbr_anchor = team_away_abbr_anchor['href']
                    team_away_abbr_formated = str(team_away_abbr_anchor).split('/', 4)[3]
                    print('AWAY: ' + team_away_abbr_formated)

                    #home team
                    team_home_abbr_anchor = teams_abbr[1].find('a')
                    team_home_abbr_anchor = team_home_abbr_anchor['href']
                    team_home_abbr_formated = str(team_home_abbr_anchor).split('/', 4)[3]
                    print('HOME: ' + team_home_abbr_formated)

                    #get teams total points
                    teams_total_points = tr.findAll('td', {'class': 'right'})
                    total_points_away = teams_total_points[0].get_text()
                    total_points_home = teams_total_points[1].get_text()

                    if total_points_home > total_points_away:
                        wins[team_home_abbr_formated] += 1
                        losses[team_away_abbr_formated] += 1
                    else:
                        losses[team_home_abbr_formated] += 1
                        wins[team_away_abbr_formated] += 1

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
                            aux = 1

                            for table in tables_score:

                                table_footer = table.find('tfoot')
                                table_footer_tr = table_footer.find('tr')
                                table_footer_td = table_footer_tr.findAll('td')

                                if aux == 1:
                                    time_away = table_footer_td[0].get_text()
                                    fg_away = table_footer_td[1].get_text()
                                    fga_away = table_footer_td[2].get_text()
                                    fg3_away = table_footer_td[3].get_text()
                                    fg3a_away = table_footer_td[4].get_text()
                                    ft_away = table_footer_td[5].get_text()
                                    fta_away = table_footer_td[6].get_text()
                                    orb_away = table_footer_td[7].get_text()
                                    trb_away = table_footer_td[8].get_text()
                                    ast_away = table_footer_td[9].get_text()
                                    stl_away = table_footer_td[10].get_text()
                                    blk_away = table_footer_td[11].get_text()
                                    tov_away = table_footer_td[12].get_text()
                                    pf_away = table_footer_td[13].get_text()
                                    pts_away = table_footer_td[14].get_text()
                                    aux = 2
                                else:
                                    time_home = table_footer_td[0].get_text()
                                    fg_home = table_footer_td[1].get_text()
                                    fga_home = table_footer_td[2].get_text()
                                    fg3_home = table_footer_td[3].get_text()
                                    fg3a_home = table_footer_td[4].get_text()
                                    ft_home = table_footer_td[5].get_text()
                                    fta_home = table_footer_td[6].get_text()
                                    orb_home = table_footer_td[7].get_text()
                                    trb_home = table_footer_td[8].get_text()
                                    ast_home = table_footer_td[9].get_text()
                                    stl_home = table_footer_td[10].get_text()
                                    blk_home = table_footer_td[11].get_text()
                                    tov_home = table_footer_td[12].get_text()
                                    pf_home = table_footer_td[13].get_text()
                                    pts_home = table_footer_td[14].get_text()
                                    aux = 1
                        else:
                            print("Error: " + request.status_code)
                            exit()

            else:
                print("Error: " + request.status_code)
                exit()

if __name__ == "__main__":
    wrapper = WNBAWrapper()
    wrapper.getBoxScore()