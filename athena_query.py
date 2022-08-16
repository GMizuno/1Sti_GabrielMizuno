from athena import Athena
from decouple import config
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
from util import result_medal

result = Athena(config('access_key_id'), config('secret_access_key'), "SELECT * FROM obmep").exec_query()

# 1 - Escola com mais medalhas

rcParams['figure.figsize'] = 30, 30
escola_top = result_medal(result, ['escola']).head(5)
sns.barplot(x="escola", y="qtd", data=escola_top)
plt.ylabel('Quantidade', fontsize=30)
plt.xlabel('Escola', fontsize=30)
plt.xticks(fontsize=20, rotation=30)
plt.yticks(fontsize=30)
plt.savefig('img/top_escola_plus.png')
plt.show()

# 2 -

rcParams['figure.figsize'] = 30, 30
uf_top = result_medal(result, ['uf']).head(10)
sns.barplot(x="uf", y="qtd", data=uf_top)
plt.ylabel('Quantidade', fontsize=30)
plt.xlabel('Estado', fontsize=30)
plt.xticks(fontsize=20, rotation=30)
plt.yticks(fontsize=30)
plt.savefig('img/top_estado_plus.png')
plt.show()

# 3 -

rcParams['figure.figsize'] = 30, 30
cidade_top = result_medal(result, ['município']).head(10)
sns.barplot(x="município", y="qtd", data=cidade_top)
plt.ylabel('Quantidade', fontsize=30)
plt.xlabel('Cidade', fontsize=30)
plt.xticks(fontsize=20, rotation=30)
plt.yticks(fontsize=30)
plt.savefig('img/top_cidade_plus.png')
plt.show()

# 4 -

rcParams['figure.figsize'] = 10, 8
medalha_origem = result_medal(result, ['medalha', 'origem'])
medalha_origem['%'] = 100 * medalha_origem['qtd'] / \
                      medalha_origem.groupby(['origem'])['qtd'].\
                          transform('sum')

sns.barplot(x="medalha", y="qtd", data=medalha_origem, hue='origem')
plt.ylabel('Quantidade')
plt.xlabel('Medalha')
plt.savefig('img/medalha_origem_plus.png')
plt.show()

rcParams['figure.figsize'] = 10, 8
sns.barplot(x="medalha", y="%", data=medalha_origem, hue='origem')
plt.ylabel('Propoção')
plt.xlabel('Medalha')
plt.savefig('img/medalha_origem_proporcao_plus.png')
plt.show()
