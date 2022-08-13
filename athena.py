import boto3
import time
import pandas as pd


class Athena():

    def __init__(self, aws_key, aws_secret_key, query):
        self.aws_key = aws_key,
        self.aws_secret_key = aws_secret_key,
        self.query = query

    def exec_query(self):
        client = boto3.client('athena',
                              region_name = 'us-east-1',
                              aws_access_key_id=self.aws_key[0],
                              aws_secret_access_key=self.aws_secret_key[0])

        queryStart = client.start_query_execution(
            QueryString=self.query,
            QueryExecutionContext={
                'Database': 'obmep'
            },
            ResultConfiguration={'OutputLocation': 's3://1sti-desafio-gabriel-mizuno/results'}
        )
        queryExecutionId = queryStart['QueryExecutionId']
        time.sleep(4)

        rows = []

        client.get_query_results(QueryExecutionId=queryStart['QueryExecutionId'])
        paginator = client.get_paginator('get_query_results')
        query_results = paginator.paginate(
            QueryExecutionId=queryExecutionId,
            PaginationConfig={'PageSize': 1000}
        )
        for page in query_results:
            for row in page['ResultSet']['Rows']:
                rows.append(row['Data'])

        columns = rows[0]
        rows = rows[1:]

        columns_list = []
        for column in columns:
            columns_list.append(column['VarCharValue'])

        dataframe = pd.DataFrame(columns=columns_list)

        for row in rows:
            df_row = []
            for data in row:
                df_row.append(data['VarCharValue'])
            dataframe.loc[len(dataframe)] = df_row

        return dataframe
