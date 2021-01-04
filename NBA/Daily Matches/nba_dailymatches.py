from bs4 import BeautifulSoup
import requests
from datetime import date

class DailyMatches:

    def __init__(self, date):
        self.date = date
    
    def GetNBAMatches(self):
        
        nba_schedule_url = 'https://www.espn.com/nba/schedule/_/date/' + self.date

        web_request = requests.get(nba_schedule_url)
        soup = BeautifulSoup(web_request.text, 'html.parser')
        nba_games_table = soup.find('table', {'class': 'schedule has-team-logos align-left'})
        nba_games_table_body = nba_games_table.find('tbody')
        nba_games_table_rows = nba_games_table_body.find_all('tr')
        
        teams_names = []

        for tr in nba_games_table_rows:
            
            datas = tr.find_all('td')
            names = []

            for td in datas:

                teams = td.find_all(class_='team-name')

                for team in teams:

                    name = team.find_all('span')
                    names.append(name[0].get_text())
                
            teams_names.append(names)
            
        return teams_names
    
    def format(self, matches):

        teams_fullnames = {'Atlanta': 'Atlanta Hawks', 'Brooklyn': 'Brooklyn Nets', 'Boston': 'Boston Celtics', 'Charlotte': 'Charlotte Hornets', 'Chicago': 'Chicago Bulls',
                           'Cleveland': 'Cleveland Cavaliers', 'Dallas': 'Dallas Mavericks', 'Denver': 'Denver Nuggets', 'Detroit': 'Detroit Pistons', 'Golden State': 'Golden State Warriors',
                           'Houston': 'Houston Rockets', 'Indiana': 'Indiana Pacers', 'LA': 'Los Angeles Clippers', 'Los Angeles': 'Los Angeles Lakers', 'Memphis': 'Memphis Grizzlies',
                           'Miami': 'Miami Heat', 'Milwaukee': 'Milwaukee Bucks', 'Minnesota': 'Minnesota Timberwolves', 'New Orleans': 'New Orleans Pelicans', 'New York': 'New York Knicks',
                           'Oklahoma City': 'Oklahoma City Thunder', 'Orlando': 'Orlando Magic', 'Philadelphia': 'Philadelphia 76ers', 'Phoenix': 'Phoenix Suns', 'Portland': 'Portland Trail Blazers',
                           'San Antonio': 'San Antonio Spurs', 'Sacramento': 'Sacramento Kings', 'Toronto': 'Toronto Raptors', 'Utah': 'Utah Jazz', 'Washington' : 'Washington Wizards'}
        
        for match in matches:
            match[0] = teams_fullnames[match[0]]
            match[1] = teams_fullnames[match[1]]
        
        return matches

    def HomeTeams(self, matches):
        
        home_teams = []

        for match in matches:
            home_teams.append(match[1])

        return home_teams

    def AwayTeams(self, matches):
        
        away_teams = []

        for match in matches:
            away_teams.append(match[0])

        return away_teams
    
    def GetDate(self):
        return self.date

if __name__ == "__main__":
    
    #get the current date
    actual_date =  date.today()
    actual_date = str(actual_date).split('-')

    #format the date
    actual_date_formated = ("").join(actual_date)

    matches = DailyMatches(actual_date_formated)

    #get the games that will be playing today
    #games that is already finish will not be returned!
    today_matches = matches.GetNBAMatches()

    #format the teams names
    today_matches_formated = matches.format(today_matches)
    
    for match in today_matches:

        print("" + match[0] + " at " + match[1])