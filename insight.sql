-- Quais são as escolas públicas e privadas com o maior número de medalhistas?
select escola, origem, count(*) as num_medalista
from obmep
where medalha in ('Ouro', 'Prata', 'Bronze')
group by escola, origem
order by num_medalista desc

select escola, count(*) as num_medalista
from obmep
where origem = 'Publicas' and medalha in ('Ouro', 'Prata', 'Bronze')
group by escola
order by num_medalista
desc

select escola, count(*) as num_medalista
from obmep
where origem = 'Privada' and medalha in ('Ouro', 'Prata', 'Bronze')
group by escola
order by num_medalista
desc

-- Quais são os estados com o maior número de medalhistas?
select uf, count(*) as num_medalista
from obmep
where medalha in ('Ouro', 'Prata', 'Bronze')
group by uf
order by num_medalista desc

-- Quais são as cidades com o maior número de medalhistas?
select "município", count(*) as num_medalista
from obmep
where medalha in ('Ouro', 'Prata', 'Bronze')
group by "município"
order by num_medalista desc
