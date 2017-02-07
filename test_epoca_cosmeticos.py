## Criado com Python 3.4.3
##############################################
##############################################
########### Importações

# Testes unitários:
import unittest

# Funções a serem testadas:
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
########### Testes

class TestesWebScrap(unittest.TestCase):
    
    def test_extrair_meio(self):
        texto = "aiweyiq67hello aba29099du0267world aba2u3"
        resultado = ['hello','world']
        self.assertEqual(webF.extrair_meio(texto, "67", " aba"), resultado)

    def test_decode_unicodeURL(self):
        url = "http://www.exemplo.com/LâmpadaDosBêbados"
        resultado = "http://www.exemplo.com/L%C3%A2mpadaDosB%C3%AAbados"
        self.assertEqual(webF.decode_unicodeURL(url), resultado)

    def test_abrir_pagina(self):
        # A página do Google não deve estar vazia.
        url = "https://www.google.com.br/"
        self.assertNotEqual(webF.abrir_pagina(url), "")

    def test_pagina_sem_char_especiais(self):
        # Se a página não tem caracteres especiais, deve estar igual antes
        # e depois de ser 'limpa'.
        url = "http://example.com/"
        self.assertEqual(webF.abrir_pagina(url), webF.abrir_pagina(url, True))


if __name__ == '__main__':
    unittest.main()
