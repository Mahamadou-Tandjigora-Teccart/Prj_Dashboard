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

def lister_bases_de_donnees(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        cursor.close()
        return databases
    except Exception as e:
        st.error(f"Erreur lors de la récupération des bases de données: {e}")
        return None

def creer_base_de_donnees(conn, nom_base_de_donnees):
    try:
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {nom_base_de_donnees}")
        st.success(f"Base de données '{nom_base_de_donnees}' créée avec succès")
        cursor.close()
    except Exception as e:
        st.error(f"Erreur lors de la création de la base de données: {e}")

def lister_schemas(conn, nom_base_de_donnees):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SHOW SCHEMAS IN DATABASE {nom_base_de_donnees}")
        schemas = cursor.fetchall()
        cursor.close()
        
        return schemas
    except Exception as e:
        st.error(f"Erreur lors de la récupération des schémas: {e}")
        return None

def ajouter_schema(conn, nom_base_de_donnees, nom_schema):
    try:
        cursor = conn.cursor()
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {nom_base_de_donnees}.{nom_schema}")
        st.success(f"Schéma '{nom_schema}' ajouté avec succès")
        cursor.close()
    except Exception as e:
        st.error(f"Erreur lors de l'ajout du schéma: {e}")

def lister_warehouses(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW WAREHOUSES")
        warehouses = cursor.fetchall()
        cursor.close()
        return warehouses
    except Exception as e:
        st.error(f"Erreur lors de la récupération des datawarehouses: {e}")
        return None

def creer_warehouse(conn, nom_warehouse):
    try:
        cursor = conn.cursor()
        cursor.execute(f"CREATE WAREHOUSE IF NOT EXISTS {nom_warehouse}")
        st.success(f"DataWarehouse '{nom_warehouse}' créé avec succès")
        cursor.close()
    except Exception as e:
        st.error(f"Erreur lors de la création du datawarehouse: {e}")
