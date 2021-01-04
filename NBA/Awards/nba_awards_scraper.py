import requests
from bs4 import BeautifulSoup
import pandas as pd

class NbaAwards:
    
    def __init__(self):
        self.url = 'http://www.espn.com/nba/history/awards/'
        pass

    def getAllAwards(self, season):
        
        seasons = []
        mvp = []
        dpoy = []
        roty = []
        smoty = []
        mip = []
        coty = []
        finals_mvp = []
        all_nba_team1 = []
        all_nba_team2 = []
        all_nba_team3 = []
        all_rookie_team1 = []
        all_rookie_team2 = []
        all_defensive_team1 = []
        all_defensive_team2 = []
        all_star_mvp = []
        twyman_stokes_award = []
        initial_season = season 

        while season <= 2019:

            all_nba_team1_str = []
            all_nba_team2_str = []
            all_nba_team3_str = []
            all_rookie_team1_str = []
            all_rookie_team2_str = []
            all_defensive_team1_str = []
            all_defensive_team2_str = []

            seasons.append(season)

            self.url = 'http://www.espn.com/nba/history/awards/_/year/' + str(season)

            request = requests.get(self.url)
            soup = BeautifulSoup(request.text, 'html.parser')
            awards_table = soup.find('table', attrs = {'class' : 'tablehead'})
            awards_table_rows = awards_table.find_all('tr')[2]
            datas = awards_table_rows.find_all('td')
            
            for i in range(1, 131, 3):

                if i==1:
                    mvp.append(datas[i].text)
                elif i==4 and season >= 1983:
                    dpoy.append(datas[4].text)
                elif i==7:
                    roty.append(datas[7].text)
                elif i==10 and season >= 1983:
                    smoty.append(datas[10].text)
                elif i==13 and season >= 1986:
                    mip.append(datas[13].text)
                elif i==16 and season >= 1963:
                    coty.append(datas[16].text)
                elif i==19 and season >= 1969:
                    finals_mvp.append(datas[19].text)
                elif i==127:
                    all_star_mvp.append(datas[127].text)
                    
                elif i==130 and season >= 2013:
                    twyman_stokes_award.append(datas[130].text)
                    
                if i>=22 and i<=34:
                    all_nba_team1_str.append(datas[i].text)
                
                if i>=37 and i<=49:
                    all_nba_team2_str.append(datas[i].text)
                
                if i>=52 and i<=64 and season >= 1989:
                    all_nba_team3_str.append(datas[i].text)
                
                if i>=67 and i<=79:
                    all_rookie_team1_str.append(datas[i].text)
                
                if i>=82 and i<=94 and season >= 1989:
                    all_rookie_team2_str.append(datas[i].text)

                if i>=97 and i<=109 and season >= 1969:
                    all_defensive_team1_str.append(datas[i].text)

                if i>=112 and i<=124 and season >= 1969:
                    all_defensive_team2_str.append(datas[i].text)
            
            all_nba_team1.append(str(all_nba_team1_str))
            all_nba_team2.append(str(all_nba_team2_str))
            all_nba_team3.append(str(all_nba_team3_str))
            all_rookie_team1.append(str(all_rookie_team1_str))
            all_rookie_team2.append(str(all_rookie_team2_str))
            all_defensive_team1.append(str(all_defensive_team1_str))
            all_defensive_team2.append(str(all_defensive_team2_str))

            print("The awards for the " +str(season)+ " season has been collected!")
            season += 1
        
        dataframe = {'Season': seasons, 'MVP': mvp, 'Defensive Player of the Year': dpoy, 'Rookie of the Year': roty,
                    'Sixth Man of the Year': smoty, 'Most Improved Player': mip, 'Coach of the Year': coty,
                    'Finals MVP': finals_mvp, 'All-NBA 1st Team': all_nba_team1, 'All-NBA 2nd Team': all_nba_team2,
                    'All-NBA 3rd Team': all_nba_team3, 'All-Rookie 1st Team': all_rookie_team1, 'All-Rookie 2nd Team': all_rookie_team2,
                    'All-Defensive 1st Team': all_defensive_team1, 'All-Defensive 2nd Team': all_defensive_team2,
                    'All-Star MVP': all_star_mvp, 'Twyman-Stokes Teammate of the Year Award': twyman_stokes_award}

        data_csv = pd.DataFrame(data = dataframe)
        csv_name = 'NBA_Season_' +str(initial_season)+ '-2019_Awards.csv'
        data_csv.to_csv(csv_name, index = False)

if __name__ == "__main__":
    
    awards = NbaAwards()
    awards.getAllAwards(2000)