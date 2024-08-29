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
                 "Stuttgart", "Brest", "Lille OSC", "FC Salzburg", "Dinamo Zagreb", "Red Star Belgrade",
                 "Young Boys", "Slovan Bratislava", "Sparta Praha"],
        "Points": [148, 144, 136, 116, 114, 101, 97, 97, 91, 90, 89, 81, 80, 79, 72, 64, 63, 59, 57, 54.5,
                   54, 32, 24, 20.86, 14.5, 18.056, 17.897, 17.324, 13.366, 47, 50, 50, 40, 34.5, 30.5, 22.5],
        "Country": ["England", "Germany", "Spain", "France", "England",
                    "Italy", "Germany", "Germany", "Spain", "Germany",
                    "Spain", "Italy", "Italy", "Portugal", "England", "Belgium",
                    "Ukraine", "Italy", "Netherlands", "Portugal", "Netherlands",
                    "Scotland", "France", "England", "Austria", "Italy", "Spain",
                    "Germany", "France", "France", "Austria", "Croatia", "Serbia",
                    "Switzerland", "Slovakia", "Czech Republic"]
    }

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
    while True:  # Uygun bir fikstür bulunana kadar denemeye devam et
        final_fixture = []
        random.shuffle(selected_teams)  # Takımları karıştır
        valid_fixture = True  # Fikstürün geçerliliğini kontrol etmek için bayrak

        for i in range(len(selected_teams)):
            home, away = selected_teams[i]

            # Son iki maçı kontrol et; ardışık üç ev sahibi veya deplasman maçı olmamalı
            if len(final_fixture) >= 2:
                last_home1, last_away1 = final_fixture[-1]
                last_home2, last_away2 = final_fixture[-2]

                if (home == choosen and last_home1 == choosen and last_home2 == choosen) or \
                        (away == choosen and last_away1 == choosen and last_away2 == choosen):

                        # Uygun bir değişiklik yoksa fikstürü geçersiz yap ve yeniden karıştır
                    valid_fixture = False
                    break  # İç döngüden çık ve baştan başla

            final_fixture.append((home, away))

        if valid_fixture:
            # Eğer geçerli bir fikstürse döngüden çık
            break

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
                 "A. Bilbao", "Slavia Praha", "Dynamo Kyiv","Qarabag FK","Bodø/Glimt","Galatasaray",
                 "FC Midtjylland","Malmö FF","Ajax","Sporting Braga","PAOK Thessaloniki","FCSB","Maccabi Tel-Aviv",
                 "Ferencváros","IF Elfsborg","Viktoria Plzeň","Ludogorets Razgrad","RFS Riga","Anderlecht","Beşiktaş",],
        "Points": [101, 92, 77, 63, 60, 54, 54, 51, 50, 48, 44, 36, 27, 17.324, 17, 12.26, 17.897, 53, 26.5,
                   33, 28, 31.5, 25.5, 18.5, 67, 49, 37, 10.5, 35.5, 35, 4.3, 28, 26, 8, 14.5, 12],
        "Country": ["Italy", "England", "Portugal", "Scotland", "Germany", "Italy", "England", "Spain", "Netherlands",
                    "Greece", "France", "Turkey", "Belgium", "Germany", "France", "Netherlands", "Spain",
                    "Czech Republic", "Ukraine","Azerbaijan", "Norway","Turkey","Denmark","Sweden","Netherlands",
                    "Portugal", "Greece","Romania","Israel", "Hungary", "Sweden", "Czech Republic", "Bulgaria",
                    "Latvia", "Belgium", "Turkey"]
    }

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
    #final_fixture = []

    while True:  # Uygun bir fikstür bulunana kadar denemeye devam et
        final_fixture = []
        random.shuffle(selected_teams)  # Takımları karıştır
        valid_fixture = True  # Fikstürün geçerliliğini kontrol etmek için bayrak

        for i in range(len(selected_teams)):
            home, away = selected_teams[i]

            # Son iki maçı kontrol et; ardışık üç ev sahibi veya deplasman maçı olmamalı
            if len(final_fixture) >= 2:
                last_home1, last_away1 = final_fixture[-1]
                last_home2, last_away2 = final_fixture[-2]

                if (home == choosen and last_home1 == choosen and last_home2 == choosen) or \
                        (away == choosen and last_away1 == choosen and last_away2 == choosen):

                        # Uygun bir değişiklik yoksa fikstürü geçersiz yap ve yeniden karıştır
                    valid_fixture = False
                    break  # İç döngüden çık ve baştan başla

            final_fixture.append((home, away))

        if valid_fixture:
            # Eğer geçerli bir fikstürse döngüden çık
            break

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
        "Team": [
            "Istanbul Başakşehir", "AA Gent", "Jagiellonia Białystok", "Rapid Wien", "Shamrock Rovers", "LASK",
            "TSC Bačka Topola", "Borac Banja Luka", "Molde FK", "Hearts", "Petrocub Hîncesti", "APOEL Nicosia",
            "Dinamo Minsk", "FC Lugano", "Chelsea", "FC København", "Fiorentina", "Pafos", "Real Betis", "Legia Warsaw",
            "Heidenheim", "Djurgårdens IF", "Panathinaikos", "Olimpija Ljubljana", "Omonia Nicosia", "HJK Helsinki",
            "FC St Gallen", "Vitória Guimarães", "FK Astana", "Cercle Brugge", "Larne FC", "The New Saints", "NK Celje",
            "Mladá Boleslav", "Vikingur Reykjavik", "FC Noah"
        ],
        "Points": [
            29, 45, 5.075, 14, 9.5, 37, 5.555, 5.5, 28.5, 7.21, 7, 14.5, 4.5, 8, 96, 51.5, 42, 4.42, 33, 18,
            17.324, 16.5, 6.305, 10.5, 12, 11.5, 6.595, 11.263, 11, 9.76, 4.5, 8.5, 4.5, 7.21, 4, 2.125
        ],
        "Country": [
            "Turkey", "Belgium", "Poland", "Austria", "Ireland", "Austria", "Serbia", "Bosnia and Herzegovina",
            "Norway",
            "Scotland", "Moldova", "Cyprus", "Belarus", "Switzerland", "England", "Denmark", "Italy", "Spain", "Cyprus",
            "Poland", "Germany", "Sweden", "Greece", "Slovenia", "Cyprus", "Finland", "Switzerland", "Portugal",
            "Kazakhstan", "Belgium", "Northern Ireland", "Wales", "Slovenia", "Czech Republic", "Iceland", "Armenia"
        ]
    }

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
