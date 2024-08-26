import streamlit as st
import pandas as pd
import random

st.title("Tournament Selection")

tournament_selected = st.selectbox("Please select a tournament:", ("UCL", "UEL", "UECL"))

# Color codes (Example)
UCL_color = "#AEC6FF"  # Blue tone
UEL_color = "#FFD8A8"  # Purple tone
UECL_color = "#C7EACF"  # Green tone

# Select the appropriate background color based on the selected tournament
if tournament_selected == "UCL":
    background_color = UCL_color
elif tournament_selected == "UEL":
    background_color = UEL_color
elif tournament_selected == "UECL":
    background_color = UECL_color
else:
    background_color = "#FFFFFF"  # Default color


# Inject CSS for background, text, header, and dropdown label color
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {background_color};
        color: black;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: black;
    }}
    .stSelectbox > label, .stSelectbox > div > div > label {{
        color: black !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# The rest of your code remains unchanged
if tournament_selected == "UCL":

    st.markdown(f"<style>body {{background-color: {UCL_color};}}</style>", unsafe_allow_html=True)

    # List of 29 existing teams and their points
    ucl_teams = {
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
    if 'ucl_winners' not in st.session_state:
        st.session_state.ucl_winners = {}

    # Create dropdown menus for each matchup
    st.title("Qualification")
    for matchup, details in matchups.items():
        team1 = details["team1"]
        points1 = details["points1"]
        country1 = details["country1"]
        team2 = details["team2"]
        points2 = details["points2"]
        country2 = details["country2"]

        selected_team = st.selectbox(f"{matchup}: {team1} vs {team2}",
                                     options=[team1, team2],
                                     key=f"{matchup}_selectbox")

        # Update the winner team
        if selected_team == team1:
            st.session_state.ucl_winners[matchup] = {"Team": team1, "Points": points1, "Country": country1}
        else:
            st.session_state.ucl_winners[matchup] = {"Team": team2, "Points": points2, "Country": country2}

    # Add selected winner teams to the existing teams list
    for ucl_winners in st.session_state.ucl_winners.values():
        if ucl_winners["Team"] not in ucl_teams["Team"]:
            ucl_teams["Team"].append(ucl_winners["Team"])
            ucl_teams["Points"].append(ucl_winners["Points"])
            ucl_teams["Country"].append(ucl_winners["Country"])

    # Create a DataFrame for all teams
    df = pd.DataFrame(ucl_teams)

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

    # Initialize a dictionary to keep track of how many teams from each country have been selected
    country_count = {}

    selected_teams = []

    for pot in [pot1, pot2, pot3, pot4]:
        teams_from_pot = [team for team in pot.to_dict('records') if team["Team"] != choosen and team["Country"] !=
                          df_sorted[df_sorted["Team"] == choosen]["Country"].values[0]]

        # Filter out teams from countries that already have 2 teams selected
        teams_from_pot = [team for team in teams_from_pot if country_count.get(team["Country"], 0) < 2]

        if len(teams_from_pot) >= 2:
            selected_teams_sample = random.sample(teams_from_pot, 2)

            # Update the country count for each selected team
            for team in selected_teams_sample:
                country_count[team["Country"]] = country_count.get(team["Country"], 0) + 1

            # First team plays at home, second team plays away
            selected_teams.append((choosen, selected_teams_sample[0]["Team"]))  # Home team
            selected_teams.append((selected_teams_sample[1]["Team"], choosen))  # Away team

    # Ensure no three consecutive home or away matches
    final_fixture = []
    random.shuffle(selected_teams)  # Optionally shuffle the final fixture
    for i in range(len(selected_teams)):
        home, away = selected_teams[i]

        # Check the last two matches to avoid three consecutive home or away matches
        if len(final_fixture) >= 2:
            last_home1, last_away1 = final_fixture[-1]
            last_home2, last_away2 = final_fixture[-2]

            if (home == choosen and last_home1 == choosen and last_home2 == choosen) or \
                    (away == choosen and last_away1 == choosen and last_away2 == choosen):
                # Swap the current match with the next one if available
                if i < len(selected_teams) - 1:
                    home, away = selected_teams[i + 1]
                    selected_teams[i + 1] = selected_teams[i]

        final_fixture.append((home, away))

    # Display results
    st.title(f"Fixture for **{choosen}**")
    for idx, (home, away) in enumerate(final_fixture, start=1):
        home_bold = f"**{home}**" if home == choosen else home
        away_bold = f"**{away}**" if away == choosen else away
        st.write(f"Match {idx}: {home_bold} vs {away_bold}")


elif tournament_selected == "UEL":


    st.markdown(f"<style>body {{background-color: {UEL_color};}}</style>", unsafe_allow_html=True)

    # Create a list of tuples from the given data
    uel_teams = {
        "Team": ["AS Roma", "Manchester United", "FC Porto", "Glasgow Rangers", "Eintracht Frankfurt", "Lazio",
                 "Tottenham Hotspur", "Real Sociedad", "AZ Alkmaar", "Olympiakos Piraeus", "Olympique Lyon",
                 "Fenerbahçe", "Union Saint-Gilloise", "1899 Hoffenheim", "OGC Nice", "FC Twente Enschede",
                 "A. Bilbao"],
        "Points": [101, 92, 77, 63, 60, 54, 54, 51, 50, 48, 44, 36, 27, 17.324, 17, 12.26, 17.897],
        "Country": ["Italy", "England", "Portugal", "Scotland", "Germany", "Italy", "England", "Spain", "Netherlands",
                    "Greece", "France", "Turkey", "Belgium", "Germany", "France", "Netherlands", "Spain"]
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
                   "team2": "Malmö FF", "points2": 18.5, "country2": "Sweden"},
        "Match8": {"team1": "Ajax", "points1": 67, "country1": "Netherlands",
                   "team2": "Jagiellonia Białystok", "points2": 5.075, "country2": "Poland"},
        "Match9": {"team1": "Sporting Braga", "points1": 49, "country1": "Portugal",
                   "team2": "Rapid Wien", "points2": 14, "country2": "Austria"},
        "Match10": {"team1": "PAOK Thessaloniki", "points1": 37, "country1": "Greece",
                    "team2": "Shamrock Rovers", "points2": 9.5, "country2": "Ireland"},
        "Match11": {"team1": "LASK", "points1": 37, "country1": "Austria",
                    "team2": "FCSB", "points2": 10.5, "country2": "Romania"},
        "Match12": {"team1": "Maccabi Tel-Aviv", "points1": 35.5, "country1": "Israel",
                    "team2": "TSC Bačka Topola", "points2": 5.555, "country2": "Serbia"},
        "Match13": {"team1": "Ferencváros", "points1": 35, "country1": "Hungary",
                    "team2": "FK Borac Banja Luka", "points2": 5.5, "country2": "Bosnia and Herzegovina"},
        "Match14": {"team1": "Molde FK", "points1": 28.5, "country1": "Norway",
                    "team2": "IF Elfsborg", "points2": 4.3, "country2": "Sweden"},
        "Match15": {"team1": "Viktoria Plzeň", "points1": 28, "country1": "Czech Republic",
                    "team2": "Heart of Midlothian", "points2": 7.21, "country2": "Scotland"},
        "Match16": {"team1": "Ludogorets Razgrad", "points1": 26, "country1": "Bulgaria",
                    "team2": "Petrocub Hîncesti", "points2": 7, "country2": "Moldova"},
        "Match17": {"team1": "APOEL Nicosia", "points1": 14.5, "country1": "Cyprus",
                    "team2": "RFS Riga", "points2": 8, "country2": "Latvia"},
        "Match18": {"team1": "Anderlecht", "points1": 14.5, "country1": "Belgium",
                    "team2": "Dinamo Minsk", "points2": 4.5, "country2": "Belarus"},
        "Match19": {"team1": "Beşiktaş", "points1": 12, "country1": "Turkey",
                    "team2": "FC Lugano", "points2": 8, "country2": "Switzerland"}
    }

    # List of selected winner teams (using Streamlit's session_state to retain selections)
    if 'uel_winners' not in st.session_state:
        st.session_state.uel_winners = {}

    # Create dropdown menus for each matchup
    st.title("Qualification")
    for matchup, details in matchups.items():
        team1 = details["team1"]
        points1 = details["points1"]
        country1 = details["country1"]
        team2 = details["team2"]
        points2 = details["points2"]
        country2 = details["country2"]

        selected_team = st.selectbox(f"{matchup}: {team1} vs {team2}",
                                     options=[team1, team2],
                                     key=f"{matchup}_selectbox")

        # Determine if it's one of the first 7 matches
        match_number = int(matchup.replace("Match", ""))

        # For the first 7 matches, add the losing team
        if match_number <= 7:
            losing_team = team2 if selected_team == team1 else team1
            losing_points = points2 if selected_team == team1 else points1
            losing_country = country2 if selected_team == team1 else country1
            st.session_state.uel_winners[matchup] = {"Team": losing_team, "Points": losing_points,
                                                 "Country": losing_country}
        # For the other matches, add the winning team
        else:
            st.session_state.uel_winners[matchup] = {"Team": selected_team,
                                                 "Points": points1 if selected_team == team1 else points2,
                                                 "Country": country1 if selected_team == team1 else country2}

    # Add selected winner/loser teams to the existing teams list
    for uel_winners in st.session_state.uel_winners.values():
        if uel_winners["Team"] not in uel_teams["Team"]:
            uel_teams["Team"].append(uel_winners["Team"])
            uel_teams["Points"].append(uel_winners["Points"])
            uel_teams["Country"].append(uel_winners["Country"])

    # Create a DataFrame for all teams
    df = pd.DataFrame(uel_teams)

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

    # Initialize a dictionary to keep track of how many teams from each country have been selected
    country_count = {}

    selected_teams = []

    for pot in [pot1, pot2, pot3, pot4]:
        teams_from_pot = [team for team in pot.to_dict('records') if team["Team"] != choosen and team["Country"] !=
                          df_sorted[df_sorted["Team"] == choosen]["Country"].values[0]]

        # Filter out teams from countries that already have 2 teams selected
        teams_from_pot = [team for team in teams_from_pot if country_count.get(team["Country"], 0) < 2]

        if len(teams_from_pot) >= 2:
            selected_teams_sample = random.sample(teams_from_pot, 2)

            # Update the country count for each selected team
            for team in selected_teams_sample:
                country_count[team["Country"]] = country_count.get(team["Country"], 0) + 1

            # First team plays at home, second team plays away
            selected_teams.append((choosen, selected_teams_sample[0]["Team"]))  # Home team
            selected_teams.append((selected_teams_sample[1]["Team"], choosen))  # Away team

    # Ensure no three consecutive home or away matches
    final_fixture = []
    random.shuffle(selected_teams)  # Optionally shuffle the final fixture
    for i in range(len(selected_teams)):
        home, away = selected_teams[i]

        # Check the last two matches to avoid three consecutive home or away matches
        if len(final_fixture) >= 2:
            last_home1, last_away1 = final_fixture[-1]
            last_home2, last_away2 = final_fixture[-2]

            if (home == choosen and last_home1 == choosen and last_home2 == choosen) or \
                    (away == choosen and last_away1 == choosen and last_away2 == choosen):
                # Swap the current match with the next one if available
                if i < len(selected_teams) - 1:
                    home, away = selected_teams[i + 1]
                    selected_teams[i + 1] = selected_teams[i]

        final_fixture.append((home, away))

    # Display results
    st.title(f"Fixture for **{choosen}**")
    for idx, (home, away) in enumerate(final_fixture, start=1):
        home_bold = f"**{home}**" if home == choosen else home
        away_bold = f"**{away}**" if away == choosen else away
        st.write(f"Match {idx}: {home_bold} vs {away_bold}")

elif tournament_selected == "UECL":


    st.markdown(f"<style>body {{background-color: {UECL_color};}}</style>", unsafe_allow_html=True)

    # Create a list of tuples from the given data
    uecl_teams = {
        "Team": [],
        "Points": [],
        "Country": []
    }

    # List of new matchups
    matchups = {
        "Match1": {"team1": "Ajax", "points1": 67, "country1": "Netherlands",
                   "team2": "Jagiellonia Białystok", "points2": 5.075, "country2": "Poland"},
        "Match2": {"team1": "Sporting Braga", "points1": 49, "country1": "Portugal",
                   "team2": "Rapid Wien", "points2": 14, "country2": "Austria"},
        "Match3": {"team1": "PAOK Thessaloniki", "points1": 37, "country1": "Greece",
                   "team2": "Shamrock Rovers", "points2": 9.5, "country2": "Ireland"},
        "Match4": {"team1": "LASK", "points1": 37, "country1": "Austria",
                   "team2": "FCSB", "points2": 10.5, "country2": "Romania"},
        "Match5": {"team1": "Maccabi Tel-Aviv", "points1": 35.5, "country1": "Israel",
                   "team2": "TSC Bačka Topola", "points2": 5.555, "country2": "Serbia"},
        "Match6": {"team1": "Ferencváros", "points1": 35, "country1": "Hungary",
                   "team2": "FK Borac Banja Luka", "points2": 5.5, "country2": "Bosnia and Herzegovina"},
        "Match7": {"team1": "Molde FK", "points1": 28.5, "country1": "Norway",
                   "team2": "IF Elfsborg", "points2": 4.3, "country2": "Sweden"},
        "Match8": {"team1": "Viktoria Plzeň", "points1": 28, "country1": "Czech Republic",
                   "team2": "Heart of Midlothian", "points2": 7.21, "country2": "Scotland"},
        "Match9": {"team1": "Ludogorets Razgrad", "points1": 26, "country1": "Bulgaria",
                   "team2": "Petrocub Hîncesti", "points2": 7, "country2": "Moldova"},
        "Match10": {"team1": "APOEL Nicosia", "points1": 14.5, "country1": "Cyprus",
                    "team2": "RFS Riga", "points2": 8, "country2": "Latvia"},
        "Match11": {"team1": "Anderlecht", "points1": 14.5, "country1": "Belgium",
                    "team2": "Dinamo Minsk", "points2": 4.5, "country2": "Belarus"},
        "Match12": {"team1": "Beşiktaş", "points1": 12, "country1": "Turkey",
                    "team2": "FC Lugano", "points2": 8, "country2": "Switzerland"},
        "Match13": {"team1": "Chelsea", "points1": 96, "country1": "England",
                    "team2": "Servette FC Genève", "points2": 9, "country2": "Switzerland"},
        "Match14": {"team1": "FC København", "points1": 51.5, "country1": "Denmark",
                    "team2": "Kilmarnock", "points2": 7.21, "country2": "Scotland"},
        "Match15": {"team1": "AA Gent", "points1": 45, "country1": "Belgium",
                    "team2": "Partizan Belgrade", "points2": 25.5, "country2": "Serbia"},
        "Match16": {"team1": "Fiorentina", "points1": 42, "country1": "Italy",
                    "team2": "Puskás Akadémia", "points2": 4.375, "country2": "Hungary"},
        "Match17": {"team1": "Real Betis", "points1": 33, "country1": "Spain",
                    "team2": "Kryvbas", "points2": 5.6, "country2": "Ukraine"},
        "Match18": {"team1": "Istanbul Başakşehir", "points1": 29, "country1": "Turkey",
                    "team2": "St. Patrick's Athletic", "points2": 4, "country2": "Ireland"},
        "Match19": {"team1": "CFR Cluj", "points1": 26.5, "country1": "Romania",
                    "team2": "Pafos", "points2": 4.42, "country2": "Cyprus"},
        "Match20": {"team1": "Legia Warsaw", "points1": 18, "country1": "Poland",
                    "team2": "FC Drita", "points2": 6.5, "country2": "Kosovo"},
        "Match21": {"team1": "Heidenheim", "points1": 17.324, "country1": "Germany",
                    "team2": "Hacken", "points2": 4.3, "country2": "Sweden"},
        "Match22": {"team1": "Djurgårdens IF", "points1": 16.5, "country1": "Sweden",
                    "team2": "NK Maribor", "points2": 9.5, "country2": "Slovenia"},
        "Match23": {"team1": "RC Lens", "points1": 13.366, "country1": "France",
                    "team2": "Panathinaikos", "points2": 6.305, "country2": "Greece"},
        "Match24": {"team1": "NK Rijeka", "points1": 12, "country1": "Croatia",
                    "team2": "Olimpija Ljubljana", "points2": 10.5, "country2": "Slovenia"},
        "Match25": {"team1": "Omonia Nicosia", "points1": 12, "country1": "Cyprus",
                    "team2": "Zira FK", "points2": 4.025, "country2": "Azerbaijan"},
        "Match26": {"team1": "HJK Helsinki", "points1": 11.5, "country1": "Finland",
                    "team2": "KI Klaksvik", "points2": 10, "country2": "Faroe Islands"},
        "Match27": {"team1": "Trabzonspor", "points1": 11.5, "country1": "Turkey",
                    "team2": "FC Sankt Gallen", "points2": 6.595, "country2": "Switzerland"},
        "Match28": {"team1": "Vitória Guimarães", "points1": 11.263, "country1": "Portugal",
                    "team2": "Zrinjski Mostar", "points2": 9.5, "country2": "Bosnia and Herzegovina"},
        "Match29": {"team1": "FK Astana", "points1": 11, "country1": "Kazakhstan",
                    "team2": "SK Brann Bergen", "points2": 6.325, "country2": "Norway"},
        "Match30": {"team1": "Cercle Brugge", "points1": 9.76, "country1": "Belgium",
                    "team2": "Wisła Kraków", "points2": 5.075, "country2": "Poland"},
        "Match31": {"team1": "Lincoln Red Imps", "points1": 9, "country1": "Gibraltar",
                    "team2": "Larne FC", "points2": 4.5, "country2": "Northern Ireland"},
        "Match32": {"team1": "The New Saints", "points1": 8.5, "country1": "Wales",
                    "team2": "FK Panevėžys", "points2": 4, "country2": "Lithuania"},
        "Match33": {"team1": "Pyunik Yerevan", "points1": 8, "country1": "Armenia",
                    "team2": "NK Celje", "points2": 4.5, "country2": "Slovenia"},
        "Match34": {"team1": "Mladá Boleslav", "points1": 7.21, "country1": "Czech Republic",
                    "team2": "Paksi", "points2": 4.375, "country2": "Hungary"},
        "Match35": {"team1": "Vikingur Reykjavik", "points1": 4, "country1": "Iceland",
                    "team2": "UE Santa Coloma", "points2": 1.199, "country2": "Andorra"},
        "Match36": {"team1": "MFK Ruzomberok", "points1": 3.925, "country1": "Slovakia",
                    "team2": "FC Noah", "points2": 2.125, "country2": "Armenia"}
    }

    # List of selected winner teams (using Streamlit's session_state to retain selections)
    if 'winners' not in st.session_state:
        st.session_state.winners = {}

    # Create dropdown menus for each matchup
    st.title("Qualification")
    for matchup, details in matchups.items():
        team1 = details["team1"]
        points1 = details["points1"]
        country1 = details["country1"]
        team2 = details["team2"]
        points2 = details["points2"]
        country2 = details["country2"]

        selected_team = st.selectbox(f"{matchup}: {team1} vs {team2}",
                                     options=[team1, team2],
                                     key=f"{matchup}_selectbox")

        # Determine if it's one of the first 7 matches
        match_number = int(matchup.replace("Match", ""))

        # For the first 7 matches, add the losing team
        if match_number <= 12:
            losing_team = team2 if selected_team == team1 else team1
            losing_points = points2 if selected_team == team1 else points1
            losing_country = country2 if selected_team == team1 else country1
            st.session_state.winners[matchup] = {"Team": losing_team, "Points": losing_points,
                                                 "Country": losing_country}
        # For the other matches, add the winning team
        else:
            st.session_state.winners[matchup] = {"Team": selected_team,
                                                 "Points": points1 if selected_team == team1 else points2,
                                                 "Country": country1 if selected_team == team1 else country2}

    # Add selected winner/loser teams to the existing teams list
    for winner in st.session_state.winners.values():
        if winner["Team"] not in uecl_teams["Team"]:
            uecl_teams["Team"].append(winner["Team"])
            uecl_teams["Points"].append(winner["Points"])
            uecl_teams["Country"].append(winner["Country"])

    # Create a DataFrame for all teams
    df = pd.DataFrame(uecl_teams)

    # Sort teams by points in descending order
    df_sorted = df.sort_values(by="Points", ascending=False).reset_index(drop=True)

    # Split into 9-team groups
    pot1 = df_sorted.iloc[:6]
    pot2 = df_sorted.iloc[6:12]
    pot3 = df_sorted.iloc[12:18]
    pot4 = df_sorted.iloc[18:24]
    pot5 = df_sorted.iloc[24:30]
    pot6 = df_sorted.iloc[30:]

    # Display the teams in 4 different columns
    st.title("Teams Distribution into Pots")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Pot 1")
        st.dataframe(pot1)

    with col2:
        st.header("Pot 2")
        st.dataframe(pot2)

    with col3:
        st.header("Pot 3")
        st.dataframe(pot3)

    with col1:
        st.header("Pot 4")
        st.dataframe(pot4)

    with col2:
        st.header("Pot 5")
        st.dataframe(pot5)

    with col3:
        st.header("Pot 6")
        st.dataframe(pot6)

    # Selected team and matchups are stored in session_state
    if 'choosen' not in st.session_state:
        st.session_state.choosen = None

    # Team selection
    choosen = st.selectbox(
        "Which team would you like to choose?",
        options=df_sorted["Team"],
        key="team_selectbox"
    )

    # Select 1 team from each pot and apply the alternating home and away pattern
    selected_teams = []

    # List of pots grouped in pairs: [(pot1, pot2), (pot3, pot4), (pot5, pot6)]
    pot_pairs = [(pot1, pot2), (pot3, pot4), (pot5, pot6)]

    for home_pot, away_pot in pot_pairs:
        # Select one team from the home pot
        home_team_candidates = [team for team in home_pot.to_dict('records') if
                                team["Team"] != choosen and team["Country"] !=
                                df_sorted[df_sorted["Team"] == choosen]["Country"].values[0]]
        # Select one team from the away pot
        away_team_candidates = [team for team in away_pot.to_dict('records') if
                                team["Team"] != choosen and team["Country"] !=
                                df_sorted[df_sorted["Team"] == choosen]["Country"].values[0]]

        if home_team_candidates and away_team_candidates:
            home_team = random.choice(home_team_candidates)
            away_team = random.choice(away_team_candidates)
            selected_teams.append((choosen, away_team["Team"]))  # choosen team is home
            selected_teams.append((home_team["Team"], choosen))  # choosen team is away

    # Ensure no three consecutive home or away matches
    final_fixture = []
    random.shuffle(selected_teams)  # Optionally shuffle the final fixture
    for i in range(len(selected_teams)):
        home, away = selected_teams[i]

        # Check the last two matches to avoid three consecutive home or away matches
        if len(final_fixture) >= 2:
            last_home1, last_away1 = final_fixture[-1]
            last_home2, last_away2 = final_fixture[-2]

            if (home == choosen and last_home1 == choosen and last_home2 == choosen) or \
                    (away == choosen and last_away1 == choosen and last_away2 == choosen):
                # Swap the current match with the next one if available
                if i < len(selected_teams) - 1:
                    home, away = selected_teams[i + 1]
                    selected_teams[i + 1] = selected_teams[i]

        final_fixture.append((home, away))

    # Display results
    st.title(f"Fixture for **{choosen}**")
    #random.shuffle(final_fixture)  # Optionally shuffle the final fixture
    for idx, (home, away) in enumerate(final_fixture, start=1):
        home_bold = f"**{home}**" if home == choosen else home
        away_bold = f"**{away}**" if away == choosen else away
        st.write(f"Match {idx}: {home_bold} vs {away_bold}")
