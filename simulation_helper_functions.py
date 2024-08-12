import random
from scipy.spatial.distance import cdist
import numpy as np
import random
import math

def create_voter_positions(distribution: str, n_voters: int) -> np.array:

    if distribution == 'Random':
        return np.random.uniform(low=-1,high=1,size=(n_voters, 2))
    
    elif distribution == 'Centrist':
        
        normal_dist = np.random.normal(loc=0, scale=0.25, size=(n_voters, 2))

        normal_dist[normal_dist > 1] = 1
        normal_dist[normal_dist < -1] = -1

        return normal_dist
    
    elif distribution == 'Polarized':
        
        left_positions = np.random.normal(loc=-0.75, scale=0.25, size=(math.ceil(n_voters/2), 2))
        right_positions = np.random.normal(loc=0.75, scale=0.25, size=(math.ceil(n_voters/2), 2))

        bimodal = np.vstack((left_positions, right_positions))

        bimodal[bimodal > 1] = 1
        bimodal[bimodal < -1] = -1

        return bimodal
        
    else:
        return 0

def get_party_movement(input_string: str) -> float:

    if input_string == 'A lot':
        return 0.5
    elif input_string == 'Some':
        return 0.2
    elif input_string == 'A Little':
        return 0.1
    else:
        return 0

def get_noise(input_string: str) -> float:

    if input_string == 'A lot':
        return 0.25
    elif input_string == 'Some':
        return 0.05
    elif input == 'A Little':
        return 0.01
    else:
        return 0

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
        'Shot Clock Length',
        'Railroad Control'
    ]

    return random.sample(potential_issues,2)
