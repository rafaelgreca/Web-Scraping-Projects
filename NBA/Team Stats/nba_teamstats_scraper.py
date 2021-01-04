from bs4 import BeautifulSoup
import requests
import pandas as pd

class Scrapper():

    def __init__(self, season, season_type):
        self.season_type = season_type
        self.season = season
        self.url = 'https://www.espn.com/nba/stats/team/_/season/'

    def getTeamStats(self):
        
        teams = []
        teams_gp = []
        teams_pts = []
        teams_fgm = []
        teams_fga = []
        teams_fg_pct = []
        teams_3pm = []
        teams_3pa = []
        teams_3p_pct = []
        teams_ftm = []
        teams_fta = []
        teams_ft_pct = []
        teams_or = []
        teams_dr = []
        teams_reb = []
        teams_ast = []
        teams_stl = []
        teams_blk = []
        teams_to = []
        teams_pf = []

        if self.season_type == 'Regular':
            full_url = self.url + str(self.season) + '/seasontype/2'
        else:
            full_url = self.url + str(self.season) + '/seasontype/3'

        request = requests.get(full_url)
        soup = BeautifulSoup(request.text, 'html.parser')
        table_team_names = soup.find('div', attrs = {'class' : 'ResponsiveTable ResponsiveTable--fixed-left mt4 Table2__title--remove-capitalization'})
        table_team_names = table_team_names.find('div', attrs = {'class' : 'flex'})
        team_names = table_team_names.find('tbody', attrs = {'class' : 'Table__TBODY'})
        team_names = team_names.find_all('a', attrs = {'class' : 'AnchorLink', 'tabindex' : '0'})

        for i in range(len(team_names)):
            if i%2!=0:
                teams.append(team_names[i].text)

        table_team_stats = table_team_names.find('div', attrs = {'class' : 'Table__Scroller'})
        team_stats = table_team_stats.find('tbody', attrs = {'class' : 'Table__TBODY'})
        
        for team in team_stats:

            team_stats = team.find_all('div', attrs = {'class' : ''})
            
            teams_gp.append(team_stats[0].text)
            teams_pts.append(team_stats[1].text)
            teams_fgm.append(team_stats[2].text)
            teams_fga.append(team_stats[3].text)
            teams_fg_pct.append(team_stats[4].text)
            teams_3pm.append(team_stats[5].text)
            teams_3pa.append(team_stats[6].text)
            teams_3p_pct.append(team_stats[7].text)
            teams_ftm.append(team_stats[8].text)
            teams_fta.append(team_stats[9].text)
            teams_ft_pct.append(team_stats[10].text)
            teams_or.append(team_stats[11].text)
            teams_dr.append(team_stats[12].text)
            teams_reb.append(team_stats[13].text)
            teams_ast.append(team_stats[14].text)
            teams_stl.append(team_stats[15].text)
            teams_blk.append(team_stats[16].text)
            teams_to.append(team_stats[17].text)
            teams_pf.append(team_stats[18].text)
        
        data = {'Team' : teams, 'GP' : teams_gp, 'PTS' : teams_pts, 'FGM' : teams_fgm, 'FGA' : teams_fga, 'FG%' : teams_fg_pct,
                '3PM' : teams_3pm, '3PA' : teams_3pa, '3P%' : teams_3p_pct, 'FTM' : teams_ftm, 'FTA' : teams_fta,
                'FT%' : teams_ft_pct, 'OR' : teams_or, 'DR' : teams_dr, 'REB' : teams_reb, 'AST' : teams_ast, 
                'STL' : teams_stl, 'BLK' : teams_to, 'PF' : teams_pf}

        dataframe = pd.DataFrame(data = data)

        csv_name = str(self.season) + '_' + str(self.season_type) + '_TeamFinalStats.csv'
        dataframe.to_csv(csv_name, index = False)

if __name__ == "__main__":
    
    scrap = Scrapper(2020, 'Regular')
    scrap.getTeamStats()
