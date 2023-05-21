########################## LEVEL BASED CLASSIFICATION #############################
# This is a classification project. It is built on sales data of a gaming company.
# Firstly, creation of persona is made by using sales data.
# Secondly, these personas are seperated to segments.

########################## Import Library and Edit Settings  ###########################
import pandas as pd
import os

path = "C:\\Users\\hseym\\OneDrive\\Masaüstü\\Miuul\\datasets"
os.chdir(path)

pd.set_option("display.max_columns", 30)
pd.set_option('display.width', 500)
pd.set_option('display.max_rows', 100)
pd.set_option('display.float_format', lambda x: '%.4f' % x)


########################## Loading  The Date  ###########################
def load_data(dataname):
    return pd.read_csv(dataname)


persona = load_data("persona.csv")
df = persona.copy()


########################## Exploring The Data  ###########################
def check_df(dataframe):
    if isinstance(dataframe, pd.DataFrame):
        print("########## shape #########\n", dataframe.shape)
        print("########## types #########\n", dataframe.dtypes)
        print("########## head #########\n", dataframe.head())
        print("########## tail #########\n", dataframe.tail())
        print("########## NA #########\n", dataframe.isna().sum())
        print("########## describe #########\n", dataframe.describe().T)
        print("########## nunique #########\n", dataframe.nunique())


check_df(df)


##########################  Data Analysis  ###########################

def data_analysis(dataframe):
    # Unique Values Counts of "Source":
    print("Unique Values of Source:\n", df["SOURCE"].nunique())
    print("################################################")

    # Frequency  of "Source":
    print("Frequency  of Source:\n", df["SOURCE"].value_counts())
    print("################################################")

    # Unique Values Counts of "Price":
    print("Unique Values of Price:\n", df["PRICE"].nunique())
    print("################################################")

    # Frequency of "Price":
    print("Frequency  of Price:\n", df["PRICE"].value_counts())
    print("################################################")

    # Total Sale per "Country":
    print("Total Sale per Country:\n", df["COUNTRY"].value_counts())
    print("################################################")

    # Total and Average Income per "Country":
    print("Total Income per Country:\n", df.groupby("COUNTRY")["PRICE"].sum())
    print("Average Income per Country:\n", df.groupby("COUNTRY")["PRICE"].mean())
    print("################################################")

    # Average Income per "Source":
    print("Average Income per Source:\n", df.groupby("SOURCE")["PRICE"].mean())
    print("################################################")

    # Average Income by "Source" and "Country":
    print("Average Income by Source and Country:\n", df.groupby(["SOURCE", "COUNTRY"])["PRICE"].mean())


data_analysis(df)


##########################  Creating Persona  ###########################

def create_persona(dataframe):
    bins = [0, 18, 23, 35, 45, dataframe["AGE"].max()]
    labels = ["0_18", "19_23", "24_30", "31_40", "41_" + str(dataframe["AGE"].max())]

    dataframe["AGE_CAT"] = pd.cut(dataframe["AGE"], bins, labels=labels)
    print("Age Category Summary:\n", dataframe.groupby("AGE_CAT").agg({"AGE": ["min", "max", "count"]}))

    agg_df = dataframe.groupby(["COUNTRY", "SOURCE", "SEX", "AGE_CAT"])[["PRICE"]].mean().reset_index()
    agg_df["CUSTOMER_LEVEL_BASED"] = [str(row[0].upper()) + "_" +
                                      str(row[1].upper()) + "_" +
                                      str(row[2].upper()) + "_" +
                                      str(row[3])
                                      for row in agg_df.values]
    agg_df_persona = agg_df.groupby("CUSTOMER_LEVEL_BASED").agg({"PRICE": "mean"}).reset_index()

    return agg_df_persona


agg_persona = create_persona(df)


##########################  Segmentation by Persona  ###########################
def segmentation(dataframe):
    labels = ["D", "C", "B", "A"]
    agg_persona["SEGMENT"] = pd.qcut(agg_persona["PRICE"], 4, labels = labels)

    print("Summary Statistic of Segments:\n", agg_persona.groupby("SEGMENT").agg({"PRICE": ["mean", "max", "min", "sum"]}))
    print("###############################################################################")
    return agg_persona


segmentation(df)


##########################  Prediction  ###########################
def new_user(persona_dataframe):
    x = input("Please enter the new user's information in the correct order, leaving a space.\n"
              "Example : bra android female 23 ")
    x = x.upper()
    x_list = x.split()

    while len(x_list) != 4:
        x = input("Please enter correct format")
        x = x.upper()
        x_list = x.split()

    new = ""

    for i, j in enumerate(x_list):
        if i < 3:
            new += j + "_"

    age = int(x_list[3])
    cat = ""
    if age >= 41:
        cat = "41_66"
    elif age >= 31:
        cat = "31_40"
    elif age >= 24:
        cat = "24_30"
    elif age >= 19:
        cat = "19_23"
    else:
        cat = "0_18"

    user = new + cat
    return persona_dataframe[persona_dataframe["CUSTOMER_LEVEL_BASED"] == user]


new_user(agg_persona)