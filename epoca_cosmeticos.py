## Criado com Python 3.4.3
##############################################
##############################################
########### Importações

# Funções necessárias:
import web_scrap_func as webF

##############################################
##############################################
#
#
#
#
#
##############################################
##############################################
########### Pesquisas no site

'''
Partindo dos seguintes pressupostos:
1 - Não há produto sem marca.
2 - Não há produto duplicado nas marcas.
4 - Não há produto com mais de uma marca.
3 - Não há marca sem produto.

Coletou-se os links dos produtos através das
páginas de suas respectivas marcas.
Posteriormente os dados foram conferidos para 
verificar duplicatas e estas foram inexistentes.
'''

# Link principal pesquisado, contém todas as marcas:
pagina_str = webF.abrir_pagina("http://www.epocacosmeticos.com.br/marcas")

# Captura todos os links das marcas: 
listas_de_marcas = webF.extrair_meio(pagina_str, '<h3>Marcas</h3><ul>', '</ul>')

# Só deve haver um elemento em listas_de_marcas. Se houver mais de um
# o programa deve ser parado para checagem, pois o site foi modificado.
assert len(listas_de_marcas) == 1, "Há mais de uma lista de marcas na página."
links = webF.extrair_meio(listas_de_marcas[0], '<li><a href="','"')


##############################################
##############################################
#
#
#
#
#
##############################################
##############################################
########### Acessando as marcas

links_produtos = []

# Abre o Chrome:
browser = webF.abrir_chrome()

# Botão de mais produtos que aparece em algumas páginas:
mais_prod = "//div[@class='btn-load-more confira-todos-produtos']"


for contador in range(0, len(links)):

    # Abre a página no navegador:
    webF.abrir_pagina_nav(browser, links[contador])

    # Caso a página da marca tenha um botão para mais produtos, o aciona:
    webF.clicar_botao(browser, mais_prod)

    html_source = browser.page_source 

    informacoes_produtos = webF.extrair_meio(html_source, '<h3><a title=','</a>')

    # Se não houver nenhum produto na página da marca, interrompe o programa para
    # checagem, pois deve ter capturado dados indevidos ou a estrutura do site mudou:
    assert len(informacoes_produtos) >= 1, "Página sem nenhum produto."


    for informacao in informacoes_produtos:
        link_produto = ''
        
        try:
            # Endereço do produto:
            link_produto = webF.extrair_meio(informacao, 'href="','"')[0]
        except Exception: 
            pass	# Não encontrou endereço.

        # Se for realmente um link válido de produto, adiciona aos links totais:
        if (link_produto.endswith('/p')):
            links_produtos.append(link_produto)


# Fecha o Chrome:
webF.fechar_navegador(browser)


##############################################
##############################################
#
#
#
#
#
##############################################
##############################################
########### Acessando os produtos

# Escreve os resultados limpos num arquivo CSV.
with open("produtos.csv", "w", encoding='utf-8') as outfile:
    
    # Primeira linha do arquivo, nomes das variáveis:
    outfile.write('nome,titulo,link,\n')
    
    # Agora, para cada produto, acessa a página e captura o conteúdo.
    for contador in range(0, len(links_produtos)):

        paginaP_str = webF.abrir_pagina(links_produtos[contador], True)
        
        try:
            # Nome do produto:
            div_nome = webF.extrair_meio(paginaP_str, '<h1 itemprop="name">','/div>')[0]
            outfile.write('"' + webF.extrair_meio(div_nome, '>','<')[0] + '"')
        except Exception: 
            pass    # Não encontrou nome.
        outfile.write(',')

        try:
            # Título da página:
            outfile.write('"' + webF.extrair_meio(paginaP_str, '<title>','</title>')[0] + '"')
        except Exception: 
            pass    # Não encontrou title.
        outfile.write(',')

        # Endereço do produto:
        outfile.write(links_produtos[contador] + ',\n')


# Fim do programa, fecha o arquivo aberto:
outfile.close()

