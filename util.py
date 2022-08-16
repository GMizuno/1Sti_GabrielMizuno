from io import BytesIO
from itertools import product

import boto3
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

class join_parquet_from_s3:

    def __init__(self, aws_key, aws_secret_key, list_folder):
        self.aws_key = aws_key
        self.aws_secret_key = aws_secret_key
        self.list_folder = list_folder

    @property
    def get_all_file(self):
        s3 = boto3.resource('s3',
                            aws_access_key_id=self.aws_key,
                            aws_secret_access_key=self.aws_secret_key)
        bucket = s3.Bucket('1sti-desafio-gabriel-mizuno')

        prefix_df = []
        for folder in self.list_folder:
            prefix_objs = bucket.objects.filter(Prefix=folder)
            for obj in prefix_objs:
                if obj.key.endswith('.parquet'):
                    body = obj.get()['Body'].read()
                    temp = pd.read_parquet(BytesIO(body))
                    prefix_df.append(temp)

        result = pd.concat(prefix_df)

        parquet_buffer = BytesIO()
        result.to_parquet(parquet_buffer)

        s3.Bucket('1sti-desafio-gabriel-mizuno'). \
            put_object(Key='data/arquivo_unico.parquet', Body=parquet_buffer.getvalue())