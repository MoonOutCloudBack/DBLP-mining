import pandas as pd
import time
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules

# data = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
'''
python fpgrowth.py
'''

split_str = ' ||| '
min_sup = 5
min_con = 0.5
alpha = 1
beta = 10

def loadData():
    dataset = {i:[] for i in range(2017, 2023)}
    with open('./authors_encoded.txt', 'r') as encode:
        for line in encode:
            words = line.split(split_str)
            length = len(words) - 1
            dataLine = [int(words[i]) for i in range(2, length)]
            dataset[int(words[0])].append(dataLine)
    return dataset

def readAuthorIndex():
    author_dict = {}
    with open('./authors_index.txt', 'r') as authors_index:
        for name in authors_index:
            name = name.strip().split(split_str)
            if len(name) != 3: continue
            author_dict[int(name[0])] = [name[1], name[2]]
    return author_dict


if __name__ == '__main__':

    print('loading the dataset...')
    dataset = loadData()
    author_dict = readAuthorIndex()

    print('change the format to one-hot...')
    df = {}
    te_len = {}
    co_authors = {}
    teams = {}
    for year in range(2017, 2023):
        data = dataset[year]
        te = TransactionEncoder()
        te_ary = te.fit(data).transform(data)
        df[year] = pd.DataFrame(te_ary, columns=te.columns_)
        te_len[year] = te_ary.shape[0]

    print('get co-authors & teams...')
    df_co_authors = pd.DataFrame(columns=['year', 'authors', 'papers', 'active'])
    df_teams = pd.DataFrame(columns=['year', 'authors', 'papers', 'active'])

    for year in range(2017, 2023):
        # get frequent itemsets
        frequent_itemsets = fpgrowth(df[year], min_support = min_sup/te_len[year], use_colnames=True)
        # get rules
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_con)

        co_authors = frequent_itemsets[frequent_itemsets.itemsets.apply(lambda x: len(x)) == 2]
        teams = frequent_itemsets[frequent_itemsets.itemsets.apply(lambda x: len(x)) > 2]
        co_authors_set = set([tuple(fs) for fs in co_authors['itemsets']])
        teams_set = set([tuple(fs) for fs in teams['itemsets']])

        rules_set = set([
            (tuple(fs[0]), tuple(fs[1])) for fs in 
                zip(rules['antecedents'].tolist(), rules['consequents'].tolist())
        ])

        # remove not confident relationships
        for rel in co_authors_set:
            stay = True
            for i in range(2):
                ok = False
                for rule in rules_set:
                    if rel[0:1] == rule[0] and rel[1:2] == rule[1]:
                        ok = True
                        break
                if not ok:
                    stay = False
                    break
            if not stay:
                co_authors = co_authors[co_authors.itemsets.apply(lambda x: tuple(x)) != rel]
        for rel in teams_set:
            stay = True
            for i in range(len(rel)):
                ok = False
                for rule in rules_set:
                    if rel[:i] + rel[i+1:] == rule[0] and (rel[i],) == rule[1]:
                        ok = True
                        break
                if not ok:
                    stay = False
                    break
            if not stay:
                teams = teams[teams.itemsets.apply(lambda x: tuple(x)) != rel]

        # write df
        for encode_lists in co_authors['itemsets']:
            authors = []
            active = 0.0
            # get author name and active/group_papers
            for encode in encode_lists:
                authors.append(author_dict[encode][0])
                active += 1/int(author_dict[encode][1])
            active += alpha + beta / len(authors)
            authors = tuple(authors)
            # get group_papers
            for index, rows in co_authors.iterrows():
                if encode_lists == rows['itemsets']:
                    papers = int(float(rows['support']) * te_len[year])
                    active *= papers
                    break
            df_co_authors.loc[len(df_co_authors)] = [year, authors, papers, active]
        for encode_lists in teams['itemsets']:
            authors = []
            active = 0.0
            # get author name and active/group_papers
            for encode in encode_lists:
                authors.append(author_dict[encode][0])
                active += 1/int(author_dict[encode][1])
            active += alpha + beta / len(authors)
            authors = tuple(authors)
            # get group_papers
            for index, rows in teams.iterrows():
                if encode_lists == rows['itemsets']:
                    papers = int(float(rows['support']) * te_len[year])
                    active *= papers
                    break
            df_teams.loc[len(df_teams)] = [year, authors, papers, active]

    print("Writing result into csv...")
    df_co_authors.to_csv(
        './result_co_authors_' + str(min_sup) + '_' + str(min_con) + '.csv',
        index=False
    )
    df_teams.to_csv(
        './result_teams_' + str(min_sup) + '_' + str(min_con) + '.csv',
        index=False
    )
