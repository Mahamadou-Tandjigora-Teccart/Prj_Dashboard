import streamlit as st
import snowflake.connector as sc
import pandas as pd
from fonctions import Authentification,lister_bases_de_donnees,creer_base_de_donnees,lister_schemas,ajouter_schema


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
        .button-container {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 20px;
        }
        .disconnect-button {
            background-color: red !important;
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.show_create_warehouse = False

    if not st.session_state.authenticated:
        st.title("Connexion au dashboard")
        # Entrées utilisateurs
        with st.form(key='login_form'):
            User = st.text_input("Username")
            Password = st.text_input("Password", type='password')
            Account = st.text_input("Account")
            submit_button = st.form_submit_button(label='Se Connecter')
        
        if submit_button:
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

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Voir les Bases de Données"):
                bases_de_donnees = lister_bases_de_donnees(conn)
                if bases_de_donnees:
                    st.subheader("Liste des Bases de Données")
                    for db in bases_de_donnees:
                        st.write(db[1])

            if st.button("Voir les Schémas"):
                nom_base_de_donnees = st.text_input("Nom de la Base de Données")
                if nom_base_de_donnees:
                    schemas = lister_schemas(conn, nom_base_de_donnees)
                    if schemas:
                        st.subheader(f"Liste des Schémas dans la base de données '{nom_base_de_donnees}'")
                        for schema in schemas:
                            st.write(schema[1])

        with col2:
            if st.button("Créer une Base de Données"):
                nom_base_de_donnees = st.text_input("Nom de la Base de Données")
                if nom_base_de_donnees:
                    creer_base_de_donnees(conn, nom_base_de_donnees)

            if st.button("Ajouter un Schéma"):
                nom_base_de_donnees = st.text_input("Nom de la Base de Données")
                nom_schema = st.text_input("Nom du Schéma")
                if nom_base_de_donnees and nom_schema:
                    ajouter_schema(conn, nom_base_de_donnees, nom_schema)

if __name__ == '__main__':
    main()
