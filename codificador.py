from math import log
from itertools import chain, groupby
from sage.all import Matrix
import numpy as np

class Message:
    
    def _flatten(self,listOfLists:list) -> list:
        return chain.from_iterable(listOfLists)
    
    def _rBlanks(self,strng:str) -> str:
        """Sustituye los espacios en blanco por '_' y convierte a mayuscula"""
        return strng.replace(' ', '_').upper()
    
    def _normalize(self,strng:str) -> list:
        """
        Sustituye los espacios en blanco por '_' y los caracteres
        especiales por su traduccion de alphSpecial
        """
        s = self._rBlanks(strng)
        accum = []
        for ch in s:
            if ch in self.alphSpecials:
                accum.append(self.alphSpecials[ch])
            else:
                accum.append(ch)
        return filter(lambda x: x in self.alphabet,self._flatten(accum))

    def __init__(self,strng):
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789'
        self.alphSpecials = {
            'Á' : 'A',
            'É' : 'E',
            'Í' : 'I',
            'Ó' : 'O',
            'Ú' : 'U',
            'Ä' : 'A',
            'Ë' : 'E',
            'Ï' : 'I',
            'Ö' : 'O',
            'Ü' : 'U',
            'Ñ' : 'GN'
        }
        x = self._normalize(strng)
        self.content = ''.join(x)
        self.length = len(self.content)
        
        
    def __str__(self):
        return self.content
    

class CodificadorHill:
    
    def NormalizarTexto(self, texto):
        t = Message(texto)
        return t.content
    
    def AniadirEspacios(self, numEspacios, texto):
        texto = texto + (numEspacios * '_')
        return texto
        
    def TransformarTexto(self, texto, dic):
        # Transforma caracteres en sus traducciones a numeros segun dic
        numeros = [dic[letra] for letra in texto]
        return numeros
    
    def ObtenerTextoDeMatriz(self, matriz):
        # Convierte una matriz de numeros en otra de caracteres segun numCh
        numCh = {v:i for i, v in self.dic.items()}
        dic_formateado = {int(clave): valor for clave, valor in numCh.items()}
        matriz_caracteres = [[dic_formateado[elemento] for elemento in fila] for fila in matriz]
    
    def ObtenerMatriz(self, textoNumeros):
        # Obtiene la matriz nxn a partir del texto de numeros
        matriz = []
        for i in range(0, len(textoNumeros), self.n):
            fila = textoNumeros[i:i+self.n]
            matriz.append(fila)
        matriz = np.array(matriz)
        # Hacer la traspuesta
        matriz = matriz.T
        return matriz
    
    def ObtenerTexto(self, dic, array):
        # Convierte un array de numeros en texto segun dic
        texto = [dic[letra] for letra in array]
        texto = ''.join(texto)
        return texto
    
    # Funcion que cambia _ por espacios
    def CambiarEspacios(self, texto):
        texto = texto.replace('_', ' ')
        return texto

    def Cifrar(self, texto:str):
        texto = self.NormalizarTexto(texto)

        # Hay que añadir barras bajas por si la longitud del texto no coincide con 
        # la dimension de la clave (n)
        longitudTexto = len(texto)
        resto = longitudTexto % self.n
        if(resto != 0):
            texto = self.AniadirEspacios(self.n-resto, texto)
            
        textoNumeros = self.TransformarTexto(texto, self.chNum)
        matriz = self.ObtenerMatriz(textoNumeros)
        
        # Hacer el producto de la clave y la matriz obtenida mod len(diccionario)
        producto = self.clave @ matriz
        productoMod = producto % len(self.numCh)
        
        # Hacer la traspuesta para que flatten de el resultado adecuado
        productoMod = productoMod.T
        array = productoMod.flatten()
        # Convertir el array a texto usando el numch

        return self.ObtenerTexto(self.numCh, array)


    
    def Descifrar(self, texto:str):
        # Descifrar el texto haciendo el producto de la matriz por la inversa de la clave
        
        texto = self.NormalizarTexto(texto)

        textoNumeros = self.TransformarTexto(texto, self.chNum)
        matriz = self.ObtenerMatriz(textoNumeros)

        # Hacer el producto de la inversa de la clave por la matriz
        # y aplicar el módulo len(diccionario)
        inversa = np.linalg.inv(self.clave).astype(int)
        producto = inversa @ matriz
        productoMod = producto % len(self.numCh)

        # Hacer la traspuesta par que flatten de el resultado adecuado
        productoMod = productoMod.T
        array = productoMod.flatten()

        resultado = self.ObtenerTexto(self.numCh, array).lower()
        resultado = self.CambiarEspacios(resultado)

        return resultado
    


    def Ataque_Gauss(self, texto_plano, texto_cifrado):
        
        # Normalizamos el texto
        texto_plano = self.NormalizarTexto(texto_plano)
        
        # Añadimos espacios si lo necesita
        longitudTexto = len(texto_plano)
        resto = longitudTexto % self.n
        if(resto != 0):
            texto_plano = self.AniadirEspacios(self.n-resto, texto_plano)
        
        # Obtenemos los índices correspondientes
        texto_plano_numeros = self.TransformarTexto(texto_plano, self.chNum)
        texto_cifrado_numeros = self.TransformarTexto(texto_cifrado, self.chNum)
        
        # Obtenemos las matrices con los índices según el diccionario
        matriz_plano = self.ObtenerMatriz(texto_plano_numeros).T
        matriz_cifrado = self.ObtenerMatriz(texto_cifrado_numeros).T
        
        # Convertimos la matriz de pyhton a una de sage
        M = Matrix(matriz_plano)
        C = Matrix(matriz_cifrado)
        
        # Creamos la matriz [M | C] para resolver el sistema de ecuaciones lineales
        matriz_ampliada = M.augment(C)

        # Aplicamos Gauss-Jordan
        matriz_reducida = matriz_ampliada.rref() % len(self.numCh)

        # Extraemos la matriz clave
        matriz_clave = matriz_reducida[:, -len(M.columns()):].T
        
        return matriz_clave
        
    
    def __init__(self, n : int):
        self.n = n
        self.numCh = {
            0:'A',
            1:'B',
            2:'C',
            3:'D',
            4:'E',
            5:'F',
            6:'G',
            7:'H',
            8:'I',
            9:'J',
            10:'K',
            11:'L',
            12:'M',
            13:'N',
            14:'O',
            15:'P',
            16:'Q',
            17:'R',
            18:'S',
            19:'T',
            20:'U',
            21:'V',
            22:'W',
            23:'X',
            24:'Y',
            25:'Z',
            26:'_',
            27:'0',
            28:'1',
            29:'2',
            30:'3',
            31:'4',
            32:'5',
            33:'6',
            34:'7',
            35:'8',
            36:'9',
        }

        self.chNum = {v:i for i, v in self.numCh.items()}