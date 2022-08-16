import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from io import BytesIO
import boto3
import time
import logging
from datetime import datetime

hoje = datetime.today().strftime('%Y_%m_%d')

FORMAT = '%(asctime)s - %(message)s'
logging.basicConfig(filename=f'logs/{hoje}.log', format=FORMAT, level=logging.INFO)

logging.info('Iniciado')

class Obmep():

    def __init__(self, url):
        self.url = url

    def parse_html(self):
        logging.info(f'Parse de {self.url} para DataFrame')
        return pd.read_html(self.url)

    def get_origem(self):
        req = requests.get(self.url)
        soup = bs(req.text, features="lxml")

        return soup.find('h1').text

    def transformation(self, nivel):

        df = self.parse_html()[nivel].reset_index(level=None)
        logging.info(f'Iniciando transformacao do DataFrame de {self.url}')

        df.columns = [i[1] for i in df.columns]
        df = df.loc[:, ~df.columns.str.contains('Unnamed')]
        df.loc[:, 'Posicao'] = list(df.index + 1)
        df.loc[:, 'Nivel'] = 'Nivel ' + str(nivel + 1)
        if 'Públicas' in self.get_origem():
            df.loc[:, 'Origem'] = 'Publicas'
        else:
            df.loc[:, 'Origem'] = 'Privada'
        df = df.astype({'Posicao': 'int'})
        return df

    def get_award_table(self):
        return pd.concat([self.transformation(index) for index, value in enumerate(self.parse_html())])

    def save_parquet_s3(self, aws_key, aws_secret_key):

        df = self.get_award_table()
        s3 = boto3.resource('s3',
                            aws_access_key_id=aws_key,
                            aws_secret_access_key=aws_secret_key)

        origem = df.Origem.unique()[0]
        medalha = df.Medalha.unique()[0]
        file_name = f'{origem}_{medalha}.parquet'

        logging.info(f'Convertendo para parquet {file_name}')
        parquet_buffer = BytesIO()
        df.to_parquet(parquet_buffer)

        logging.info(f'Enviando para AWS {self.url}')
        s3.Bucket('1sti-desafio-gabriel-mizuno'). \
            put_object(Key='medalhista/' + file_name, Body=parquet_buffer.getvalue())

class Mencao_honrosa():

    def __init__(self, url):
        self.url = url

    def parse_html(self):
        time.sleep(1.5)
        logging.info(f'Parse de {self.url} para DataFrame')
        return pd.read_html(self.url)

    def get_origem(self):
        req = requests.get(self.url)
        soup = bs(req.text, features="lxml")

        return soup.find('h1').text

    def transformation(self):

        df = self.parse_html()[0].reset_index(level=None)
        logging.info(f'Iniciando transformacao do DataFrame de {self.url}')

        nivel = df.columns[1][0].replace(' ','_')
        df.columns = [i[1] for i in df.columns]
        df = df.loc[:, ~df.columns.str.contains('Unnamed')]
        df.loc[:, 'Posicao'] = list(df.index + 1)
        df.loc[:, 'Nivel'] = nivel
        if 'Públicas' in self.get_origem():
            df.loc[:, 'Origem'] = 'Publicas'
        else:
            df.loc[:, 'Origem'] = 'Privada'
        df = df.astype({'Posicao': 'int'})
        df.rename(columns = {"Menção": "Medalha"}, inplace=True)
        df.replace({'Sim':'Mencao'}, inplace=True)
        return df

    def save_parquet_s3(self, aws_key, aws_secret_key):
        df = self.transformation()
        s3 = boto3.resource('s3',
                            aws_access_key_id=aws_key,
                            aws_secret_access_key=aws_secret_key)

        origem = df.Origem.unique()[0]
        nivel = df.Nivel.unique()[0]
        uf = df.UF.unique()[0]
        file_name = f'{origem}_{uf}_{nivel}.parquet'

        logging.info(f'Convertendo para parquet {file_name}')
        parquet_buffer = BytesIO()
        df.to_parquet(parquet_buffer)

        logging.info(f'Enviando para AWS {self.url}')
        s3.Bucket('1sti-desafio-gabriel-mizuno'). \
            put_object(Key='mencao/' + file_name, Body=parquet_buffer.getvalue())