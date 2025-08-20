from create_bar_chart_race_data import CreateBarChartRaceData
import plotly.express as px
import pandas as pd
from raceplotly.plots import barplot

create_bar_chart_race_data= CreateBarChartRaceData()
cumulative_votes_by_time_candiate= create_bar_chart_race_data.create_cumulative_votes_by_time_candiate()
nlargest_covid19_confirmed= create_bar_chart_race_data.create_nlargest_covid19_confirmed()

early_collected = cumulative_votes_by_time_candiate[cumulative_votes_by_time_candiate["collected_in"] < pd.to_datetime("2024-01-13 17:30:00")]
max_votes= early_collected["cumsum_votes"].max()
# fig=px.bar(early_collected,x="cumsum_votes",y="candidate",color="candidate",
#            animation_frame="collected_in",animation_group="candidate",range_x=[0,max_votes])
# fig.update_yaxes(categoryorder="total ascending")
# fig.show()
# ==============================================================================================================='

max_confirmed= nlargest_covid19_confirmed["confirmed"].max()
# fig= px.bar(nlargest_covid19_confirmed,x="confirmed",y="country",color="country",animation_frame="reported_on",animation_group="country",range_x=[0,max_confirmed])
# fig.update_yaxes(categoryorder="total ascending")
# fig.show()

votes_raceplot= barplot(early_collected,item_column="candidate",value_column="cumsum_votes",time_column="collected_in",top_entries=3)
fig= votes_raceplot.plot(item_label="Votes_collected by candidate",value_label="Number of votes",frame_duration=75)
fig.write_html("bar_chart_race_votes.html")

confirmed_raceplot= barplot(nlargest_covid19_confirmed,item_column="country",value_column="confirmed",time_column="reported_on",top_entries=10)
fig= confirmed_raceplot.plot(item_label="Country",value_label="Number of confirmed",frame_duration=60)
fig.write_html("bar_chart_race_covid19_confirmed.html")