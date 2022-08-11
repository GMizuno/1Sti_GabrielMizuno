CREATE EXTERNAL TABLE IF NOT EXISTS `obmep`.`obmep` ( `Nome` string, `Escola` string,
  `Tipo` string,
  `Município` string,
  `UF` string,
  `Posicao` int,
  `Nivel` string,
  `Origem` string,
  `Medalha` string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' WITH SERDEPROPERTIES ( 'serialization.format' = '1'
) LOCATION 's3://1sti-desafio-gabriel-mizuno/data/'
TBLPROPERTIES ('has_encrypted_data'='false');

select * from obmep;