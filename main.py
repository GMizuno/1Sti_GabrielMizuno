from OBMEP import Obmep, Mencao_honrosa
from decouple import config
from util import get_link

links = ['http://premiacao.obmep.org.br/16aobmep/verRelatorioPremiadosOuro.do.htm',
         'http://premiacao.obmep.org.br/16aobmep/verRelatorioPremiadosPrata.do.htm',
         'http://premiacao.obmep.org.br/16aobmep/verRelatorioPremiadosBronze.do.htm',
         'http://premiacao.obmep.org.br/16aobmep/verRelatorioPremiadosOuro.privada.do.htm',
         'http://premiacao.obmep.org.br/16aobmep/verRelatorioPremiadosPrata.privada.do.htm',
         'http://premiacao.obmep.org.br/16aobmep/verRelatorioPremiadosBronze.privada.do.htm'
         ]
links_mencao = get_link()

[Obmep(link).save_parquet_s3(config('access_key_id'), config('secret_access_key')) for link in links]

[Mencao_honrosa(link).save_parquet_s3(config('access_key_id'), config('secret_access_key')) for link in links_mencao]