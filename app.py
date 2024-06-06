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
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        # Entrees utilisateurs
        User = st.text_input("Username")
        Password = st.text_input("Password", type='password')
        Account = st.text_input("Account")
        
        if st.button("Se Connecter"):
            conn = Authentification(User, Password, Account)
            if conn is not None:
                st.session_state.authenticated = True
                st.session_state.conn = conn
                st.success("Connexion réussie au compte")
                st.experimental_rerun()
            else:
                st.error("Connexion au compte échouée")
    else:
        st.title("Bienvenue sur le dashboard")
        conn = st.session_state.conn
        
        if st.button("Voir les Warehouses de données"):
            try:
                cursor = conn.cursor()
                cursor.execute("SHOW WAREHOUSES")
                warehouses = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                df_warehouses = pd.DataFrame(warehouses, columns=columns)
                st.write(df_warehouses)
                cursor.close()
            except Exception as e:
                st.error(f"Erreur lors de la récupération des warehouses: {e}")
        
        warehouse_name = st.text_input("Nom du warehouse")
        if st.button("Créer un warehouse de données"):
            if warehouse_name:
                try:
                    cursor = conn.cursor()
                    cursor.execute(f"CREATE WAREHOUSE {warehouse_name}")
                    st.success(f"DataWarehouse {warehouse_name} créé")
                    cursor.close()
                except Exception as e:
                    st.error(f"Erreur lors de la création du warehouse: {e}")
            else:
                st.warning("Veuillez entrer un nom pour le warehouse.")
        
        if st.button("Se Déconnecter"):
            st.session_state.authenticated = False
            del st.session_state.conn
            st.experimental_rerun()

if __name__ == '__main__':
    main()
