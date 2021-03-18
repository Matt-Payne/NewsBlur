import pandas as pd
from pandas import DataFrame
import ast

# table_name ex: FeedData
# columns is list of columns from the table ['popular_tags', 'feed']
def get_df_from_database(table_name, columns):
    return DataFrame(list(table_name.objects.values(columns)))


# list of dataframes to combine
def combine_table_dfs_together(dfs):
    if len(dfs) > 1:
        main = dfs.pop(0)
        for df in dfs:
            for column in df:
                main[column] = df[column]
        return main
    return dfs.pop(0)

#get user ids + feeds they subscribe to
df = get_df_from_database('UserSubscription', ['user','feed_id'])



df = DataFrame(list(UserSubscription.objects.values('user','feed_id')))

# add a followed_feed column, all will be 1 for now but we will add negatives later
df.loc[:, 'is_following_feed'] = 1



#map = dict(zip(categories.feed_id, categories.feed_id))

#create df of feed_id and popular_tags

ids = list(FeedData.objects.values('feed'))
input = list(FeedData.objects.values('popular_tags'))


df = pd.DataFrame(columns=['feed_id','popular_tags'])
df['feed_id'] = ids
df['popular_tags'] = input
#df['feed_id'] = [ast.literal_eval(x) for x in feed]
# popular_tags comes in as a string looking like a list, can convert to real list with:
import ast
ast.literal_eval(df['popular_tags'][0])
