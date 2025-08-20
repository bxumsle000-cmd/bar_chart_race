import sqlite3
import pandas as pd


class CreateBarChartRaceData:
    def adjust_datetime_format(self,x:str):
        date_part,time_part= x.split()
        date_part="2024-01-13"
        iso_8601_format= f"{date_part} {time_part}"
        return iso_8601_format
    
    def create_cumulative_votes_by_time_candiate(self):
        connection= sqlite3.connect("data/create_taiwan_presidential_election_2024.db")
        sql_query="""
                    SELECT polling_place.county,
                        polling_place.polling_place,
                        candidate.candidate,
                        SUM(votes.votes) AS votes
                    FROM votes
                    JOIN polling_place
                    ON votes.polling_place_id=polling_place.id
                    JOIN candidate
                    ON votes.candidate_id= candidate.id       
                    GROUP BY polling_place.county,
                            polling_place.id,
                            candidate.candidate
        """
        votes_by_county_polling_place_candidate= pd.read_sql(sql_query,con=connection)
        connection.close()

        votes_collected= pd.read_excel("data/113全國投開票所完成時間.xlsx",skiprows=[0,1,2])
        votes_collected.columns= ["county","town","polling_place","collected_in","numbe_of_voter"]
        votes_collected= votes_collected[["county","polling_place","collected_in"]]

        merge= pd.merge(votes_by_county_polling_place_candidate,votes_collected,left_on=["county","polling_place"],right_on=["county","polling_place"],how="left")
        votes_by_collected_candidate= merge.groupby(["collected_in","candidate"])["votes"].sum().reset_index()
        cum_sum= votes_by_collected_candidate.groupby("candidate")["votes"].cumsum()
        votes_by_collected_candidate["cumsum_votes"]= cum_sum   

        votes_by_collected_candidate["collected_in"]= votes_by_collected_candidate["collected_in"].map(self.adjust_datetime_format)
        votes_by_collected_candidate["collected_in"]= pd.to_datetime(votes_by_collected_candidate["collected_in"])
        return votes_by_collected_candidate

    def create_nlargest_covid19_confirmed(self):
        connection= sqlite3.connect("data/covid_19_pandemic.db")
        sql_query="""
        SELECT  country,
                reported_on,
                confirmed
        FROM time_series
        WHERE reported_on <= "2020-12-31" ;
        """
        covid19_confirmed= pd.read_sql(sql_query,con=connection)

        covid19_confirmed.groupby("reported_on")["confirmed"].nlargest(10)
        nlargest_index= covid19_confirmed.groupby("reported_on")["confirmed"].nlargest(10).reset_index()["level_1"].values
        nlargest_covid19_confirmed= covid19_confirmed.loc[nlargest_index,:].reset_index(drop=True)
        return nlargest_covid19_confirmed

create_bar_chart_race_data= CreateBarChartRaceData()
cumulative_votes_by_time_candiate= create_bar_chart_race_data.create_cumulative_votes_by_time_candiate()
nlargest_covid19_confirmed= create_bar_chart_race_data.create_nlargest_covid19_confirmed()


