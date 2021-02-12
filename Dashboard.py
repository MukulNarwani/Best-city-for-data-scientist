import pandas as pd     #(version 1.0.0)
import plotly as py        #(version 4.5.4) #pip install plotly==4.5.4
import plotly.express as px
import plotly.io as pio
import numpy as np


df = pd.read_excel('data.xls')


#filter out error fields
bools =[]
for column in df.columns:
    if column != 'Unnamed: 0':    
        s=df[column]
        filter = s.str.find('Error:').astype(bool).tolist()
        bools.append(filter)
    
bools=np.array(bools)
combined_filter=np.matrix([fil.all() for fil in np.matrix([*bools]).T]).A1
df= df[pd.Series(combined_filter)]

for col in df.columns:
    col = int(col)

barchart = px.scatter(df,x='Salary',y='Rent', hover_data=[df.columns[0]])
df=df.sort_values([df.columns[1]])
print(df)
#pio.show(barchart)