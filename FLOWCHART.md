# ------------------------------------------------------------
# # Extrair todas as atividades profissionais
# ------------------------------------------------------------

``` python
ap = soup.find_all('atuacao-profissional')
len(ap)

app = ap[5].find_all('atividades-de-participacao-em-projeto')
len(app)
ppe = app[0].find_all('projeto-de-pesquisa')
len(ppe)
ppe[1]
ep = ppe[1].find_all('equipe-do-projeto')
len(ep)
ep[0]
ip = ep[0].find_all('integrantes-do-projeto')
len(ip)
ip[0]
```

# ------------------------------------------------------------
# iniciando funcao para producao tecnica - cursos etc
# ------------------------------------------------------------

```python
# demais-tipos-de-producao-tecnica
dtpt = soup.find_all('demais-tipos-de-producao-tecnica')
len(dtpt)

# curso-de-curta-duracao-ministrado
ccdm = dtpt[0].find_all('curso-de-curta-duracao-ministrado')
len(ccdm)
ccdm[0]

# curso-de-curta-duracao-ministrado AUTORES
ccdm_aut = ccdm[0].find_all('autores')
len(ccdm_aut)
ccdm_aut[0]
```


# ------------------------------------------------------------
# producoes ct do projeto ext
# ------------------------------------------------------------

``` pyhton
# producoes ct do projeto ext
pctp = ppe[1].find_all('producoes-ct-do-projeto')
len(pctp)
pctp[0]

pctp_i = pctp[0].find_all('producao-ct-do-projeto')
len(pctp_i)
pctp_i[0]
```

# ------------------------------------------------------------
# producoes bibliograficas
# ------------------------------------------------------------

```python
# producao bibliografica
pb = soup.find_all('producao-bibliografica')
len(pb)
pb

# artigos publicados
artsper = pb[0].find_all('artigos-publicados')
len(artsper)
artper = artsper[0].find_all('artigo-publicado')
len(artper)
```






