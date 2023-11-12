# Safe Beach Data

Este repositório contém os scripts e arquivos de dados utilizados no projeto Praia Segura. A intenção do projeto Praia Segura é conseguir estimar o risco de incidentes com tubarões e afogamentos em praias, principalmente nas praias que já têm histórico dessas ocorrências.

A partir da coleta e processamento de dados históricos de incidentes com tubarões, dados meteorológicos, dados de maré e as coordenadas geográficas de postos de guarda-vidas, é possível estimar a ocorrência de incidentes com tubarões e afogamentos nas praias da região metropolitana do Recife (RMR).

## Fontes de dados

Os dados históricos sobre incidentes com tubarões na RMR foram coletados do Comitê Estadual de Monitoramento de Incidentes com Tubarões (Cemit) (https://semas.pe.gov.br/cemit/).

Os dados meteorológicos históricos foram coletados da Open-Meteo, um serviço de APIs climáticas e de localização. A coleta de dados foi feita usando a API Historical Weather (https://open-meteo.com/en/docs/historical-weather-api)

Os dados de maré foram coletados através dos PDFs disponibilizados no portal oficial da Marinha (https://www.marinha.mil.br/chm/tabuas-de-mare)

As coordenadas geográficas dos postos de guarda-vidas foram disponibilizadas pelo Corpo de Bombeiros de Pernambuco.

## Insights

Nota-se que os incidentes com tubarões e afogamentos são relacionados ao nível de maré. Quanto mais alta a maré, maior a chance de um incidente com tubarão, isso porque durante a maré alta, a vida marinha fica mais agitada. Além disso, as correntes de retorno ficam mais fortes, podendo arrastar pessoas para mar aberto mais rapidamente.
