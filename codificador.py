from math import log
from itertools import chain, groupby
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
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_'
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
    
    def Cifrar(self, texto:str):
        texto = self.NormalizarTexto(texto)

        
        # Hay que añadir espacios por si la longitud del texto no coincide con 
        # la dimension de la clave (n)
        longitudTexto = len(texto)
        resto = longitudTexto % self.n
        if(resto != 0):
            texto = self.AniadirEspacios(self.n-resto, texto)
            
        textoNumeros = self.TransformarTexto(texto, self.chNum)
        matriz = self.ObtenerMatriz(textoNumeros)
        
        # Hacer el producto de la clave y la matriz obtenida mod 27
        producto = self.clave @ matriz
        productoMod = producto % 27
        
        productoMod = productoMod.T
        array = productoMod.flatten()
        # convertir el array a texto usando el numch ya creado y sin dar formato
        # No dar formato al array

        return self.ObtenerTexto(self.numCh, array)


    
    def Descifrar(self, texto:str):
        # Descifrar el texto haciendo el producto de la matriz por la inversa de la clave
        
        texto = self.NormalizarTexto(texto)

        textoNumeros = self.TransformarTexto(texto, self.chNum)
        matriz = self.ObtenerMatriz(textoNumeros)

        # Hacer el producto de la inversa de la clave por la matriz
        inversa = np.linalg.inv(self.clave).astype(int)
        producto = inversa @ matriz
        productoMod = producto % 27

        productoMod = productoMod.T
        array = productoMod.flatten()

        return self.ObtenerTexto(self.numCh, array)
        
        
    
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
            26:'_'
        }

        self.chNum = {v:i for i, v in self.numCh.items()}
