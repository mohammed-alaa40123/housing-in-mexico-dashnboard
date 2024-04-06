# Preparing data
import pandas as pd
import plotly.express as px
import streamlit as st

# Loading Data
df1 = pd.read_csv("data/brasil-real-estate-1.csv")
df2 = pd.read_csv("data/brasil-real-estate-2.csv")

#Preproccessing Data
df1[["lat","lon"]] = df1["lat-lon"].str.split(",",expand=True).astype(float)
df1["state"]=df1["place_with_parent_names"].str.split("|",expand=True)[2]
df1["price_usd"] = (df1["price_usd"]
                 .str.replace("$","",regex=False)
                 .str.replace(",","")
                 .astype(float))
df1.drop(columns=["lat-lon","place_with_parent_names"],inplace=True)
df2["price_usd"]=df2["price_brl"]/3.19
df2.dropna(inplace=True)
df2.drop(columns=["price_brl"],inplace=True)

#merge data
df = pd.concat([df1 , df2])