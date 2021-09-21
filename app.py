from flask import Flask, render_template
app = Flask(__name__)
import pandas as pd
import time


url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url2 = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
url3 = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"


df = pd.read_csv(url, index_col=0)
df2 = pd.read_csv(url2, index_col=0)

df3 = pd.read_csv(url3, index_col=0)
values = df.iloc[[206]].values.tolist()[0][3:]
death = df2.iloc[[206]].values.tolist()[0][3:]
recovered = df3.iloc[[204]].values.tolist()[0][3:]

dates = list(df.columns)[3:]
new_dates = []
for x in dates:
    string = []
    for i in x.split("/"):
        string.append(int(i))

    new_dates.append(string)



values_flipped = values[::-1]
marginal_values = []
for one in range(len(values_flipped)):
    new_val = values_flipped[one -1 ] - values_flipped[one]
    marginal_values.append(new_val)
marginal_values.append(0)
marginal_values = marginal_values[1:][::-1]

death_flipped = death[::-1]
marginal_death = []
for one in range(len(death_flipped)):
    new_val = death_flipped[one -1 ] - death_flipped[one]
    marginal_death.append(new_val)
marginal_death.append(0)
marginal_death = marginal_death[1:][::-1]

recovered_flipped = recovered[::-1]
marginal_rec = []
for one in range(len(recovered_flipped)):
    new_val = recovered_flipped[one -1 ] - recovered_flipped[one]
    marginal_rec.append(new_val)
marginal_rec.append(0)
marginal_rec = marginal_rec[1:][::-1]

"""
More_data page
"""






all_infected = df.iloc[[206]].values.tolist()[0][3:][-1]
all_death = df2.iloc[[206]].values.tolist()[0][3:][-1]
all_recovered = df3.iloc[[204]].values.tolist()[0][3:][-1]

percentage = round((all_death/all_infected)*100,2)
percentage_rec = round((all_recovered/all_infected)*100,2)

data = [all_infected,all_death,all_recovered] #can pass all recovered and than fix the chart in more_data with these values ;)







@app.route('/')
def index():
    return render_template('index.html',values=values, dates=new_dates, date=new_dates[-1], marginal=marginal_values, death=death, marginal_death=marginal_death, recovered=recovered, marginal_rec=marginal_rec)

@app.route('/more_data')
def more():
    return render_template('more_data.html', data=data,date=new_dates[-1], percentage=percentage, percentage_rec=percentage_rec)


@app.route('/facts_sources')
def facts():
    return render_template('facts_sources.html')

if __name__ == '__main__':
    app.run(debug=False)

