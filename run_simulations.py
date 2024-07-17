from simulation_helper_functions import *
import numpy as np
import pandas as pd

def run_n_elections(parties: list, n_voters: int, n_elections: int, n_states: int, movement_rate: str,
                    min_viable_share: float, min_viable_seats: int, noise: str) -> pd.DataFrame:
    
    party_results = pd.DataFrame()
    
    party_positions = np.random.uniform(low=-1,high=1,size=(len(parties),2))
    party_names = np.array(random_party_names(len(parties)))

    voter_positions = np.random.uniform(low=-1,high=1,size=(n_voters, 2))
    voter_states = np.random.randint(low=0, high=n_states, size=n_voters)

    if movement_rate == 'A lot':
        party_move_rate = 0.5
    elif movement_rate == 'Some':
        party_move_rate = 0.2
    elif movement_rate == 'A Little':
        party_move_rate = 0.1
    else:
        party_move_rate = 0

    if noise == 'A lot':
        rand_amt = 0.25
    elif noise == 'Some':
        rand_amt = 0.05
    elif noise == 'A Little':
        rand_amt = 0.01
    else:
        rand_amt = 0

    for i in range(n_elections):
        
        voter_parties = party_names[find_closest_pair(voter_positions, party_positions)].tolist()

        voter_df = pd.DataFrame(voter_positions, columns=['position1','position2'])
        voter_df['party'] = voter_parties
        voter_df['state'] = voter_states

        if i == 0:
            initial_voter_df = voter_df.copy()

        avg_voter_pos = voter_df.groupby('party', as_index=False).agg(
            avg_pos1 = ('position1','mean'),
            avg_pos2 = ('position2','mean')
        )

        state_votes = voter_df.groupby(['state','party'], as_index=False)['position1'].count()
        party_votes = voter_df.groupby('party', as_index=False)['position1'].count()\
            .rename({'position1':'party_votes'}, axis=1)
        
        max_state_idx = state_votes.groupby('state')['position1'].idxmax()

        seat_count = state_votes.loc[max_state_idx, ['state','party']].groupby('party', as_index=False).agg(
            seats=('state','count')
        )

        party_df = pd.DataFrame(party_positions, columns=['position1','position2'])
        party_df['party'] = party_names
        party_df = party_df.merge(avg_voter_pos[['party','avg_pos1','avg_pos2']], on='party', how='left')

        rand_x = np.random.uniform(-1,1)*rand_amt
        rand_y = np.random.uniform(-1,1)*rand_amt
        
        party_df['new_position1'] = (1-party_move_rate)*party_df['position1'] + party_move_rate*party_df['avg_pos1'] + rand_x
        party_df['new_position2'] = (1-party_move_rate)*party_df['position2'] + party_move_rate*party_df['avg_pos2'] + rand_y

        party_df['new_position1'] = np.where(party_df['new_position1'] < -1, -1, party_df['new_position1'])
        party_df['new_position1'] = np.where(party_df['new_position1'] > 1, 1, party_df['new_position1'])

        party_df['new_position2'] = np.where(party_df['new_position2'] < -1, -1, party_df['new_position2'])
        party_df['new_position2'] = np.where(party_df['new_position2'] > 1, 1, party_df['new_position2'])

        party_df = party_df.merge(seat_count, on='party', how='left').merge(party_votes, on='party',how='left')
        party_df['seats'] = party_df['seats'].fillna(0)
        party_df['vote_share'] = party_df['party_votes']/n_voters

        party_df['election'] = i
        voter_df['election'] = i

        party_results = pd.concat([party_results, party_df])
        # voter_results = pd.concat([voter_results, voter_df])

        remaining_parties = party_df[(party_df.seats.values >= min_viable_seats) | (party_df.vote_share.values >= min_viable_share)]

        party_positions = remaining_parties[['new_position1','new_position2']].values
        party_names = remaining_parties['party'].to_numpy()

    return party_results, voter_df, initial_voter_df