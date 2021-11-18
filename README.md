# Desafio 2

## Instalar dependencias
```sh
pip install -r requirements.txt
```
## DOCS
Criação de contêineres `containers/create`
```json
{
  "Image":"alpine"
  "Cmd":"echo Ola"
}
```
\
Inicialização de contêineres URL
```
containers/stats/id_do_container
```
\
Parada de contêineres `containers/stop`
```json
{
  "id":"alpine"
}
```
\
Deleção de contêineres URL
```
containers/id_do_container
```
\
Listar todos os contêineres, com e sem filtros URL
```
containers/
containers/?status=running
containers/?status=restarting
containers/?status=paused
containers/?status=exited
```
\
Criação de redes Docker `networks/create`
```json
{
  "Name":"NomeRede"
}
```
\
Deleção de redes Docker URL
```
networks/id_rede
```
\
Listar todas as redes criadas, com e sem filtros URLs
```
networks/
networks/?driver=bridge
networks/?driver=host
networks/?driver=overlay
networks/?driver=ipvlan
networks/?driver=macvlan
networks/?driver=none
```
\
Pull de imagens `images/create`
```json
{
  "fromImage": "alpine"
}

```
\
Remoção de imagens baixadas URL
```
images/nome_da_imagem
```
\
Listar as imagens baixadas URL
```
images/
```
\
Criação de volumes `volumes/create`
```json
{
"Name":"Nome do volume"
}
```
\
Listagem de volumes URL
```
volumes/
```
\
Deleção de volumes URL
```
volumes/nome_do_volume
```
