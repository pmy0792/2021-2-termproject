from flask import Flask, session,url_for,render_template,render_template_string, request, redirect
import pandas as pd
from daash import create_dash_app
from static import clg_and_dptmt
clgs=clg_and_dptmt.clgs
result=pd.read_csv("./static/result5.csv")[["College","Major","Continent","Country","Foreign Univ","Semester","Url"]]

app = Flask(__name__)
create_dash_app(app)
def continent_dic():
    continent_df=pd.read_csv("./static/continent-country.csv")
    continents = continent_df["Continent"].value_counts().keys()
    continents = list(continents)
    result_dic = {}
    for continent in continents:
        temp = continent_df[continent_df["Continent"] == continent]
        country_list = list(temp["Country"].value_counts().keys())
        result_dic[continent] = country_list
        
    result_dic["Oceania"]=["호주","뉴질랜드"]
    result_dic["etc"].remove("호주")
    result_dic["etc"].remove("뉴질랜드")
    return result_dic

def search_df(slctd_clg,slctd_dptmt,slctd_cntry):

    #result=result[["College","Major","Continent","Country","Foreign Univ","Semester","Url"]]
    df=pd.DataFrame(columns=["College","Major","Continent","Country","Foreign Univ","Semester","Url"])

    if slctd_clg=="모든 단과대학":
        for cntry in slctd_cntry:
            temp = result[(result["Country"] == cntry)]
            df = df.append(temp)
    elif slctd_dptmt=="모든 학과":
        for cntry in slctd_cntry:
            temp=result[(result["College"]==slctd_clg)& (result["Country"]==cntry)]
            df=df.append(temp)
    else:
        for cntry in slctd_cntry:
            temp=result[(result["College"]==slctd_clg) & (result["Major"]==slctd_dptmt) & (result["Country"]==cntry)]
            df=df.append(temp)
    print("집계완료")
    print(df)
    return df

def popular_cntry(slctd_clg,slctd_dptmt):
    if slctd_clg=="모든 단과대학":
        cont_df=result["Continent"].value_counts().rename_axis('Continent').reset_index(name='Count').sort_values(by="Count",ascending=False).reset_index(drop=True)
        most_pplr_cont=cont_df.iloc[0]["Continent"]

        cntry_df=result["Country"].value_counts().rename_axis('Country').reset_index(name='Count').sort_values(by="Count",ascending=False).reset_index(drop=True)

    else:
        #if slctd_dptmt=="모든 학과":
            cont_df=result[result["College"]==slctd_clg]["Continent"].value_counts().rename_axis('Continent').reset_index(name='Count').sort_values(by="Count",ascending=False).reset_index(drop=True)
            most_pplr_cont=cont_df.iloc[0]["Continent"]
            cntry_df=result[result["College"]==slctd_clg]["Country"].value_counts().rename_axis('Country').reset_index(name='Count').sort_values(by="Count",ascending=False).reset_index(drop=True)

    most_pplr_cntry1 = cntry_df.iloc[0]["Country"]
    most_pplr_cntry2 = cntry_df.iloc[1]["Country"]
    most_pplr_cntry3 = cntry_df.iloc[2]["Country"]


    return most_pplr_cont,most_pplr_cntry1,most_pplr_cntry2,most_pplr_cntry3

@app.route('/', methods=["GET", "POST"])
def index(slctd_clg="None",slctd_dptmt="None",slctd_cntry="None",headings=tuple(),data=tuple(),popular_list=[]):
    if request.method == "POST":
        slctd_clg = request.form.get("college")
        slctd_dptmt = request.form.get("department")
        slctd_cntry=request.form.getlist("country")


        searched_df=search_df(slctd_clg, slctd_dptmt, slctd_cntry)
        headings=tuple(searched_df.columns)
        data=tuple(searched_df.to_records(index=False))
        p_cont,p_cntry1,p_cntry2,p_cntry3=popular_cntry(slctd_clg,slctd_dptmt)
        popular_list=[p_cont,p_cntry1,p_cntry2,p_cntry3]
    return render_template("1.html",continents=continents,slctd_clg=slctd_clg,slctd_dptmt=slctd_dptmt,slctd_cntry=slctd_cntry,headings=headings,data=data,popular_list=popular_list)

@app.route('/dashboard2',methods=["GET"])
def dashboard():
    return render_template("dashboard.html")

if __name__ == '__main__':
    continents=continent_dic()

    app.run(host="127.0.0.1",port=5001,debug=True)
