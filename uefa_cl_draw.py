import streamlit as st
import random
import pandas as pd

# Define the qualified teams and their respective pots for the 2024-25 season
teams_data = [
    # Pot 1 (League champions and previous European winners)
    {'name': 'Manchester City', 'pot': 1},  # England
    {'name': 'Barcelona', 'pot': 1},  # Spain
    {'name': 'Bayern Munich', 'pot': 1},  # Germany
    {'name': 'Paris Saint-Germain', 'pot': 1},  # France
    {'name': 'Feyenoord', 'pot': 1},  # Netherlands
    {'name': 'Sporting CP', 'pot': 1},  # Portugal
    {'name': 'Shakhtar Donetsk', 'pot': 1},  # Ukraine (CL winner rebalancing)
    {'name': 'Benfica', 'pot': 1},  # Portugal (Europa League winner rebalancing)

    # Pot 2 (Other top teams based on coefficients)
    {'name': 'Real Madrid', 'pot': 2},  # Spain
    {'name': 'Arsenal', 'pot': 2},  # England
    {'name': 'Inter Milan', 'pot': 2},  # Italy
    {'name': 'Atlético de Madrid', 'pot': 2},  # Spain
    {'name': 'Liverpool', 'pot': 2},  # England
    {'name': 'Juventus', 'pot': 2},  # Italy
    {'name': 'Borussia Dortmund', 'pot': 2},  # Germany
    {'name': 'Leverkusen', 'pot': 2},  # Germany

    # Pot 3 (Teams with a mid-range coefficient)
    {'name': 'Milan', 'pot': 3},  # Italy
    {'name': 'Leipzig', 'pot': 3},  # Germany
    {'name': 'Atalanta', 'pot': 3},  # Italy
    {'name': 'Monaco', 'pot': 3},  # France
    {'name': 'Celtic', 'pot': 3},  # Scotland
    {'name': 'Club Brugge', 'pot': 3},  # Belgium
    {'name': 'PSV Eindhoven', 'pot': 3},  # Netherlands
    {'name': 'Stuttgart', 'pot': 3},  # Germany

    # Pot 4 (Remaining teams)
    {'name': 'Aston Villa', 'pot': 4},  # England
    {'name': 'Girona', 'pot': 4},  # Spain
    {'name': 'Brest', 'pot': 4},  # France
    {'name': 'Sturm Graz', 'pot': 4},  # Austria
    {'name': 'Bologna', 'pot': 4},  # Italy (European Performance Spot)
    {'name': 'Feyenoord', 'pot': 4},  # Netherlands (Duplicate removed)
]

# Sort teams into pots
pots = {1: [], 2: [], 3: [], 4: []}
for team in teams_data:
    pots[team['pot']].append(team['name'])

# Function to create the draw
def create_draw():
    matches = []
    for i in range(8):  # Each team plays 8 matches
        for pot_num, pot_teams in pots.items():
            random.shuffle(pot_teams)
            for j in range(0, len(pot_teams) - 1, 2):
                home_team = pot_teams[j]
                away_team = pot_teams[j + 1]
                match = {'home_team': home_team, 'away_team': away_team, 'home_score': None, 'away_score': None}
                matches.append(match)

                # Reverse the home and away for the next match
                match_reverse = {'home_team': away_team, 'away_team': home_team, 'home_score': None, 'away_score': None}
                matches.append(match_reverse)
            
            # If there's an odd number of teams, handle the last team here
            if len(pot_teams) % 2 == 1:
                unpaired_team = pot_teams[-1]
                # Custom logic for unpaired teams can go here (e.g., bye, carryover, etc.)
                # For now, we'll just skip any unpaired team
                st.warning(f"Unpaired team in Pot {pot_num}: {unpaired_team}")

    return matches

# Function to simulate the matches
def simulate_matches(matches):
    standings = {team['name']: {'points': 0, 'matches_played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'goals_for': 0, 'goals_against': 0, 'goal_difference': 0}
                 for team in teams_data}
    
    for match in matches:
        if match['home_score'] is None or match['away_score'] is None:  # Skip already simulated matches
            match['home_score'] = random.randint(0, 5)
            match['away_score'] = random.randint(0, 5)
        
        home_team = match['home_team']
        away_team = match['away_team']
        
        standings[home_team]['matches_played'] += 1
        standings[away_team]['matches_played'] += 1
        standings[home_team]['goals_for'] += match['home_score']
        standings[home_team]['goals_against'] += match['away_score']
        standings[away_team]['goals_for'] += match['away_score']
        standings[away_team]['goals_against'] += match['home_score']
        
        if match['home_score'] > match['away_score']:
            standings[home_team]['wins'] += 1
            standings[home_team]['points'] += 3
            standings[away_team]['losses'] += 1
        elif match['home_score'] < match['away_score']:
            standings[away_team]['wins'] += 1
            standings[away_team]['points'] += 3
            standings[home_team]['losses'] += 1
        else:
            standings[home_team]['draws'] += 1
            standings[away_team]['draws'] += 1
            standings[home_team]['points'] += 1
            standings[away_team]['points'] += 1

        standings[home_team]['goal_difference'] = standings[home_team]['goals_for'] - standings[home_team]['goals_against']
        standings[away_team]['goal_difference'] = standings[away_team]['goals_for'] - standings[away_team]['goals_against']

    return standings

# Sidebar Navigation
st.sidebar.title("UEFA Champions League")
page = st.sidebar.selectbox("Navigate", ["Home", "View Pots", "Create Draw", "View Matches", "View Standings"])

# Home Page
if page == "Home":
    st.title("UEFA Champions League 2024-25")
    st.write("""
        Welcome to the interactive UEFA Champions League 2024-25 simulation.
        Use the sidebar to navigate between viewing the seeding pots, creating the match draw,
        simulating the games, and viewing the standings.
    """)

# View Pots Page
if page == "View Pots":
    st.title("Seeding Pots")
    for pot_num, teams in pots.items():
        st.subheader(f"Pot {pot_num}")
        pot_table = pd.DataFrame(teams, columns=[f"Pot {pot_num} Teams"])
        st.table(pot_table)

# Create Draw Page
if page == "Create Draw":
    st.title("Create the Match Draw")
    if st.button("Generate Draw"):
        matches = create_draw()
        st.session_state['matches'] = matches
        st.success("Draw generated successfully!")

    if 'matches' in st.session_state:
        st.header("Match Draw")
        draw_table = pd.DataFrame(st.session_state['matches'])
        draw_table['Result'] = draw_table.apply(lambda x: f"{x['home_team']} vs {x['away_team']}", axis=1)
        st.table(draw_table[['Result']])

# View Matches Page
if page == "View Matches":
    st.title("Simulate Matches")
    if st.button("Simulate All Matches"):
        if 'matches' in st.session_state:
            standings = simulate_matches(st.session_state['matches'])
            st.session_state['standings'] = standings
            st.success("Matches simulated successfully!")
        else:
            st.warning("Please generate the match draw first.")

    if 'matches' in st.session_state:
        st.header("Match Results")
        results_table = pd.DataFrame(st.session_state['matches'])
        results_table['Match'] = results_table.apply(lambda x: f"{x['home_team']} {x['home_score']} - {x['away_score']} {x['away_team']}", axis=1)
        st.table(results_table[['Match']])

# View Standings Page
if page == "View Standings":
    st.title("Standings")
    if 'standings' in st.session_state:
        sorted_standings = sorted(st.session_state['standings'].items(), key=lambda x: (-x[1]['points'], -x[1]['goal_difference'], -x[1]['goals_for']))
        standings_table = pd.DataFrame([{
            'Team': team,
            'Matches Played': stats['matches_played'],
            'Wins': stats['wins'],
            'Draws': stats['draws'],
            'Losses': stats['losses'],
            'Goals For': stats['goals_for'],
            'Goals Against': stats['goals_against'],
            'Goal Difference': stats['goal_difference'],
            'Points': stats['points']
        } for team, stats in sorted_standings])
        st.table(standings_table)
    else:
        st.warning("No standings available. Please simulate matches first.")
        
st.write("© 2024 Mohamed Osman & UEFA Champions League. All rights reserved.")
# Reset Option
if st.sidebar.button("Reset All"):
    st.session_state.clear()
    st.success("All data reset successfully!")
