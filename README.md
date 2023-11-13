# Safe Beach Data

Este repositório contém os scripts e arquivos de dados utilizados no projeto Praia Segura. A intenção do projeto Praia Segura é conseguir estimar o risco de incidentes com tubarões e afogamentos em praias, principalmente nas praias que já têm histórico dessas ocorrências.

A partir da coleta e processamento de dados históricos de incidentes com tubarões, dados meteorológicos, dados de maré e as coordenadas geográficas de postos de guarda-vidas, é possível estimar a ocorrência de incidentes com tubarões e afogamentos nas praias da região metropolitana do Recife (RMR).

## Fontes de dados

Os dados históricos sobre incidentes com tubarões na RMR foram coletados do Comitê Estadual de Monitoramento de Incidentes com Tubarões (Cemit) (https://semas.pe.gov.br/cemit/).

Os dados meteorológicos históricos foram coletados através da Open-Meteo, um serviço de APIs climáticas e de localização. A coleta de dados foi feita usando a Historical Weather API (https://open-meteo.com/en/docs/historical-weather-api)

Os dados de maré foram coletados através de PDFs disponibilizados no portal oficial do Centro de Hidrografia da Marinha (https://www.marinha.mil.br/chm/tabuas-de-mare).

As coordenadas geográficas dos postos de guarda-vidas e os polígonos de áreas protegidas por recifes foram disponibilizados pelo Corpo de Bombeiros de Pernambuco.

## Insights

- Nota-se que os incidentes com tubarões e afogamentos são relacionados ao nível de maré. Quanto mais alta a maré, maior a chance de um incidente com tubarão, isso porque durante a maré alta, a vida marinha fica mais agitada. Além disso, as correntes de retorno ficam mais fortes, podendo arrastar pessoas para mar aberto mais rapidamente;
- A presença de recifes formando uma barreira protetora diminui a ocorrência de incidentes com tubarões, principalmente se o nível da maré estiver baixo (baixa-mar ou maré morta);
- A turvidez da água pode ser um fator que corrobore para incidentes com tubarões. Essa turvidez por si só vai depender de uma série de fatores, entre eles, a presença de chuvas no dia do incidente ou no dia anterior ao incidente;
  - A turvidez da água também vai depender da quantidade de partículas flutuantes na água, isso é influenciado também pela presença de desembocaduras de rios na região.


## Objetivos

- Conseguir estimar a probabilidade de uma nova ocorrência de incidente com tubarão ou afogamento;
- Determinar o quão impactante cada fator (maré, presença de recifes, presença de postos guarda-vidas) é para a materialização de incidentes, seja afogamento ou incidentes com tubarões.
