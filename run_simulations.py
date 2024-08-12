from simulation_helper_functions import *
import numpy as np
import pandas as pd

def run_n_elections(parties: list, n_voters: int, n_elections: int, n_states: int, movement_rate: str,
                    min_viable_share: float, min_viable_seats: int, noise: str, distribution: str) -> pd.DataFrame:
    
    party_results = pd.DataFrame()
    
    #Initialize the positions of the parties and voters on the issues
    party_positions = np.random.uniform(low=-1,high=1,size=(len(parties),2))
    party_names = np.array(random_party_names(len(parties)))

    voter_positions = create_voter_positions(distribution, n_voters)
    voter_states = np.random.randint(low=0, high=n_states, size=n_voters)

    #Initialize how much the parties will move after a given election
    party_move_rate = get_party_movement(movement_rate)
    rand_amt = get_noise(noise)

    for i in range(n_elections):
        
        #Assign every voter to a party
        voter_parties = party_names[find_closest_pair(voter_positions, party_positions)].tolist()

        #Turn this into a dataframe
        voter_df = pd.DataFrame(voter_positions, columns=['position1','position2'])
        voter_df['party'] = voter_parties
        voter_df['state'] = voter_states

        #Keep the initial results
        if i == 0:
            initial_voter_df = voter_df.copy()

        #Get the average position of every voter in a given party
        avg_voter_pos = voter_df.groupby('party', as_index=False).agg(
            avg_pos1 = ('position1','mean'),
            avg_pos2 = ('position2','mean')
        )

        #Get the amount of votes a party won in a given state
        state_votes = voter_df.groupby(['state','party'], as_index=False)['position1'].count()
        #Get the total amount of votes that a party won, regardless of state
        party_votes = voter_df.groupby('party', as_index=False)['position1'].count()\
            .rename({'position1':'party_votes'}, axis=1)
        
        #Get the index of the party who won the most seats in every state
        max_state_idx = state_votes.groupby('state')['position1'].idxmax()

        #Get the number of seats that each party won
        seat_count = state_votes.loc[max_state_idx, ['state','party']].groupby('party', as_index=False).agg(
            seats=('state','count')
        )

        #Now we throw all of the final voting results in a given election into a dataframe
        
        #get the party positions and add in their names
        party_df = pd.DataFrame(party_positions, columns=['position1','position2'])
        party_df['party'] = party_names

        #merge in the average positions of all of each party's voters
        party_df = party_df.merge(avg_voter_pos[['party','avg_pos1','avg_pos2']], on='party', how='left')

        #create a random amount of noise to move each party by
        rand_x = np.random.uniform(-1,1)*rand_amt
        rand_y = np.random.uniform(-1,1)*rand_amt
        
        #This is where we move the positions of each party
        party_df['new_position1'] = (1-party_move_rate)*party_df['position1'] + party_move_rate*party_df['avg_pos1'] + rand_x
        party_df['new_position2'] = (1-party_move_rate)*party_df['position2'] + party_move_rate*party_df['avg_pos2'] + rand_y

        #Just setting a ceiling on all party positions
        party_df['new_position1'] = np.where(party_df['new_position1'] < -1, -1, party_df['new_position1'])
        party_df['new_position1'] = np.where(party_df['new_position1'] > 1, 1, party_df['new_position1'])

        party_df['new_position2'] = np.where(party_df['new_position2'] < -1, -1, party_df['new_position2'])
        party_df['new_position2'] = np.where(party_df['new_position2'] > 1, 1, party_df['new_position2'])

        party_df = party_df.merge(seat_count, on='party', how='left').merge(party_votes, on='party',how='left')
        party_df['seats'] = party_df['seats'].fillna(0)
        party_df['party_votes'] = party_df['party_votes'].fillna(0)
        
        party_df['vote_share'] = party_df['party_votes']/n_voters

        party_df['election'] = i
        voter_df['election'] = i

        party_results = pd.concat([party_results, party_df])
        # voter_results = pd.concat([voter_results, voter_df])
        
        remaining_parties = party_df[(party_df.seats.values >= min_viable_seats) & (party_df.vote_share.values >= min_viable_share)]
        
        party_positions = remaining_parties[['new_position1','new_position2']].values
        party_names = remaining_parties['party'].to_numpy()

    return party_results, voter_df, initial_voter_df