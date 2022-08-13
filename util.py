from itertools import product
import pandas as pd
from typing import List

lista_estados = ["AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "AC", "PA", "PB", "PE", "PI",
                 "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"]


def get_public_url():
    final = list(product(lista_estados, ['1', '2', '3']))

    return ['http://premiacao.obmep.org.br/16aobmep/verRelatorioPremiadosMencao-' + i[0] + '.' + i[1] + '.do.htm' for i
            in final]


def get_private_url():
    final = list(product(lista_estados, ['1', '2', '3']))

    return [
        'http://premiacao.obmep.org.br/16aobmep/verRelatorioPremiadosMencao-' + i[0] + '.' + i[1] + '.privada.do.htm'
        for i
        in final]


def get_link():
    return get_public_url() + get_private_url()


def result_medal(dataframe: pd.DataFrame, group:List, ascending:bool = False):
    return dataframe. \
        groupby(group). \
        agg(qtd=('nome', 'count')). \
        reset_index().sort_values(by='qtd',ascending=ascending)
