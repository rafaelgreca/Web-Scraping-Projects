from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
import re
from _datetime import date
import datetime
import time
import progressbar

class NbaBoxScoreScrapper():

    def __init__(self, folder_location):
        self.folder_location = folder_location

    def GetDatas(self, first_season = 'None', last_season = 'None', type_season = 'None'):
        
        os.chdir(self.folder_location)

        #if last season is 'None', will collect the data from the first season only
        if last_season == 'None':
            first_season_year, _ = first_season.split('-')
            first_season_year = int(first_season_year)
            last_season_year = first_season_year
        #if first season is 'None' will collect the data from 1949-50 season till the last season
        elif first_season == 'None':
            first_season_year = '1950'
            last_season_year, _ = last_season.split('-')
            last_season_year = int(last_season_year)
        else:
            first_season_year, _ = first_season.split('-')
            first_season_year = int(first_season_year)
            last_season_year, _ = last_season.split('-')
            last_season_year = int(last_season_year)
        
        #get the data within the range between the first and last season
        while first_season_year <= last_season_year:

            #start_time = time.time()
            bar = progressbar.ProgressBar(max_value = progressbar.UnknownLength)

            current_year = datetime.datetime.now()
            current_year = int(current_year.year)
            
            #columns that will be used in your csv file
            columns = ['gmDate', 'seasonType', 'season', 'teamWins', 'teamLosses', 'teamAbbr', 'teamLoc', 'teamRslt',
                        'teamDayOff', 'teamPTS', 'teamAST', 'teamTO', 'teamMin',
                        'teamSTL', 'teamBLK', 'teamPF', 'teamFGA', 'teamFGM', 'teamFG%',
                        'team2PA', 'team2PM', 'team2P%', 'team3PA', 'team3PM', 'team3P%',
                        'teamFTA', 'teamFTM', 'teamFT%', 'teamORB', 'teamDRB', 'teamTRB',
                        'teamPTS1', 'teamPTS2', 'teamPTS3', 'teamPTS4', 'teamPTS5', 'teamPTS6',
                        'teamPTS7', 'teamPTS8', 'teamPTS9', 'teamPTS10', 'teamTREB%', 'teamASST%',
                        'teamTS%', 'teamEFG%', 'teamOREB%', 'teamDREB%', 'teamTO%',
                        'teamSTL%', 'teamBLK%', 'teamBLKR', 'teamPPS', 'teamFIC',
                        'teamFIC40', 'teamOrtg', 'teamDrtg', 'teamEDiff', 'teamPlay%',
                        'teamAR', 'teamPoss', 'teamAST/TO', 'teamPace', 'teamSTL/TO', 'opptWins',
                        'opptLosses', 'opptAbbr', 'opptLoc', 'opptRslt',
                        'opptDayOff', 'opptPTS', 'opptAST', 'opptTO', 'opptMin', 'opptSTL', 'opptBLK',
                        'opptPF', 'opptFGA', 'opptFGM', 'opptFG%', 'oppt2PA', 'oppt2PM',
                        'oppt2P%', 'oppt3PA', 'oppt3PM', 'oppt3P%', 'opptFTA', 'opptFTM',
                        'opptFT%', 'opptORB', 'opptDRB', 'opptTRB', 'opptPTS1', 'opptPTS2',
                        'opptPTS3', 'opptPTS4', 'opptPTS5', 'opptPTS6', 'opptPTS7', 'opptPTS8',
                        'opptPTS9', 'opptPTS10', 'opptTREB%', 'opptASST%', 'opptTS%', 'opptEFG%',
                        'opptOREB%', 'opptDREB%', 'opptTO%', 'opptSTL%', 'opptBLK%',
                        'opptBLKR', 'opptPPS', 'opptFIC', 'opptFIC40', 'opptOrtg',
                        'opptDrtg', 'opptEDiff', 'opptPlay%', 'opptAR', 'opptAST/TO',
                        'opptSTL/TO', 'opptPoss', 'opptPace', 'matchWinner']

            data = pd.DataFrame(columns = columns)

            season = str(first_season_year) + "-" + str(first_season_year+1)[2:]

            print("\nCollecting the data from the " +season+ " season. Please wait!")

            first_season_year += 1
            playoff_first_game_date = date(2099, 12, 31)

            season_months = []

            if type_season == 'Regular' or type_season == 'None':
                url = 'https://www.basketball-reference.com/leagues/NBA_' + str(first_season_year) + '_games-'
            else:
                url = 'https://www.basketball-reference.com/playoffs/NBA_' + str(first_season_year) + '_games-'

            #get the months that had at least one game, including regular season and playoffs
            get_months_url = 'https://www.basketball-reference.com/leagues/NBA_' + str(first_season_year) + '_games.html'
            request_months = requests.get(get_months_url)
            soup_months = BeautifulSoup(request_months.text, 'html.parser')
            soup_months = soup_months.find('div', attrs = {"class": "filter"})
            months_season = soup_months.find_all('a')

            #format all the months names to be in lower case
            for i in range(len(months_season)):
                m = months_season[i].text.strip()
                season_months.append(m.lower())

            #will be used to check if that season already has finished the regular season
            #if date(first_season_year, 12, 31) - date(current_year + 1, 12, 31) == 0:

            monthss = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 
                            'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

            #get the date from the first playoffs game in that season
            playoffs_first_date = 'https://www.basketball-reference.com/playoffs/NBA_' + str(first_season_year) + '_games.html'
            request = requests.get(playoffs_first_date)

            if request:
                soup = BeautifulSoup(request.text, 'html.parser')
                game_days = soup.find_all('th', attrs={"data-stat": "date_game", "class": "left"})

                #format the data
                datee = str(game_days[0].text.strip())
                _, month_day, year = datee.split(',')
                month, day = (month_day.strip()).split(' ')
                        
                if int(day) > 0 and int(day)<10:
                    day = '0' + day

                date_formated = year.strip() + '-' + monthss[month] + '-' + day
                date_formated_url = year.strip() + monthss[month] + day
                playoff_first_game_date = date(int(year.strip()), int(monthss[month]), int(day))
            else:
                playoff_first_game_date = date(2099, 12, 31)

            index = 0

            teams_day_off = {'ATL': '', 'BKN': '', 'BOS': '', 'CHA': '', 'CHI': '', 'CLE': '', 'DAL': '', 'DEN': '', 'DET': '', 'GS': '',
                    'HOU': '', 'IND': '', 'LAC': '', 'LAL': '', 'MEM': '', 'MIA': '', 'MIL': '', 'MIN': '', 'NO': '', 'NY': '', 'DNN': '',
                    'OKC': '', 'ORL': '', 'PHI': '', 'PHO': '', 'POR': '', 'SA': '', 'SAC': '', 'TOR': '', 'UTA': '', 'WAS': '', 'NOH': '',
                    'CHO': '', 'NJN': '', 'SEA': '', 'VAN': '', 'CHH': '', 'NOK': '', 'WSB': '', 'KCK': '', 'SDC': '', 'BUF': '', 'NOJ': '',
                    'KCO': '', 'CAP': '', 'CIN': '', 'SDR': '', 'SFW': '', 'STL': '', 'SYR': '', 'CHZ': '', 'CHP': '', 'PHW': '', 'MNL': '',
                    'FTW': '', 'ROC': '', 'INO': '', 'MLH': '', 'TRI': '', 'WSC': '', 'STB': '', 'CHS': '', 'AND': '', 'SHE': '', 'WAT': '',
                    'BAL': '', 'NYN': ''}

            #get the data from every month
            for month in season_months:

                full_url = url + month + '.html'
                request = requests.get(full_url)
                soup = BeautifulSoup(request.text, 'html.parser')
                game_days = soup.find_all('th', attrs={"data-stat": "date_game", "class": "left"})
                visitor_team_names = soup.find_all('td', attrs={"data-stat": "visitor_team_name", "class": "left"})
                visitor_pts = soup.find_all('td', attrs={"data-stat": "visitor_pts", "class": "right"})
                home_team_names = soup.find_all('td', attrs={"data-stat": "home_team_name", "class": "left"})
                home_pts = soup.find_all('td', attrs={"data-stat": "home_pts", "class": "right"})
                notes = soup.find_all('td', attrs={"data-stat": "game_remarks"})

                #get the data from each day
                for i in range(len(game_days)):

                    months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 
                            'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

                    team_abbrs = {'Atlanta Hawks': 'ATL', 'Brooklyn Nets': 'BKN', 'Boston Celtics': 'BOS', 'Charlotte Hornets': 'CHA', 'Chicago Bulls': 'CHI', 'Cleveland Cavaliers': 'CLE', 'Dallas Mavericks': 'DAL',
                                  'Denver Nuggets': 'DEN', 'Detroit Pistons': 'DET', 'Golden State Warriors': 'GS', 'Houston Rockets': 'HOU', 'Indiana Pacers': 'IND', 'Los Angeles Clippers': 'LAC', 'Los Angeles Lakers': 'LAL',
                                  'Memphis Grizzlies': 'MEM', 'Miami Heat': 'MIA', 'Milwaukee Bucks': 'MIL', 'Minnesota Timberwolves': 'MIN', 'New Orleans Pelicans': 'NO', 'New York Knicks': 'NY', 'Oklahoma City Thunder': 'OKC',
                                  'Orlando Magic': 'ORL', 'Philadelphia 76ers': 'PHI', 'Phoenix Suns': 'PHO', 'Portland Trail Blazers': 'POR', 'San Antonio Spurs': 'SA', 'Sacramento Kings': 'SAC', 'Toronto Raptors': 'TOR',
                                  'Utah Jazz': 'UTA', 'Washington Wizards' : 'WAS', 'New Orleans Hornets' : 'NOH', 'Charlotte Bobcats' : 'CHA', 'New Jersey Nets': 'NJN', 'Seattle SuperSonics': 'SEA', 'Vancouver Grizzlies': 'VAN',
                                  'New Orleans/Oklahoma City Hornets': 'NOK', 'Washington Bullets': 'WSB', 'Kansas City Kings': 'KCK', 'San Diego Clippers': 'SDC', 'Buffalo Braves': 'BUF', 'New Orleans Jazz': 'NOJ',
                                  'Kansas City-Omaha Kings': 'KCO', 'Capital Bullets': 'CAP', 'Cincinnati Royals': 'CIN', 'San Diego Rockets': 'SDR', 'San Francisco Warriors': 'SFW', 'St. Louis Hawks': 'STL', 'Syracuse Nationals': 'SYR',
                                  'Chicago Zephyrs': 'CHZ', 'Chicago Packers': 'CHP', 'Philadelphia Warriors': 'PHW', 'Minneapolis Lakers': 'MNL', 'Fort Wayne Pistons': 'FTW', 'Rochester Royals': 'ROC',
                                  'Indianapolis Olympians': 'INO', 'Milwaukee Hawks': 'MLH', 'Tri-Cities Blackhawks': 'TRI', 'Washington Capitols': 'WSC', 'St. Louis Bombers': 'STB', 'Chicago Stags': 'CHS',
                                  'Anderson Packers': 'AND', 'Sheboygan Red Skins': 'SHE', 'Waterloo Hawks': 'WAT', 'Baltimore Bullets': 'BAL', 'New York Nets': 'NYN'}

                    #format the data
                    datee = str(game_days[i].text.strip())
                    _, month_day, year = datee.split(',')
                    month, day = (month_day.strip()).split(' ')
                    
                    if int(day) > 0 and int(day)<10:
                        day = '0' + day

                    date_formated = year.strip() + '-' + months[month] + '-' + day
                    date_formated_url = year.strip() + months[month] + day
                    game_date = date(int(year.strip()), int(months[month]), int(day))

                    v_pts = visitor_pts[i].text.strip()
                    h_pts = home_pts[i].text.strip()

                    #check if the has already occurred and has the results
                    if v_pts != '':

                        #v_pts = visitor points
                        #h_pts = home points
                        v_pts = int(v_pts)
                        h_pts = int(h_pts)

                        if v_pts > h_pts:
                            data.loc[index, 'teamRslt'] = 'Win'
                            data.loc[index, 'opptRslt'] = 'Loss'
                        else:
                            data.loc[index, 'teamRslt'] = 'Loss'
                            data.loc[index, 'opptRslt'] = 'Win'

                        #check if the teams day off is empty
                        if teams_day_off[team_abbrs[visitor_team_names[i].text.strip()]] == '':
                            first_date = date(int(year.strip()), int(months[month]), int(day))
                            teams_day_off[team_abbrs[visitor_team_names[i].text.strip()]] = first_date
                        else:
                            #if is not empty, calculate the difference between the last game day
                            #and the current date
                            last_date = teams_day_off[team_abbrs[visitor_team_names[i].text.strip()]]
                            current_date = date(int(year.strip()), int(months[month]), int(day))

                            days_off = current_date - last_date
                            data.loc[index, 'teamDayOff'] = int(days_off.days) - 1

                            #replace the last game date for the current date
                            teams_day_off[team_abbrs[visitor_team_names[i].text.strip()]] = current_date
                        
                        #do the same for the home team
                        if teams_day_off[team_abbrs[home_team_names[i].text.strip()]] == '':
                            first_date = date(int(year.strip()), int(months[month]), int(day))
                            teams_day_off[team_abbrs[home_team_names[i].text.strip()]] = first_date
                        else:
                            last_date = teams_day_off[team_abbrs[home_team_names[i].text.strip()]]
                            current_date = date(int(year.strip()), int(months[month]), int(day))

                            days_off = current_date - last_date
                            data.loc[index, 'opptDayOff'] = int(days_off.days) - 1
                            teams_day_off[team_abbrs[home_team_names[i].text.strip()]] = current_date

                        #correcting some teams abbreviation for the visitor team
                        if team_abbrs[visitor_team_names[i].text.strip()] == 'NO':
                            team_abbrs[visitor_team_names[i].text.strip()] = 'NOP'
                        elif team_abbrs[visitor_team_names[i].text.strip()] == 'SA':
                            team_abbrs[visitor_team_names[i].text.strip()] = 'SAS'
                        elif team_abbrs[visitor_team_names[i].text.strip()] == 'NY':
                            team_abbrs[visitor_team_names[i].text.strip()] = 'NYK'
                        elif team_abbrs[visitor_team_names[i].text.strip()] == 'GS':
                            team_abbrs[visitor_team_names[i].text.strip()] = 'GSW'
                        elif team_abbrs[visitor_team_names[i].text.strip()] == 'BKN':
                            team_abbrs[visitor_team_names[i].text.strip()] = 'BRK'

                        if team_abbrs[visitor_team_names[i].text.strip()] == 'CHA' and first_season_year >= 2015:
                            team_abbrs[visitor_team_names[i].text.strip()] = 'CHO'
                        elif team_abbrs[visitor_team_names[i].text.strip()] == 'CHA' and first_season_year <= 2002:
                            team_abbrs[visitor_team_names[i].text.strip()] = 'CHH'

                        #correcting some teams abbreviation for the home team
                        if team_abbrs[home_team_names[i].text.strip()] == 'NO':
                            team_abbrs[home_team_names[i].text.strip()] = 'NOP'
                        elif team_abbrs[home_team_names[i].text.strip()] == 'SA':
                            team_abbrs[home_team_names[i].text.strip()] = 'SAS'
                        elif team_abbrs[home_team_names[i].text.strip()] == 'NY':
                            team_abbrs[home_team_names[i].text.strip()] = 'NYK'
                        elif team_abbrs[home_team_names[i].text.strip()] == 'GS':
                            team_abbrs[home_team_names[i].text.strip()] = 'GSW'
                        elif team_abbrs[home_team_names[i].text.strip()] == 'BKN':
                            team_abbrs[home_team_names[i].text.strip()] = 'BRK'

                        if team_abbrs[home_team_names[i].text.strip()] == 'CHA' and first_season_year >= 2015:
                            team_abbrs[home_team_names[i].text.strip()] = 'CHO'
                        elif team_abbrs[home_team_names[i].text.strip()] == 'CHA' and first_season_year <= 2002:
                            team_abbrs[home_team_names[i].text.strip()] = 'CHH'
                        
                        if first_season_year <= 1978:
                            team_abbrs['Denver Nuggets'] = 'DNN'
                        else:
                            team_abbrs['Denver Nuggets'] = 'DEN'

                        if first_season_year <= 1963:
                            team_abbrs['Baltimore Bullets'] = 'BLB'
                        else:
                            team_abbrs['Baltimore Bullets'] = 'BAL'

                        id_away_table = 'box-'+team_abbrs[visitor_team_names[i].text.strip()]+'-game-'
                        id_home_table = 'box-'+team_abbrs[home_team_names[i].text.strip()]+'-game-'

                        team_abbrs_tables = [id_away_table, id_home_table]

                        url_boxscore = 'https://www.basketball-reference.com/boxscores/' + date_formated_url + '0' + team_abbrs[home_team_names[i].text.strip()] + '.html'
            
                        req = requests.get(url_boxscore)
                        soup = BeautifulSoup(re.sub("<!--|-->","", req.text), 'html.parser')
                        away = True

                        #get the data from both teams
                        for team_tables in team_abbrs_tables:

                            tspct = 0.0
                            trbpct = 0.0
                            efgpct = 0.0
                            orbpct = 0.0
                            drbpct = 0.0
                            astpct = 0.0
                            stlpct = 0.0
                            tovpct = 0.0
                            offrtg = 0.0
                            defrtg = 0.0
                            blkpct = 0.0
                            wins = 0
                            losses = 0
                            four_factor = [0.0, 0.0]

                            team = team_tables + 'basic'

                            #treating some exceptions
                            if first_season_year >= 1951:
                                current_score = soup.find('div', attrs={"id": "all_" + team})

                                if current_score:
                                    current_score = current_score.find('div', attrs={"class": "section_heading"})
                                    current_score = (current_score.find('h2')).get_text()

                                    try:
                                        wins, losses = re.findall(r'\b\d+\b', current_score)
                                    except ValueError:
                                        wins, losses = '', ''
                        
                            table = soup.find('table', attrs={"id": team})

                            if table:
                                tfoot = table.find('tfoot')
                                fg = self.checkNumber((tfoot.find('td', attrs={"data-stat": "fg", "class": "right"})))
                                minn = self.checkNumber((tfoot.find('td', attrs={"data-stat": "mp", "class": "right"})))
                                fg = self.checkNumber((tfoot.find('td', attrs={"data-stat": "fg", "class": "right"})))
                                fga = self.checkNumber((tfoot.find('td', attrs={"data-stat": "fga", "class": "right"})))
                                fg3 = self.checkNumber((tfoot.find('td', attrs={"data-stat": "fg3", "class": "right"})))
                                fg3a = self.checkNumber((tfoot.find('td', attrs={"data-stat": "fg3a", "class": "right"})))
                                ft = self.checkNumber((tfoot.find('td', attrs={"data-stat": "ft", "class": "right"})))
                                fta = self.checkNumber((tfoot.find('td', attrs={"data-stat": "fta", "class": "right"})))
                                orb = self.checkNumber((tfoot.find('td', attrs={"data-stat": "orb", "class": "right"})))
                                drb = self.checkNumber((tfoot.find('td', attrs={"data-stat": "drb", "class": "right"})))
                                trb = self.checkNumber((tfoot.find('td', attrs={"data-stat": "trb", "class": "right"})))
                                ast = self.checkNumber((tfoot.find('td', attrs={"data-stat": "ast", "class": "right"})))
                                stl = self.checkNumber((tfoot.find('td', attrs={"data-stat": "stl", "class": "right"})))
                                blk = self.checkNumber((tfoot.find('td', attrs={"data-stat": "blk", "class": "right"})))
                                tov = self.checkNumber((tfoot.find('td', attrs={"data-stat": "tov", "class": "right"})))
                                pf = self.checkNumber((tfoot.find('td', attrs={"data-stat": "pf", "class": "right"})))
                            else:
                                fg = 0.0
                                minn = 0.0
                                fg = 0.0
                                fga = 0.0
                                fg3 = 0.0
                                fg3a = 0.0
                                ft = 0.0
                                fta = 0.0
                                orb = 0.0
                                drb = 0.0
                                trb = 0.0
                                ast = 0.0
                                stl = 0.0
                                blk = 0.0
                                tov = 0.0
                                pf = 0.0

                            #treating other exception
                            if first_season_year >= 1984:
                                team = team_tables + 'advanced'                        
                                table = soup.find('table', attrs={"id": team})

                                if table:
                                    tfoot = table.find('tfoot')
                                    tspct = self.checkNumber((tfoot.find('td', attrs={"data-stat": "ts_pct", "class": "right"})))
                                    trbpct = self.checkNumber((tfoot.find('td', attrs={"data-stat": "trb_pct", "class": "right"})))
                                    efgpct = self.checkNumber((tfoot.find('td', attrs={"data-stat": "efg_pct", "class": "right"})))
                                    orbpct = self.checkNumber((tfoot.find('td', attrs={"data-stat": "orb_pct", "class": "right"})))
                                    drbpct = self.checkNumber((tfoot.find('td', attrs={"data-stat": "drb_pct", "class": "right"})))
                                    astpct = self.checkNumber((tfoot.find('td', attrs={"data-stat": "ast_pct", "class": "right"})))
                                    stlpct = self.checkNumber((tfoot.find('td', attrs={"data-stat": "stl_pct", "class": "right"})))
                                    tovpct = self.checkNumber((tfoot.find('td', attrs={"data-stat": "tov_pct", "class": "right"})))
                                    offrtg = self.checkNumber((tfoot.find('td', attrs={"data-stat": "off_rtg", "class": "right"})))
                                    defrtg = self.checkNumber((tfoot.find('td', attrs={"data-stat": "def_rtg", "class": "right"})))
                                    blkpct = self.checkNumber((tfoot.find('td', attrs={"data-stat": "blk_pct", "class": "right"})))

                            #treating other exception
                            if first_season_year >= 1951:
                                quarter_points = soup.find('table', attrs={"id": "line_score"})

                                if quarter_points:
                                    qt_points_tr = quarter_points.find_all('tr', attrs={"class": ''})

                            #treating other exception
                            if first_season_year >= 1981:
                                four_factors = soup.find('table', attrs={"id": "four_factors"})

                                if four_factors:
                                    four_factor = four_factors.find_all('td', attrs={"class": "right", "data-stat": "pace"})

                            #fill the data in the columns
                            if away:
                                data.loc[index, 'teamWins'] = wins
                                data.loc[index, 'teamLosses'] = losses
                                data.loc[index, 'teamMin'] = minn
                                data.loc[index, 'teamAST'] = ast
                                data.loc[index, 'teamTO'] = tov
                                data.loc[index, 'teamSTL'] = stl
                                data.loc[index, 'teamBLK'] = blk
                                data.loc[index, 'teamPF'] = pf
                                data.loc[index, 'teamFGA'] = fga
                                data.loc[index, 'teamFGM'] = fg
                                if fga == 0:
                                    data.loc[index, 'teamFG%'] = 0.0
                                else:
                                    data.loc[index, 'teamFG%'] = "%0.2f" % (float(fg/fga))
                                data.loc[index, 'team2PA'] = fga - fg3a
                                data.loc[index, 'team2PM'] = fg - fg3
                                if fga == 0 and fg3a ==0:
                                    data.loc[index, 'team2P%'] = 0.0
                                else:
                                    data.loc[index, 'team2P%'] = "%0.2f" % ((fg - fg3)/(fga - fg3a))
                                data.loc[index, 'team3PA'] = fg3a
                                data.loc[index, 'team3PM'] = fg3
                                if fg3a == 0:
                                    data.loc[index, 'team3P%'] = 0.0
                                else:
                                    data.loc[index, 'team3P%'] = "%0.2f" % (float(fg3/fg3a))
                                data.loc[index, 'teamFTA'] = fta
                                data.loc[index, 'teamFTM'] = ft
                                if fta == 0:
                                    data.loc[index, 'teamFT%'] = 0.0
                                else:
                                    data.loc[index, 'teamFT%'] = "%0.2f" % float(ft/fta)
                                data.loc[index, 'teamORB'] = orb
                                data.loc[index, 'teamDRB'] = drb
                                data.loc[index, 'teamTRB'] = trb
                                data.loc[index, 'teamTS%'] = tspct
                                data.loc[index, 'teamEFG%'] = efgpct
                                data.loc[index, 'teamOREB%'] = orbpct
                                data.loc[index, 'teamDREB%'] = drbpct
                                data.loc[index, 'teamTO%'] = tovpct
                                data.loc[index, 'teamSTL%'] = stlpct
                                data.loc[index, 'teamBLK%'] = blkpct
                                if fg3 == 0 and fg3a == 0:
                                    data.loc[index, 'teamBLKR'] = 0.0
                                else:
                                    try:
                                        data.loc[index, 'teamBLKR'] = "%0.2f" % ((blk * 100)/(fga - fg3a))
                                    except ZeroDivisionError:
                                        data.loc[index, 'teamBLKR'] = 0.0
                                data.loc[index, 'teamDrtg'] = defrtg
                                data.loc[index, 'teamOrtg'] = offrtg
                                if fga == 0:
                                    data.loc[index, 'teamPPS'] = 0.0
                                else:
                                    data.loc[index, 'teamPPS'] = "%0.2f" % (v_pts/fga)
                                data.loc[index, 'teamFIC'] = "%0.2f" % (v_pts + orb + 0.75 * drb + ast + stl + blk - 0.75 * fga - 0.375 * fta - tov - 0.5 * pf)
                                if minn == 0:
                                    data.loc[index, 'teamFIC40'] = 0.0
                                else:
                                    data.loc[index, 'teamFIC40'] = "%0.2f" % (((v_pts + orb + 0.75 * drb + ast + stl + blk - 0.75 * fga - 0.375 * fta - tov - 0.5 * pf) * 40 * 5)/minn)
                                data.loc[index, 'teamEDiff'] = "%0.2f" % (offrtg - defrtg)
                                if fga == 0 and fta == 0 and ast == 0 and tov == 0:
                                    data.loc[index, 'teamAR'] = 0.0
                                else:
                                    data.loc[index, 'teamAR'] = "%0.2f" % ((ast * 100) / (fga - 0.44 * fta + ast + tov))
                                if tov == 0:
                                    data.loc[index, 'teamAST/TO'] = 0.0
                                    data.loc[index, 'teamSTL/TO'] = 0.0
                                else:
                                    data.loc[index, 'teamAST/TO'] = "%0.2f" % (ast/tov)
                                    data.loc[index, 'teamSTL/TO'] = "%0.2f" % (stl/tov)
                                if fga == 0 and orb == 0 and tov == 0:
                                    data.loc[index, 'teamPlay%'] = 0.0
                                else:
                                    data.loc[index, 'teamPlay%'] = "%0.2f" % (fg / (fga - orb + tov))
                                data.loc[index, 'teamASST%'] = "%0.2f" % astpct
                                data.loc[index, 'teamTREB%'] = trbpct
                                data.loc[index, 'teamPace'] = self.checkNumber(four_factor[0])
                                data.loc[index, 'teamPoss'] = (self.checkNumber(four_factor[0]) * minn)/(48 * 5)

                                #treating other exception
                                if first_season_year >= 1951 and quarter_points:
                                    
                                    tds = qt_points_tr[1].find_all('td', attrs={"class": "center"})

                                    for s in range(len(tds)-1):
                                        quarter = 'teamPTS' + str(s+1)
                                        data.loc[index, quarter] = self.checkNumber(tds[s])

                                away = False

                            else:
                                data.loc[index, 'opptWins'] = wins
                                data.loc[index, 'opptLosses'] = losses
                                data.loc[index, 'opptMin'] = minn
                                data.loc[index, 'opptAST'] = ast
                                data.loc[index, 'opptTO'] = tov
                                data.loc[index, 'opptSTL'] = stl
                                data.loc[index, 'opptBLK'] = blk
                                data.loc[index, 'opptPF'] = pf
                                data.loc[index, 'opptFGA'] = fga
                                data.loc[index, 'opptFGM'] = fg
                                if fga == 0:
                                    data.loc[index, 'opptFG%'] = 0.0
                                else:
                                    data.loc[index, 'opptFG%'] = "%0.2f" % (float(fg/fga))
                                data.loc[index, 'oppt2PA'] = fga - fg3a
                                data.loc[index, 'oppt2PM'] = fg - fg3
                                if fga ==0 and fg3a == 0:
                                    data.loc[index, 'oppt2P%'] = 0.0
                                else:
                                    data.loc[index, 'oppt2P%'] = "%0.2f" % ((fg - fg3)/(fga - fg3a))
                                data.loc[index, 'oppt3PA'] = fg3a
                                data.loc[index, 'oppt3PM'] = fg3
                                if fg3a == 0:
                                    data.loc[index, 'oppt3P%'] = 0.0
                                else:
                                    data.loc[index, 'oppt3P%'] = "%0.2f" % (float(fg3/fg3a))
                                data.loc[index, 'opptFTA'] = fta
                                data.loc[index, 'opptFTM'] = ft
                                if fta == 0:
                                    data.loc[index, 'opptFT%'] = 0.0
                                else:
                                    data.loc[index, 'opptFT%'] = "%0.2f" % (float(ft/fta))
                                data.loc[index, 'opptORB'] = orb
                                data.loc[index, 'opptDRB'] = drb
                                data.loc[index, 'opptTRB'] = trb
                                data.loc[index, 'opptTS%'] = tspct
                                data.loc[index, 'opptEFG%'] = efgpct
                                data.loc[index, 'opptOREB%'] = orbpct
                                data.loc[index, 'opptDREB%'] = drbpct
                                data.loc[index, 'opptTO%'] = tovpct
                                data.loc[index, 'opptSTL%'] = stlpct
                                data.loc[index, 'opptBLK%'] = blkpct
                                try:
                                    data.loc[index, 'opptBLKR'] = "%0.2f" % ((blk * 100)/(fga - fg3a))
                                except ZeroDivisionError:
                                    data.loc[index, 'opptBLKR'] = 0.0
                                data.loc[index, 'opptDrtg'] = defrtg
                                data.loc[index, 'opptOrtg'] = offrtg
                                if fga == 0:
                                    data.loc[index, 'opptPPS'] = 0.0
                                else:
                                    data.loc[index, 'opptPPS'] = "%0.2f" % (h_pts/fga)
                                data.loc[index, 'opptFIC'] = "%0.2f" % (h_pts + orb + 0.75 * drb + ast + stl + blk - 0.75 * fga - 0.375 * fta - tov - 0.5 * pf)
                                if minn == 0:
                                    data.loc[index, 'opptFIC40'] = 0.0
                                else:
                                    data.loc[index, 'opptFIC40'] = "%0.2f" % (((h_pts + orb + 0.75 * drb + ast + stl + blk - 0.75 * fga - 0.375 * fta - tov - 0.5 * pf) * 40 * 5)/minn)
                                data.loc[index, 'opptEDiff'] = "%0.2f" % (offrtg - defrtg)
                                if fta == 0 and ast == 0 and tov == 0 and fga == 0:
                                    data.loc[index, 'opptAR'] = 0.0
                                else:
                                    data.loc[index, 'opptAR'] = "%0.2f" % ((ast * 100) / (fga - 0.44 * fta + ast + tov))
                                if tov == 0:
                                    data.loc[index, 'opptAST/TO'] = 0.0
                                    data.loc[index, 'opptSTL/TO'] = 0.0
                                else:
                                    data.loc[index, 'opptAST/TO'] = "%0.2f" % (ast/tov)
                                    data.loc[index, 'opptSTL/TO'] = "%0.2f" % (stl/tov)
                                if fga == 0 and orb == 0 and tov == 0:
                                    data.loc[index, 'opptPlay%'] = 0.0
                                else:
                                    data.loc[index, 'opptPlay%'] = "%0.2f" % (fg / (fga - orb + tov))
                                data.loc[index, 'opptASST%'] = "%0.2f" % astpct
                                data.loc[index, 'opptTREB%'] = trbpct
                                data.loc[index, 'opptPace'] = self.checkNumber(four_factor[1])
                                data.loc[index, 'opptPoss'] = (self.checkNumber(four_factor[1]) * minn)/(48 * 5)

                                #treating other exception
                                if first_season_year >= 1951 and quarter_points:

                                    tds = qt_points_tr[2].find_all('td', attrs={"class": "center"})

                                    for s in range(len(tds)-1):
                                        quarter = 'opptPTS' + str(s+1)
                                        data.loc[index, quarter] = self.checkNumber(tds[s])
                        
                        data.loc[index, 'gmDate'] = date_formated
                        data.loc[index, 'season'] = season
                        data.loc[index, 'teamAbbr'] = team_abbrs[visitor_team_names[i].text.strip()]
                        data.loc[index, 'teamLoc'] = 'Away'
                        data.loc[index, 'teamPTS'] = v_pts
                        data.loc[index, 'opptAbbr'] = team_abbrs[home_team_names[i].text.strip()]
                        data.loc[index, 'opptLoc'] = 'Home'
                        data.loc[index, 'opptPTS'] = h_pts

                        #check if the game is from regular season, play-in or playoffs
                        if notes[i].text.strip() != '':
                            data.loc[index, 'seasonType'] = 'Play-In'
                        else:
                            if game_date < playoff_first_game_date:
                                data.loc[index, 'seasonType'] = 'Regular'
                            else:
                                data.loc[index, 'seasonType'] = 'Playoffs'

                        if v_pts > h_pts:
                            data.loc[index, 'matchWinner'] = team_abbrs[visitor_team_names[i].text.strip()]
                        else:
                            data.loc[index, 'matchWinner'] = team_abbrs[home_team_names[i].text.strip()]

                        index += 1
                        time.sleep(1.3)
                        bar.update(index+1)
            
                #fill the missing values with zero
                data.fillna(0.0, inplace = True)

            #print("The data was collected in " + str((time.time() - start_time)/60) + " minutes!")
            print("\nSaving the data from the " + season + " season!\n")
            data.to_csv(season + "_officialBoxScore.csv", index=False)

    #will check if the param passed isn't null
    def checkNumber(self, number):
        
        if number and number.text.strip() != '':
            number_float = float(number.text.strip())
            return number_float
        else:
            return 0.0

if __name__ == "__main__":
  
    boxscore_scrap = NbaBoxScoreScrapper('NBA_BoxScore/data/')
    boxscore_scrap.GetDatas(first_season = '2020-21')
