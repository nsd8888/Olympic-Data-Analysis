from django.shortcuts import render,HttpResponseRedirect,HttpResponse
import json
from .forms import year_country,Overanalysis,year_form
# Create your views here.
import numpy as np
import pandas as pd
from .graphs import get_graph


def files():
    df = pd.read_csv('files/athlete_events.csv')
    return df
def dataframe():
    df = pd.read_csv('files/athlete_events.csv')
    df_region = pd.read_csv('files/noc_regions.csv')
    df.drop_duplicates(inplace=True)
    df = df.merge(df_region, on='NOC', how='left')
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df

def country_year_list(df):
    years = list(np.unique(df['Year'].dropna().values))
    years.sort(reverse=True)


    country= list(np.unique(df['region'].dropna().values))
    return years,country

def home(request):
    return render(request, 'enroll/home.html')

def all_list(request):
   a=dataframe()
   medal_tally = a.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

   if request.method=='POST':
       form=year_country(request.POST)
       print('you are in post')

       if form.is_valid():
           x=form.cleaned_data['Year']
           y=form.cleaned_data['Country']
           var=0
           ##################################################
           if x=='All' and y=='All':
               medal_tally=medal_tally
               statement="Overall Olymic Tally- since 1896"

           elif x!='All' and y=='All':
               print(var)
               print('i am in year and all country')
               medal_tally = medal_tally[medal_tally['Year'] == int(x)]
               statement = 'Medal Tally in {} Olymics'.format(int(x))


           elif x=='All' and y!='All':
               var=1
               medal_tally = medal_tally[medal_tally['region'] == str(y)]
               statement='Overall performance of {} in Olymics'.format(y)

           else:
               var=2
               medal_tally = medal_tally[(medal_tally['Year'] == int(x)) & (medal_tally['region'] == str(y))]
               statement="Performance of {} in {} Olympics".format(y,int(x))
           ###########################################
       if var==2:
           medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                       ascending=False).reset_index()
           medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
           medal_tally.index += 1
           medal_tally.rename_axis(index='Ranking')
           ##################
           var_2 = list(medal_tally['Gold'])
           var_2.extend(list(medal_tally['Silver']))
           var_2.extend(list(medal_tally['Bronze']))

           ####################
           fm = year_country(data={'Year': x, 'Country': y})
           return render(request, 'enroll/medal_tally.html', {'table': medal_tally, 'form': fm, 'note': statement,'chart': var_2})

       elif var==0:
           medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()
           medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
           medal_tally.index += 1
           medal_tally.rename_axis(index='Ranking')
           ##################

           ####################
           fm = year_country(data={'Year':x,'Country':y})
           return render(request, 'enroll/medal_tally.html', {'table': medal_tally, 'form': fm,'note': statement})

       else:
           medal_tally = medal_tally.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()
           ################################################
           medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
           medal_tally.index += 1
           medal_tally.rename_axis(index='Ranking')
           ##################

           ####################
           fm = year_country(data={'Year':x,'Country':y})
           return render(request, 'enroll/medal_tally.html', {'table': medal_tally, 'form': fm,'note':statement})

   else:
       medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()
       medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
       medal_tally.index += 1
       medal_tally.rename_axis(index='Ranking')

       """
       medal_tally = medal_tally.reset_index().to_json(orient='records')
       arr = []
       arr = json.loads(medal_tally)
       """
       ##############


       ################
       fm=year_country()
       statement = "Overall Olymic Tally- since 1896"

       ###############



       return render(request, 'enroll/medal_tally.html', {'table': medal_tally, 'form':fm, 'note':statement})


def Overall_analysis(request):

    if request.method=='POST':
        fm = Overanalysis(request.POST)
        if fm.is_valid():
            var = fm.cleaned_data['search_sport']

        a = files()
        b = dataframe()
        event_num = b['Event'].unique().shape
        sports_num = b['Sport'].unique().shape
        country_num = b['region'].unique().shape
        edition_num = b['Year'].unique().shape
        athlete_num = a['Name'].unique().shape



        ##################
        pl = b.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values('index')
        c = list(pl['index'])
        d = list(pl['Year'])

        ##############
        pl2 = b.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index().sort_values('index')
        e = list(pl2['index'])
        f = list(pl2['Year'])

         #####################
        df_1 = b.dropna(subset=['Medal'])
        df_1 = df_1['Name'].value_counts().reset_index().merge(b, left_on='index', right_on='Name')[
            ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index').reset_index()
        df_1 = df_1[df_1['Sport'] == var]
        df_1.drop(['level_0'], axis=1)
        df_1 = df_1.head(10)

        ##############
        df_5 = a.drop_duplicates(['Year', 'Sport', 'Event'])
        df_5 = df_5.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')
        graph = get_graph(df_5)


    else:
        fm=Overanalysis()

        a = files()
        b = dataframe()
        event_num = b['Event'].unique().shape
        sports_num = b['Sport'].unique().shape
        country_num = b['region'].unique().shape
        edition_num = b['Year'].unique().shape
        athlete_num = a['Name'].unique().shape

        ##############
        pl = b.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values('index')
        c = list(pl['index'])
        d = list(pl['Year'])

         ######################
        pl2 = b.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index().sort_values('index')
        e = list(pl2['index'])
        f = list(pl2['Year'])

        ##############
        df_1 = b.dropna(subset=['Medal'])
        df_1 = df_1['Name'].value_counts().reset_index().merge(b, left_on='index', right_on='Name')[
            ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index').reset_index()
        df_1.drop(['level_0'], axis=1).reset_index()
        df_1.rename(columns={'level_0':'Rank','index':'Name','Name_x':'Medal'},inplace=True)
        df_1 = df_1.head(10)

        ###############
        df_5 = a.drop_duplicates(['Year', 'Sport', 'Event'])
        df_5 = df_5.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')

        graph=get_graph(df_5)


    return render(request, 'enroll/Overall_analysis.html',
                  {'event': event_num, 'sport': sports_num, 'Country': country_num, 'Edition': edition_num,
                   'Athlete': athlete_num,
                   'C': c, 'D': d, 'e': e, 'f': f, 'table': df_1, 'fm':fm,'graph':graph})

def yearwise_analysis(request):
    if request.method=='POST':
        a = dataframe()
        df_x = a.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
        fm=year_form(request.POST)
        if fm.is_valid():
            var=fm.cleaned_data['search_country']

        df_x = df_x[df_x['region'] == var]
        df_m=df_x
        df_x = df_x.groupby('Year').count()['Medal'].reset_index()
        var_x = list(df_x['Year'])
        var_y = list(df_x['Medal'])
        note='Yearwise Performance of {}'.format(var)

        ##########
        df_m=df_m.pivot_table(index="Sport",columns='Year',values='Medal',aggfunc='count').fillna(0)
        graph=get_graph(df_m)

        ##############
        f_1 = a.dropna(subset=['Medal'])
        f_1=f_1[f_1["region"]==var]

        f_1 = f_1['Name'].value_counts().reset_index().merge(a, left_on='index', right_on='Name')[['index', 'Name_x', 'Sport']].drop_duplicates('index').reset_index()
        f_1.drop(['level_0'], axis=1).reset_index()
        f_1.rename(columns={'level_0': 'Rank', 'index': 'Name', 'Name_x': 'Medal'}, inplace=True)
        f_1 = f_1.head(10)



    else:
        a = dataframe()
        df_x = a.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
        fm = year_form(request.POST)
        df_x = df_x[df_x['region'] == 'USA']
        df_m=df_x
        df_x = df_x.groupby('Year').count()['Medal'].reset_index()
        var_x = list(df_x['Year'])
        var_y = list(df_x['Medal'])
        f=year_form()
        note='Yearwise Performance of USA'

        ############
        df_m = df_m.pivot_table(index="Sport", columns='Year', values='Medal', aggfunc='count').fillna(0)
        graph = get_graph(df_m)

        ################
        f_1 = a.dropna(subset=['Medal'])
        f_1 = f_1[f_1["region"] == "USA"]

        f_1 = f_1['Name'].value_counts().reset_index().merge(a, left_on='index', right_on='Name')[['index', 'Name_x', 'Sport']].drop_duplicates('index').reset_index()
        f_1.drop(['level_0'], axis=1).reset_index()
        f_1.rename(columns={'level_0': 'Rank', 'index': 'Name', 'Name_x': 'Medal'}, inplace=True)
        f_1 = f_1.head(10)

    return render(request,'enroll/Yearwise_analysis.html',{'var_x':var_x,'var_y':var_y,'fm':fm,'note':note,'graph':graph,'table':f_1})