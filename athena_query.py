from athena import Athena
from decouple import config
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
from util import result_medal

result = Athena(config('access_key_id'), config('secret_access_key'), "SELECT * FROM obmep").exec_query()

# 1 - Escola com mais medalhas de Ouro

rcParams['figure.figsize'] = 30,30
escola_top = result_medal(result,['escola']).head(5)
sns.barplot(x="escola", y="qtd", data=escola_top)
plt.ylabel('Quantidade', fontsize=20)
plt.xlabel('Escola', fontsize=20)
plt.xticks(fontsize=12,rotation=30)
plt.yticks(fontsize=30)
plt.savefig('img/top_escola_plus.png')
plt.show()

