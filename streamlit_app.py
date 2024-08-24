import streamlit as st
import pandas as pd
import random

# List of 29 existing teams and their points
teams = {
    "Team": ["Manchester City", "Bayern München", "Real Madrid", "Paris Saint-Germain", "Liverpool",
             "Internazionale", "Borussia Dortmund", "RB Leipzig", "FC Barcelona", "Bayer Leverkusen",
             "Atlético Madrid", "Atalanta", "Juventus", "Benfica", "Arsenal", "Club Brugge",
             "Shakhtar Donetsk", "AC Milan", "Feyenoord", "Sporting CP Lisbon", "PSV Eindhoven",
             "Celtic", "AS Monaco", "Aston Villa", "Sturm Graz", "Bologna", "Girona",
             "Stuttgart", "Brest"],
    "Points": [148, 144, 136, 116, 114, 101, 97, 97, 91, 90, 89, 81, 80, 79, 72, 64, 63, 59, 57, 54.5,
               54, 32, 24, 20.86, 14.5, 18.056, 17.897, 17.324, 13.366],
    "Country": ["England", "Germany", "Spain", "France", "England",
                "Italy", "Germany", "Germany", "Spain", "Germany",
                "Spain", "Italy", "Italy", "Portugal", "England", "Belgium",
                "Ukraine", "Italy", "Netherlands", "Portugal", "Netherlands",
                "Scotland", "France", "England", "Austria", "Italy", "Spain",
                "Germany", "France"]
}

# List of new matchups
matchups = {
    "Match1": {"team1": "Slavia Praha", "points1": 53, "country1": "Czech Republic",
               "team2": "Lille OSC", "points2": 47, "country2": "France"},
    "Match2": {"team1": "FC Salzburg", "points1": 50, "country1": "Austria",
               "team2": "Dynamo Kyiv", "points2": 26.5, "country2": "Ukraine"},
    "Match3": {"team1": "Dinamo Zagreb", "points1": 50, "country1": "Croatia",
               "team2": "Qarabag FK", "points2": 33, "country2": "Azerbaijan"},
    "Match4": {"team1": "Red Star Belgrade", "points1": 40, "country1": "Serbia",
               "team2": "Bodø/Glimt", "points2": 28, "country2": "Norway"},
    "Match5": {"team1": "Young Boys", "points1": 34.5, "country1": "Switzerland",
               "team2": "Galatasaray", "points2": 31.5, "country2": "Turkey"},
    "Match6": {"team1": "Slovan Bratislava", "points1": 30.5, "country1": "Slovakia",
               "team2": "FC Midtjylland", "points2": 25.5, "country2": "Denmark"},
    "Match7": {"team1": "Sparta Praha", "points1": 22.5, "country1": "Czech Republic",
               "team2": "Malmö FF", "points2": 18.5, "country2": "Sweden"}
}

# List of selected winner teams (using Streamlit's session_state to retain selections)
if 'winners' not in st.session_state:
    st.session_state.winners = {}

# Create dropdown menus for each matchup
st.title("Matchups")
for matchup, details in matchups.items():
    team1 = details["team1"]
    points1 = details["points1"]
    country1 = details["country1"]
    team2 = details["team2"]
    points2 = details["points2"]
    country2 = details["country2"]

    selected_team = st.selectbox(f"{matchup}: {team1} ({country1}) vs {team2} ({country2})",
                                 options=[team1, team2],
                                 key=f"{matchup}_selectbox")

    # Update the winner team
    if selected_team == team1:
        st.session_state.winners[matchup] = {"Team": team1, "Points": points1, "Country": country1}
    else:
        st.session_state.winners[matchup] = {"Team": team2, "Points": points2, "Country": country2}

# Add selected winner teams to the existing teams list
for winner in st.session_state.winners.values():
    if winner["Team"] not in teams["Team"]:
        teams["Team"].append(winner["Team"])
        teams["Points"].append(winner["Points"])
        teams["Country"].append(winner["Country"])

# Create a DataFrame for all teams
df = pd.DataFrame(teams)

# Sort teams by points in descending order
df_sorted = df.sort_values(by="Points", ascending=False).reset_index(drop=True)

# Split into 9-team groups
pot1 = df_sorted.iloc[:9]
pot2 = df_sorted.iloc[9:18]
pot3 = df_sorted.iloc[18:27]
pot4 = df_sorted.iloc[27:]

# Display the teams in 4 different columns
st.title("Teams Distribution into Pots")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.header("Pot 1")
    st.dataframe(pot1)

with col2:
    st.header("Pot 2")
    st.dataframe(pot2)

with col3:
    st.header("Pot 3")
    st.dataframe(pot3)

with col4:
    st.header("Pot 4")
    st.dataframe(pot4)

# Selected team and matchups are stored in session_state
if 'choosen' not in st.session_state:
    st.session_state.choosen = None

# Team selection
choosen = st.selectbox(
    "Which team would you like to choose?",
    options=df_sorted["Team"],
    key="team_selectbox"
)

# Select 2 teams from each pot and prevent matching with the same country
selected_teams = []

for pot in [pot1, pot2, pot3, pot4]:
    teams_from_pot = [team for team in pot.to_dict('records') if team["Team"] != choosen and team["Country"] != df_sorted[df_sorted["Team"] == choosen]["Country"].values[0]]
    if len(teams_from_pot) >= 2:
        selected_teams_sample = random.sample(teams_from_pot, 2)
        # First team plays at home, second team plays away
        selected_teams.append((choosen, selected_teams_sample[0]["Team"]))  # Home team
        selected_teams.append((selected_teams_sample[1]["Team"], choosen))  # Away team

# Display results
st.title(f"Random Matchups for {choosen}")
st.write(f"Selected team: {choosen}")
st.write("Fixture:")
random.shuffle(selected_teams)
for idx, (home, away) in enumerate(selected_teams, start=1):
    st.write(f"Match {idx}: {home} vs {away}")
