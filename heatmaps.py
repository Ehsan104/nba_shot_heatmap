import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob

# Load the data from multiple CSV files
@st.cache_data
def load_data():
    # Assuming all CSV files are named like 'NBA_2004_Shots.csv', 'NBA_2005_Shots.csv', etc.
    files = glob.glob('NBA_*_Shots.csv')
    data = pd.concat((pd.read_csv(file) for file in files), ignore_index=True)
    return data

# Main function to run the app
def main():
    st.markdown("<h1 style='text-align: center;'>NBA Shot Heatmap</h1>", unsafe_allow_html=True)

    # Load data
    data = load_data()

    # Filter by season
    seasons = data['SEASON_1'].unique()
    selected_season = st.selectbox("Select Season", seasons)

    # Filter data by selected season
    season_data = data[data['SEASON_1'] == selected_season]

    # Filter by player
    players = season_data['PLAYER_NAME'].unique()
    selected_player = st.selectbox("Select Player", players)

    # Filter data by selected player
    player_data = season_data[season_data['PLAYER_NAME'] == selected_player]

    # Calculate statistics
    total_shots = len(player_data)
    three_pt_shots = len(player_data[player_data['SHOT_TYPE'] == '3PT Field Goal'])
    two_pt_shots = len(player_data[player_data['SHOT_TYPE'] == '2PT Field Goal'])

    three_pt_percentage = (three_pt_shots / total_shots) * 100 if total_shots > 0 else 0
    two_pt_percentage = (two_pt_shots / total_shots) * 100 if total_shots > 0 else 0

    # Display statistics
    st.markdown(f"<h3 style='text-align: center;'>Shot Heatmap for {selected_player} in {selected_season}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>3PT Shots: {three_pt_shots} ({three_pt_percentage:.2f}%)</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>2PT Shots: {two_pt_shots} ({two_pt_percentage:.2f}%)</p>", unsafe_allow_html=True)

    plt.figure(figsize=(16, 14))
    court_img = plt.imread('basketball_court.png')  # Ensure you have a basketball court image
    plt.imshow(court_img, extent=[-25, 25, 0, 47])

    sns.kdeplot(
        x=player_data['LOC_X'],
        y=player_data['LOC_Y'],
        shade=True,
        cmap="Blues",
        alpha=0.6
    )

    plt.xlim(-25, 25)
    plt.ylim(0, 47)
    plt.axis('off')
    st.pyplot(plt)

if __name__ == "__main__":
    main()
