import big_board
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def simulate_n_games(n):
    cols = ['draw', 'o', 'x']
    games_df = pd.DataFrame(0, columns=cols, index=range(n))
    for i in range(n):
        my_board = big_board.BigBoard(3)
        winner = my_board.play_one_random_game()
        games_df.loc[i][winner] = 1
        wins = games_df.mean()
    return wins, games_df

wins, games = simulate_n_games(5)
print(wins)

def simulate_n_games_convergence(n):
    cols = ['draw', 'o', 'x']
    summary_df = pd.DataFrame(columns=cols, index=range(1, n+1))
    for i in range(1, n+1):
        summary_df.loc[i]['draw':'x'], _ = simulate_n_games(n)
        print(str(i) + ' done')
    summary_df.columns = ['draws', 'o wins', 'x wins']
    return summary_df

def plot_convergence(summary_df, filename):
    sns.set()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for col in summary_df.columns:
        ax.plot(summary_df.index, np.array(summary_df.loc[:, col]), label=col)
    ax.legend(loc='best')
    ax.set_ylabel('result percentage')
    ax.set_xlabel('number of games')
    ax.set_title('ultimate kolko i krzyzyk mc convergence')
    fig.savefig(filename)

#summary_5 = simulate_n_games_convergence(5)
#plot_convergence(summary_5, 'mc_5_test')