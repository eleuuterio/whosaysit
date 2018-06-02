# Usando as credenciais  OAuth para autorizar o querys no Twitter API

import twitter
import json
from urllib.parse import unquote
import json

CONSUMER_KEY = ''
CONSUMER_SECRET =''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

# procurando Twitter que tem a palavra colocada em q

q = input('Digite Hashtag a procurar: ')

count = 100

search_results = twitter_api.search.tweets(q=q, count=count)

statuses = search_results['statuses']

for _ in range(5):
    print ('Length of statuses', len(statuses))
    try:
     next_results = search_results['search_metadata']['refresh_url']
    except:
     break
kwargs = dict([ kv.split('=') for kv in unquote(next_results[1:]).split('&') ])

search_results = twitter_api.search.tweets(**kwargs)

statuses += search_results['statuses']

# mostrar so o priemiro tweet que a pessoa enviou por tem muitos dados sobre (metadata)
#print (json.dumps(statuses[0], indent=1))

status_texts = [ status['text'] for status in statuses ]

screen_names = [ user_mention['screen_name'] for status in statuses for user_mention in status['entities']['user_mentions'] ]

hashtags = [ hashtag['text'] for status in statuses for hashtag in status['entities']['hashtags'] ]

# Computando uma colecao de todas as palavras de todos os tweets
words = [ w for t in status_texts for w in t.split() ]

# Vendo os primeiros 5 itens de cada
#print (json.dumps(status_texts[0:5], indent=1))
#print (json.dumps(screen_names[0:5], indent=1))
#print (json.dumps(hashtags[0:5], indent=1))
#print (json.dumps(words[0:5], indent=1))

# Contando o numero de palavras, usuarios e hashtags usadas

from collections import Counter
for item in [words, screen_names, hashtags]:
    c = Counter(item)
    #print (c.most_common()[:10])  # top 10 de cada um

#Colocando todos encontrados em uma tabela bonita

from prettytable import PrettyTable

for label, data in (('Palavras', words),('Usuario', screen_names),('Hashtag', hashtags)):
    pt = PrettyTable(field_names=[label, 'Quantidade'])
    c = Counter(data)
    [ pt.add_row(kv) for kv in c.most_common()]
    pt.align[label], pt.align['Quantidade'] = 'l', 'r'

    print(pt)
