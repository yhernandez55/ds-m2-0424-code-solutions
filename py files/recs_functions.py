# creating a function that takes user index and the datasets 
# and returns 5 movie recs based on popularity

import pandas as pd

# reading the files:
def read_data():
    movie = pd.read_csv('u.item', encoding='latin1', delimiter='|', header=None, usecols=[0,1,2], names=['movie_id', 'name', 'date'])
    rating = pd.read_csv('u.data', header=None, delimiter='\t', names=['user_id','movie_id', 'ratings', 'time'])
    u_user = pd.read_csv('u.user', delimiter='|', header=None)
    return movie, rating, u_user

# popular movies user based
def pop_5_movie_rec_user_based(rating, movie, df, um, usermovies, popularmovies):
    df = rating.merge(movie, on=['movie_id'], how='inner')
    df.groupby('name')['ratings'].sum().sort_values(ascending=False).head(10)
    um = df.pivot_table(index='user_id', columns=['name'], values='ratings')
    usermovies = um.loc[1].dropna()
    usermovies.index
    # um['Star Wars (1977)'].dropna()
    popularmovies = df.groupby('name').agg({'ratings': ['mean', 'count', 'sum']}).sort_values(by=('ratings', 'count'), ascending=False)
    set(popularmovies.index) - set(usermovies.index) 
    df.sort_values(by=['user_id', 'time']).head(20)
    df.sort_values(by=['user_id', 'time'],inplace=True)
    df.head(5)
    # popularmovies = popularmovies[popularmovies['ratings']['count'] >= 100]
    # popularmovies = pd.DataFrame(popularmovies)
    # popularmovies = pd.DataFrame(popularmovies).reset_index()
    # popularmovies.columns = ['name', 'mean', 'count', 'sum']
    return df


# similar movies item based:
def sim_5_movie_rec_item_based(rating, movie, df, um, corrmatrix, user2ratings, simovies, sims, final_recomentation):
    df = rating.merge(movie, on=['movie_id'], how='inner')
    df.groupby('name')['ratings'].sum().sort_values(ascending=False).head(10)

    um = df.pivot_table(index='user_id', columns=['name'], values='ratings')
    corrmatrix = um.corr(min_periods=100)

    user2ratings = um.loc[2].dropna()  # Ratings of user 2
    simovies = pd.Series(dtype='float64')  # Initialize an empty Series

    # we turned it into a series bc 
    # the series has an indx and val while a list doesn't
    # and that is what we wanted. 
    # We use concat instead of merge for a series

    for i in range(len(user2ratings)):
        print("Similar movies to {}".format(user2ratings.index[i]))
        sims = corrmatrix[user2ratings.index[i]].dropna()
        simovies = pd.concat([simovies, sims])

    final_recomentation = simovies.groupby(simovies.index).count().sort_values(ascending=False)
    
    # Ensure we exclude movies the user has already rated
    final_recomentation = final_recomentation.drop(user2ratings.index, errors='ignore')

    # Return only the top 5 recommendations
    final_recomentation = final_recomentation.sort_values(ascending=False).head(5)
    
    return final_recomentation
    
    
