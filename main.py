import streamlit as st
from run_simulations import *
from simulation_helper_functions import random_party_names
from generate_plots import *

st.markdown("# Election Simulator-tron 9000")
st.markdown("## By Conor McQuiston (alpha 0.1)")
st.markdown('This app will let you simulate a series of elections in your very own country where citizens vote for parties based on important issues. \
            This will let you see how many viable parties your country will end up with based on its parties actions and its electoral system.')

st.markdown('My [Github](https://github.com/mcqconor/Election-Simulation), [LinkedIn](https://www.linkedin.com/in/conor-mcquiston-b6a8761a3), [Portfolio](https://mcqconor.github.io/), [Twitter](https://x.com/conormcq5), and [Substack](https://conormcquiston.substack.com/)')

country_name = st.text_input(label='First, what is your country called?')

st.markdown(
    'Here are the immutable rules of the simulation as it is currently set up: \
    \n1. Parties and Voters are placed on a 2D issue space according to a uniform distribution\
    \n2. Voters will **always** vote for the party closest to them by Euclidean distance\
    \n3. Parties change their positions by some combination of random noise and moving towards their average Voter\
    \n4. If a Party gets the most votes in a given state, they win a Seat in the National Legislature\
    \n5. Parties die if they get below the minimum National Legislature seats AND the minimum National Vote Share\
    \n6. Party Names and the Important Issues are randomly assigned'
)

st.markdown('Now let\'s set up your electoral system, and see how many parties you end up with!')

with st.form(key='Input-Form'):
    st.markdown('#### Simulation Settings')

    election_input = st.number_input(label='How Many Elections Do You Want To Simulate?', min_value=1, max_value=100, value=50, key='int')    

    party_input = st.number_input(label='How Many Parties are There?', min_value=1, max_value=12, value=4)

    voter_input = st.number_input(label = f'How Many Voters Are There In {country_name}?', min_value=10, max_value=10000, step=50, value=1000)

    state_input = st.number_input(label=f'How Many States Does {country_name} Have?', min_value=2, max_value=voter_input, value=5)  
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        party_movement = st.radio(
            label='How much do the parties move towards their voters?',
            options=['A lot','Some','A Little','Not at All'],
            index=2
            )
        
        voter_positions = st.radio(
            label='How are the voters distributed about the important issues?',
            options=['Random','Centrist','Polarized'],
            index=2
        )
        
    with col2:
        randomness = st.radio(
            label='How much do the parties randomly move?',
            options=['A lot','Some','A Little','Not at All'],
            index=3
            )

    with col3:
        min_share = st.number_input(
            label = f'What is the smallest national vote share a party needs to stay viable in {country_name}?',
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.05
        )

    with col4:
        min_seats = st.number_input(
            label = f'What is the fewest number of Legislature Seats a party needs to stay viable in {country_name}?',
            min_value=0,
            max_value=round(state_input/2),
            value=round(0.1*state_input),
            step=1
        )

    

    submit_button = st.form_submit_button(label='Simulate Elections')

party_names = random_party_names(party_input)

issues = select_issues()

party_df, final_voter_df, initial_voter_df = run_n_elections(party_names, voter_input, election_input, state_input, party_movement,
                     min_share, min_seats, randomness, voter_positions)

share_plot = create_voteshare_time_plot(party_df, country_name)
seats_plot = create_seats_time_plot(party_df, state_input, country_name)
movement_plot = create_party_movement_plot(party_df, party_input, issues)
initial_results_plot = create_state_voting_pattern(initial_voter_df, party_df[party_df.election.values == 0], issues, 
                                                   election_number='First')
last_results_plot = create_state_voting_pattern(final_voter_df, party_df[party_df.election.values == election_input-1], issues, 
                                                election_number='Last')

st.markdown(f'***Here\'s an overall summary of how each party did in every {country_name} election over time***')

st.pyplot(share_plot)
st.pyplot(seats_plot)

st.markdown('***Here is how the parties changed their positions over time***')

st.pyplot(movement_plot)

st.markdown(f'***Here is a snapshot of how the parties performed in each given {country_name} state in the first and last election***')
st.pyplot(initial_results_plot)
st.pyplot(last_results_plot)