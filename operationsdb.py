# -*- coding: utf-8 -*-
"""

Este Script é responsável por realizar as operações de banco de dados

"""

from datetime import datetime

def searchUserByFromId(fromId, cursor):
    sql_command = ("SELECT FromId FROM tbusuario WHERE FromId = %s")
    cursor.execute(sql_command, fromId)
    users = cursor.fetchall() # Retorna todos os valores obtidos no select
    cont=0
    for u in users:
        cont+=1
    if cont >= 1:
        return True # Retorna true se esse usuário já foi cadastrado
        
    else:
        return False # ou falso se ainda não foi        

def createUser(firstName, lastName, fromId, cursor, connection):
    sql_command = "INSERT INTO tbusuario(Nome, SobreNome, FromId) VALUES (%s,%s,%s)"
    valor = (firstName, lastName, fromId)
    cursor.execute(sql_command, valor)
    connection.commit()

def createConversation(fromId, msgIn, msgOut, dateMsg, cursor, connection):
    sqlIdUsuario = ("SELECT Id FROM tbusuario WHERE FromId = %s")
    cursor.execute(sqlIdUsuario, fromId)
    idUsers = cursor.fetchone()
    for idUser in idUsers:
        idUsuario = idUser
    sql_command = "INSERT INTO tbconversa(FkIdUsuario, MensagemEntrada, MensagemSaida, DataMensagem) VALUES (%s,%s,%s,%s)"
    
    convertDateUnixToInt = int(dateMsg)
    convertedDate = datetime.utcfromtimestamp(convertDateUnixToInt).strftime('%Y-%m-%d %H:%M:%S')
    
    valor = (idUsuario, msgIn, msgOut, convertedDate)
    cursor.execute(sql_command, valor)
    connection.commit()
