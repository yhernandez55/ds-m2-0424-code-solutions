import pandas as pd
# popular movies user based
# reading the files:
def read_data():
    rating = pd.read_csv('BX-Book-Ratings.csv',encoding='unicode_escape',  sep=';', on_bad_lines='skip')
    Books = pd.read_csv('BX_Books.csv', encoding='unicode_escape',  sep=';', on_bad_lines='skip')
    return rating, Books

# popular books user based
def pop_5_book_rec_user_based(rating, Books):
    df = rating.merge(Books, on=['ISBN'], how='inner')
    df.drop(['Image-URL-S', 'Image-URL-M', 'Image-URL-L'], axis=1)
    df.dropna()
    df.groupby('Book-Title')['Book-Rating'].sum().sort_values(ascending=False).head(10)
    df = df.iloc[:10000]
    um = df.pivot_table(index='ISBN', columns=['Book-Title'], values='Book-Rating')
    userbooks = um.iloc[1].dropna().index
    popularbooks = df.groupby('Book-Title').agg({'Book-Rating': ['mean', 'count', 'sum']}).sort_values(by=('Book-Rating', 'count'), ascending=False)
    popularbooks = popularbooks.drop(userbooks)
    return popularbooks


def sim_5_books_rec_item_based(rating, Books):
    df = rating.merge(Books, on=['ISBN'], how='inner')
    df.drop(['Image-URL-S', 'Image-URL-M', 'Image-URL-L'], axis=1)
    top_5000 = df.groupby('Book-Title')['Book-Rating'].sum().sort_values(ascending=False).head(5000)
    df = df[df['Book-Title'].isin(top_5000.index)] 
    um = df.pivot_table(index='User-ID', columns=['Book-Title'], values='Book-Rating')
    um['The Da Vinci Code'].dropna(inplace=True)
    corrmatrix = um.corr()
    corr_da_vinci = corrmatrix['The Da Vinci Code'].dropna()
    um[['The Lovely Bones: A Novel', 'The Da Vinci Code']].corr()
    user2ratings = um.iloc[2].dropna()
    simbooks = pd.Series()
    
    for i in range(len(user2ratings)):
        sims = corrmatrix[user2ratings.index[i]].dropna()
        simbooks = pd.concat([simbooks, sims])
    final_recommendation = simbooks.groupby(simbooks.index).count().sort_values(ascending=False)
    final_recommendation = final_recommendation.drop(user2ratings.index, errors='ignore')
    recommended_books = final_recommendation.head(10)
    return recommended_books

# svd 