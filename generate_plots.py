import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import math
from simulation_helper_functions import *

def _add_party_to_state_plots(data, *args, **kwargs):
    sns.scatterplot(data=data, x='position1', y = 'position2', hue='party', s = 20, markers='X', legend=False)

def create_voteshare_time_plot(df, country):

    y = plt.figure(figsize=(10,6))
    sns.scatterplot(data=df, x='election',y='vote_share',hue='party')
    sns.lineplot(data=df, x='election',y='vote_share',hue='party', legend=False)
    plt.title(f'Party Vote Share by {country} Election')
    plt.xlabel('Election')
    plt.ylabel('Vote Share')
    plt.legend(title='Party', loc='upper left')
    plt.ylim(0,1)
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    return y 

def create_seats_time_plot(df, n_states, country):

    x = plt.figure(figsize=(10,6))
    sns.scatterplot(data=df, x='election',y='seats',hue='party')
    sns.lineplot(data=df, x='election',y='seats',hue='party', legend=False)
    plt.title(f'Party {country} Legislature Seats by Election')
    plt.xlabel('Election')
    plt.ylabel('Legislature Seats')
    plt.legend(title='Party', loc='upper left')
    plt.ylim(0,n_states)

    return x 

def create_party_movement_plot(df, n_parties, issues):

    g = sns.FacetGrid(df, col='party', col_wrap=math.ceil(n_parties/2), height=4, aspect=1)

    g.map(sns.scatterplot, 'position1','position2')
    
    g.set_titles("{col_name} Movement by Election")
    g.set_axis_labels(''.join(['Party Position on ',issues[0]]), ''.join(['Party Position on ',issues[1]]))
    g.set(xlim=(-1,1), ylim=(-1,1))

    return g

def create_state_voting_pattern(df, party_df, issues, election_number='First'):

    
    n_states = df['state'].nunique()

    states_plot = sns.FacetGrid(df, col='state', col_wrap=math.ceil(n_states/2), height=4, aspect=1, hue='party')
    
    states_plot.map(sns.scatterplot, 'position1','position2', s = 20)

    axes = states_plot.figure.axes

    for ax in axes:
        ax.scatter(party_df['position1'], party_df['position2'], s = 50, c = 'black')

    states_plot.add_legend()
    states_plot.set_titles(''.join(["State {col_name} - ",election_number," Election Results"]))
    states_plot.set_axis_labels(''.join(['Position on ',issues[0]]), ''.join(['Position on ',issues[1]]))
    states_plot.set(xlim=(-1,1), ylim=(-1,1))

    return states_plot