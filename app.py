import streamlit as st
import snowflake.connector as sc
import pandas as pd
from fonctions import Authentification



def main():
    st.markdown(
        """
        <style>
        .stButton > button {
            background-color: blue;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
        }
        .stButton > button:hover {
            background-color: darkblue;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.title("Connexion au dashboard")
    
    # Entrees utilisateurs
    User= st.text_input("Username")
    Password= st.text_input("Password", type='password')
    Account= st.text_input("Account")
    
    if st.button("Se Connecter"):
        conn= Authentification(User,Password,Account)
        if conn is not  None:
            st.success("Connexion réussie au compte")
            
            st.title("Bienvenue sur le dashboard")
            if st.sidebar.button("Voir les Warehouses de donnees"):
                st.write("Hiiii")
                # cursor= st.cursor()
                # cursor.execute("SHOW WAREHOUSES")
                # warehouses=cursor.fetchall()
                # st.write(warehouses) 
                
            if st.sidebar.button("Ceer un warehouse de donnees"):
                warehouse_name= st.text_input("Nom du warehouse")
                if st.button("Ceer"):
                    cursor=conn.cursor()
                    cursor.execute(f"create warehouse {warehouse_name} ")
                    st.success(f"DataWarehouse{warehouse_name} cree")
                
                
                
        else:
            st.error("Connexion au compte échouée")
            
            
    
    
    
    
if __name__ == '__main__':
    main()