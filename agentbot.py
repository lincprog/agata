# -*- coding: utf-8 -*-

"""

Este Script é reponsável por detectar a intenção do usuário no DialogFlow e retornar a possível resposta

"""

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] ="CHAVE_DE_AUTENTICAÇÃO_DO_AGENT_NO_DIALOGFLOW"

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "PROJECT_ID_DO_AGENT_NO_DIALOGFLOW"


def detect_intent_from_text(text, session_id, language_code='pt-br'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def fetch_reply(query, session_Id):
    response = detect_intent_from_text(query, session_Id)
    return response.fulfillment_messages
    
