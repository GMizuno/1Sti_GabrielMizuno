from athena import Athena
from decouple import config
import seaborn as sns
import matplotlib.pyplot as plt

result = Athena(config('access_key_id'), config('secret_access_key'), "SELECT * FROM obmep").exec_query()
ouro = result[result['medalha'] == 'Ouro']
prata = result[result['medalha'] == 'Prata']
bronze = result[result['medalha'] == 'Bronze']

# Medalhas por origem
sns.countplot(x='uf',data=result, hue='origem', order=result['uf'].value_counts().index)
plt.show()

# Distribuicao medalhas Escola
sns.countplot(x='medalha',data=result, hue='origem', order=result['medalha'].value_counts().index)
plt.show()

# Medalhas de ouro por estado
sns.countplot(x='uf',data=ouro, hue='origem', order=ouro['uf'].value_counts().index)
plt.show()

# Medalhas de prata por estado
sns.countplot(x='uf',data=prata, hue='origem', order=prata['uf'].value_counts().index)
plt.show()

# Medalhas de bronze por estado
sns.countplot(x='uf',data=bronze, hue='origem', order=bronze['uf'].value_counts().index)
plt.show()

# Escolas com mais medalhas
escola_medalhas = result.\
    groupby(['escola', 'medalha'], as_index=False)['nome'].\
    count().\
    reset_index().\
    rename(columns={'nome':'qtd'}).\
    sort_values(by='qtd', ascending=False)

top20_escolas_ouro = escola_medalhas[escola_medalhas['medalha']=='Ouro'].head(20)
top20_escolas_ouro

top20_escolas_prata = escola_medalhas[escola_medalhas['medalha']=='Prata'].head(20)
top20_escolas_prata

top20_escolas_bronze = escola_medalhas[escola_medalhas['medalha']=='Bronze'].head(20)
top20_escolas_bronze