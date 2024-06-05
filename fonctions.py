import streamlit as st 
import snowflake.connector as sc
import pandas as pd

def Authentification(username, password,account):
    try:
        conn = sc.connect(
            user=username,
            password=  password,
            account= account
        )
        return conn
    except Exception as e:
        print(e)
        return None
    
