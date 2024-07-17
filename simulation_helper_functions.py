import random
from scipy.spatial.distance import cdist
import numpy as np
import random

#Generates random colors for the parties so the plotting is prettier later
def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

#this finds the party closest to each voter in an arbitrary dimension
def find_closest_pair(set1, set2):

    #this gets us all pairwise distances
    distances = cdist(set1, set2) 

    #this gest us the index of the minimum distance
    return np.argmin(distances, axis = 1)

def random_party_names(party_list_size: int) -> list:

    potential_party_names = [
        'Squirtle',
        'Bulbasaur',
        'Charmander',
        'Totodile',
        'Chikorita',
        'Cyndaquil',
        'Democrats',
        'Republicans',
        'Democratic-Republicans',
        'Whigs',
        'Know Nothings',
        'Progressives',
        'Reform',
        'Tories',
        'Labor',
        'Bolsheviks',
        'CCP',
        'Eevee',
        'Philadelphia Phillies',
        'Minecraft Creepers',
        'Seattle Seahawks',
        'Paradox Interactive',
        'Mudkip',
        'Torchic',
        'Treecko',
        'Conservatives',
        'Liberals',
        'Mugwumps',
        'Seattle Sonics',
        'Denver Broncos',
        'Detroit Red Wings',
        'Toronto Maple Leafs'
    ]

    return random.sample(potential_party_names, party_list_size)

def select_issues() -> list:

    potential_issues = [
        'Abortion',
        'Gun Control',
        'Mango Prices',
        'Tariff Control',
        'Voting Reform',
        'Tax Policy',
        'Colonial Policy',
        'Legal Driving Age',
        'Prohibition',
        'Regulation Basketball Hoop Height',
        'Defensive Pass Interference Rules',
        'Hockey Period Length',
        'Pokémon License Age',
        'School Prayer',
        'Immigration Policy',
        'Environmental Policy',
        'Shot Clock Length'
    ]

    return random.sample(potential_issues,2)
