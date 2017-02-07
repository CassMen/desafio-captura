## Criado com Python 3.4.3
##############################################
##############################################
########### Importações

import urllib.error as error
import urllib.request as URL
import urllib.parse as parse

import html

import time

# Navegador:
from selenium import webdriver

##############################################
##############################################
#
#
#
#
#
##############################################
##############################################
########### Funções

def extrair_meio(texto, inicio, fim):
    """ Extrai uma palavra ou grupo de palavras de uma string (texto).
    As palavras devem estar cercadas pelos mesmos caracteres
    (inicio e fim).
    Retorna uma lista com todas as palavras extraídas.

    Exemplo:
    >>> texto = "aiweyiq67hello aba29099du0267world aba2u3"
    >>> extrair_meio(texto, "67", " aba")
    ['hello','world']
    """
    
    resultado=[]

    # Primeira partição, removendo o início, que é o texto antes
    # de chegar no que se quer.
    sem_inicio = texto.split(inicio)[1:]

    # Para cada elemento de sem_inicio, faz a segunda partição.
    # O sem_fim[1] é texto indesejado.
    for parte_texto in sem_inicio:
        sem_fim = parte_texto.split(fim)
        resultado.append(sem_fim[0])

    return resultado


def decode_unicodeURL(url):
    """ Retorna uma URL que contenha caracteres legíveis para o
    programa a partir de uma que contenha unicode.

    Exemplo:
    >>> url = "http://www.exemplo.com/LâmpadaDosBêbados"
    >>> decode_unicodeURL(url)
    "http://www.exemplo.com/L%C3%A2mpadaDosB%C3%AAbados"
    """

    # Separa a url em seus elementos básicos:
    url_lista = list(parse.urlsplit(url))

    # Muda o path da url (2º elemento, que tem unicode):
    url_lista[2] = parse.quote(url_lista[2])

    # Junta novamente a url:
    url = parse.urlunsplit(url_lista)

    return url


def abrir_pagina(url, limparHTML = False):
    """ Conecta a uma URL e retorna seu conteúdo em texto.
    Opcionalmente, se o conteúdo tiver caracteres não reconhecidos,
    pode tentar substituí-los por seus equivalentes em UTF-8 ao retornar
    o texto.
    Para isto, basta colocar limparHTML = True.
    """
	
    tentativas = 0
    pagina = ""
    
    while (tentativas <= 10):
        try:
            pagina = URL.urlopen(url)
            break
        except UnicodeEncodeError:
            # URL com Unicode:
            url = decode_unicodeURL(url)
        except error.URLError:
            # Não foi possivel abrir a conexão, tenta novamente em 3 segundos:
            tentativas += 1
            time.sleep(3)
            

    # Caso a página esteja vazia (não conseguiu pegar conteúdo):      
    if not pagina:
        return ""
    
    try:
        # Conteúdo da página:
        pagina_str = pagina.read().decode(pagina.headers.get_content_charset())
    except Exception:
        # Página sem charset é lida como UTF-8:
        pagina_str = pagina.read().decode("utf-8")
        
    if (limparHTML):
        # Remove elementos HTML, substituindo pelos caracteres certos:
        pagina_str = html.unescape(pagina_str)
        
    return pagina_str


def abrir_chrome():
    """ Abre uma janela do Chrome e retorna
    a instância do navegador aberta.
    """
	
    # Ignora erros de certificado e prossegue:
    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument('--ignore-certificate-errors')
    
    browser = webdriver.Chrome(chrome_options = opcoes)

    return browser
    

def fechar_navegador(browser):
    """ Fecha um navegador aberto (qualquer que seja ele). """
	
    browser.quit()


def abrir_pagina_nav(browser, url, tempo = 5):
    """ Abre uma página com um navegador acionado
    pelo programa. Espera um tempo padrão de 5 segundos
    após abrir, para a página carregar.
    """
	
    browser.get(url)
    time.sleep(tempo)


def clicar_botao(browser, caminho_botao, tempo = 5):
    """ Com um navegador com uma página aberta,
    clica em todos os elementos identificados pelo
    XPath dado em caminho_botao.
    Espera um tempo padrão de 5 segundos
    após cada clique.

    Exemplo de XPath:
    '//div[@class='container']'
    Seleciona todas as divs de classe container.
    """
	
    while True:
        try:
            element = browser.find_element_by_xpath(caminho_botao)
            element.click()
            time.sleep(tempo)
        except Exception:
            # A exceção indica que não há os elementos especificados.
            # Então, encerra o loop.
            break
    
