import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def calc_total_macros(df,drop=True):
    macros=["kcal","protein","carbs","fat"]
    for macro in macros:
        df["total "+macro]=df["g"]/100*df[macro]
    if drop:
        df.drop(macros,axis=1,inplace=True)
        
#color scheme:
dark_blue="#31525b"
light_blue="#b3dee5"
orange="#ffa101"
peach_yellow="#fae6b1"
#%%
meal_types=pd.read_csv(r"C:\Users\Tamás Baráth\Documents\diet\meal_types.csv",
                       sep=",")
meals_eaten=pd.read_csv(r"C:\Users\Tamás Baráth\Documents\diet\meals_eaten.csv",
                       sep=",")
meals_eaten["date"]=pd.to_datetime(meals_eaten["date"],
                                   format="%d/%m/%Y")
#%%
new_meal=pd.DataFrame({
    "name": ["Biscino (Sonday, melkchocolade)"],
    "kcal":[506],
    "protein":[7.7],
    "carbs":[57.6],
    "fat":[26]
     })

if not new_meal["name"][0] in meal_types["name"].to_list():
    meal_types=meal_types.append(new_meal)
#%%
meal_types.to_csv(r"C:\Users\Tamás Baráth\Documents\diet\meal_types.csv",
                sep=",",index=False)
#%%







#%%
new_meal_eaten=pd.DataFrame({
    "name": ["Biscino (Sonday, melkchocolade)"],
    "g":[125/9],
    "date":["12/6/2021"]
     })
new_meal_eaten["date"]=pd.to_datetime(new_meal_eaten["date"],
                                      format="%d/%m/%Y")

meals_eaten=meals_eaten.append(new_meal_eaten)

#%%
# Delete last n meals
n=1
meals_eaten=meals_eaten[:-n]
#%%
meals_eaten["date"]=pd.to_datetime(meals_eaten["date"],
                                   format="%d/%m/%Y")
meals_eaten.to_csv(r"C:\Users\Tamás Baráth\Documents\diet\meals_eaten.csv",
                sep=",",index=False,date_format="%d/%m/%Y")

#%%
timestamp=pd.to_datetime("12/6/2021",format="%d/%m/%Y")
# Select meals eaten at date
macros_df=meals_eaten[meals_eaten['date']==timestamp] 
# left join food macros
macros_df=macros_df.merge(meal_types,on="name")
# calculate total macros
calc_total_macros(macros_df)
print("calories eaten:",macros_df["total kcal"].sum())
print("protein eaten:",macros_df["total protein"].sum())
print("carbs eaten:",macros_df["total carbs"].sum())
print("fat eaten:",macros_df["total fat"].sum())
#%%
plot_df=meals_eaten.merge(meal_types,on="name")
calc_total_macros(plot_df)
plot_df=plot_df.resample("D",on="date").sum()
plot_df['date'] = plot_df.index
kcal_plot_df=plot_df[['date',"total kcal"]]
plot_df=plot_df.drop(["g","total kcal"],axis=1)

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(
    go.Scatter(x=plot_df["date"], y=plot_df["total protein"],
               name="total protein",
               mode="lines+markers",
               line=dict(color=dark_blue, width=4),
               marker=dict(color=dark_blue, size=16, opacity=0.5)),
    secondary_y=False)
fig.add_trace(
    go.Scatter(x=plot_df["date"], y=plot_df["total carbs"],
               name="total protein",
               mode="lines+markers",
               line=dict(color=light_blue, width=4),
               marker=dict(color=light_blue, size=16, opacity=0.5)),
    secondary_y=False)
fig.add_trace(
    go.Scatter(x=plot_df["date"], y=plot_df["total fat"],
               name="total protein",
               mode="lines+markers",
               line=dict(color=peach_yellow, width=4),
               marker=dict(color=peach_yellow, size=16, opacity=0.5)),
    secondary_y=False)
fig.add_trace(
    go.Scatter(x=kcal_plot_df["date"], y=kcal_plot_df["total kcal"],
               name="total kcal",
               mode="lines+markers",
               line=dict(color=orange, width=4),
               marker=dict(color=orange, size=16, opacity=0.5)),
    secondary_y=True,
)

fig.update_layout(template="plotly_white")
fig.update_xaxes(
    dtick="d",
    tickformat="%d %b")
fig.show()

#%%

check_df=meal_types.copy()
check_df["estimated kcal"]=check_df["carbs"]*4+check_df["fat"]*8.8+check_df["protein"]*4
check_df["error"]=check_df["estimated kcal"]-check_df["kcal"]
check_df["relative error"]=(check_df["estimated kcal"]-check_df["kcal"])/check_df["estimated kcal"]