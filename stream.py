import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
st.set_page_config(page_title="Türkiye Enflasyon Tahmini")
tabs=["Yıllık Enflasyon","Aylık Enflasyon","Model Bazlı Yıllık Tahmin","Model Bazlı Aylık Tahmin","Performans Tablomuz","Metodoloji","Hakkında"]
page=st.sidebar.radio("Sekmeler",tabs)
yıllıktahmin=pd.read_csv("yıllıktahmin.csv")
yıllıktahmin=yıllıktahmin.set_index(yıllıktahmin["Unnamed: 0"])
del yıllıktahmin["Unnamed: 0"]
yıllıktahmin=yıllıktahmin.rename_axis(["Tarih"])
aylık=pd.read_csv('aylık.csv')
aylık=aylık.set_index(aylık["Unnamed: 0"])
del aylık["Unnamed: 0"]
aylık=aylık.rename_axis(["Tarih"])
aylık.columns=["Aylık Enflasyon"]
df=pd.read_csv("df.csv")
df=df.set_index(df["Unnamed: 0"])
del df["Unnamed: 0"]
df=df.rename_axis(["Tarih"])

modelaylık=pd.read_csv('modelaylık.csv')
modelaylık=modelaylık.set_index(modelaylık["Unnamed: 0"])
del modelaylık["Unnamed: 0"]
modelaylık=modelaylık.rename_axis(["Tarih"])






dfas=pd.read_csv("dfas.csv")
dfas=dfas.set_index(dfas["Unnamed: 0"])
del dfas["Unnamed: 0"]
dfas=dfas.rename_axis(["Tarih"])

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=yıllıktahmin.index[:25],y=yıllıktahmin["Ortalama"].iloc[:25],mode='lines',name="Enflasyon"))
fig1.add_trace(go.Scatter(x=yıllıktahmin.index[24:-1],y=yıllıktahmin["Ortalama"].iloc[24:-1],mode='lines',line_color='red',line=dict(dash='dash')))
fig1.add_trace(go.Scatter(x=yıllıktahmin.index[25:-1],y=yıllıktahmin["Ortalama"].iloc[25:-1],mode='markers',name="Tahmin",marker=dict(size=10, color='orange')))
fig1.add_trace(go.Scatter(x=yıllıktahmin.index[16:24],y=[61.94,60.84,62.18,64.70,65.06,65.73,69.47,69.69],mode='markers',name="Geçmiş Tahminler",line_color="black"))
fig1.update_traces(line=dict(width=3)) 

fig1.update_layout(
    xaxis=dict(tickfont=dict(size=14, family="Arial Black", color="black")),  
    yaxis=dict(tickfont=dict(size=14, family="Arial Black", color="black")),
    font=dict(family="Arial", size=14, color="black")
)

fig1.update_xaxes(
    tickformat="%Y-%m",  # Adjust the format as needed
    tickmode="linear",
    tickangle=45,
    tick0=yıllıktahmin.index[1],  # Set the starting tick to the first date in your data
    dtick="M2"  # Set the tick interval to 2 months
)
fig1.update_xaxes(
    range=[yıllıktahmin.index[1], yıllıktahmin.index[-2]]  # Set the range from the first to the last date in your data
)

fig1.update_layout(height=1500,width=1500)


last_12_months = aylık.iloc[-24:-14]
fig2 = px.bar(last_12_months, x=last_12_months.index, y="Aylık Enflasyon", labels={'y': 'Aylık Enflasyon'},text=last_12_months["Aylık Enflasyon"])
fig2.update_traces(texttemplate='%{text:.2f}', textposition='outside', textangle=0)

# Filter the next 12 months for predictions
next_12_months = aylık.iloc[-14:].copy()

fig2.add_trace(go.Bar(x=next_12_months.index, y=next_12_months["Aylık Enflasyon"], name="Tahmin",text=next_12_months["Aylık Enflasyon"]))
fig2.update_traces(texttemplate='%{text:.2f}', textposition='outside', textangle=0)
fig2.update_layout(font=dict(family="Arial Black", size=20, color="black"),xaxis=dict(
        title_font=dict(family="Arial Black", size=14, color="black"),
        tickfont=dict(size=14, family="Arial Black", color="black")
    ),  
    yaxis=dict(
        title_font=dict(family="Arial Black", size=14, color="black"),
        tickfont=dict(size=14, family="Arial Black", color="black")
    ))
fig2.update_xaxes(
    tickformat="%Y-%m"  # Adjust the format as needed
)
fig2.update_layout(width=1000, height=600) 
fig2.update_xaxes(
    tickformat="%Y-%m",  # Adjust the format as needed
    tickmode="linear",
    tickangle=45,
    tick0=aylık.index[-23],  # Set the starting tick to the first date in your data
    dtick="M2"  # Set the tick interval to 2 months
)






fig1.update_layout(width=1000, height=600)  

fig3 = go.FigureWidget(data=[
go.Scatter(x=yıllıktahmin["Ortalama"].iloc[1:25].index,y=yıllıktahmin["Ortalama"].iloc[1:25],mode='lines',name="Enflasyon"),
go.Scatter(x=yıllıktahmin["Ortalama"].iloc[24:-2].index,y=yıllıktahmin["Ortalama"].iloc[24:],mode='lines',name="Ortalama",line={'dash':'dash'}),
go.Scatter(x=yıllıktahmin["NN1"].iloc[24:-2].index,y=yıllıktahmin["NN1"].iloc[24:],mode='lines',name="Neural Network 1",line={'dash':'dash'}),
go.Scatter(x=yıllıktahmin["NN2"].iloc[24:-2].index,y=yıllıktahmin["NN2"].iloc[24:],mode='lines',name="Neural Network 2",line={'dash':'dash'}),
go.Scatter(x=yıllıktahmin["NN3"].iloc[24:-2].index,y=yıllıktahmin["NN3"].iloc[24:],mode='lines',name="Neural Network 3",line={'dash':'dash'}),
go.Scatter(x=yıllıktahmin["NN4"].iloc[24:-2].index,y=yıllıktahmin["NN4"].iloc[24:],mode='lines',name="Neural Network 4",line={'dash':'dash'}),
go.Scatter(x=yıllıktahmin["NN5"].iloc[24:-2].index,y=yıllıktahmin["NN5"].iloc[24:],mode='lines',name="Neural Network 5",line={'dash':'dash'}),
go.Scatter(x=yıllıktahmin["NN6"].iloc[24:-2].index,y=yıllıktahmin["NN6"].iloc[24:],mode='lines',name="Neural Network 6",line={'dash':'dash'})
])
fig3.update_traces(line=dict(width=3)) 
fig3.update_layout(
    xaxis=dict(tickfont=dict(size=14, family="Arial Black", color="black")),  
    yaxis=dict(tickfont=dict(size=14, family="Arial Black", color="black")),
    font=dict(family="Arial", size=14, color="black")
)
fig3.update_xaxes(
    tickformat="%Y-%m",  # Adjust the format as needed
    tickmode="linear",
    tickangle=45,
    tick0=yıllıktahmin.index[1],  # Set the starting tick to the first date in your data
    dtick="M2"  # Set the tick interval to 2 months
)
fig3.update_layout(width=1000, height=600)  
       





if page=='Yıllık Enflasyon':
    st.markdown(
    """
    <style>
        /* Özel stil ayarları */
        .black-text {
            color: black;
            font-size: 24px;
            font-weight: bold;
        }
        .red-text {
            color: red;
            font-size: 24px;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)
    #col1, col2 = st.columns(2)

# Sol sütunda siyah yazı
    #col1.markdown('<p class="inline-text black-text" style="padding-right:1px;">Ocak Ayı Enflasyon Tahmini:</p>', unsafe_allow_html=True)
    #col2.markdown('<p class="inline-text red-text"> %6.60 (Önceki %6.47)</p>', unsafe_allow_html=True)
    st.markdown(
    '<div style="display: flex;">'
    '<p class="inline-text black-text" style="margin-right: 1px;">Mayıs Ayı Enflasyon Tahmini:</p>'
    '<p class="inline-text red-text">%2.95(Önceki %3.22)</p>'
    '</div>',
    unsafe_allow_html=True
)
    st.markdown('<p class="inline-text black-text">Son Güncellenme Tarihi:23 Mayıs 2024</p>', unsafe_allow_html=True)
    st.markdown('<p class="inline-text black-text">Sonraki Güncellenme Tarihi:30 Mayıs 2024</p>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:left;'>Yıllık Enflasyon Tahmini</h1>",unsafe_allow_html=True)
    st.plotly_chart(fig1)
if page=='Aylık Enflasyon':
    st.markdown("<h1 style='text-align:left;'>Aylık Enflasyon Tahmini</h1>",unsafe_allow_html=True)
    st.plotly_chart(fig2)
if page=='Model Bazlı Yıllık Tahmin':
    st.markdown("<h1 style='text-align:left;'>Model Bazlı Tahmin</h1>",unsafe_allow_html=True)
    st.plotly_chart(fig3)
if page=='Model Bazlı Aylık Tahmin':
    st.markdown("<h1 style='text-align:left;'>Model Bazlı Aylık Enflasyon Tahmini</h1>",unsafe_allow_html=True)
    selected_model = st.sidebar.selectbox("Tarih", ["Mayıs 2024","Haziran 2024","Temmuz 2024","Ağustos 2024","Eylül 2024","Ekim 2024","Kasım 2024","Aralık 2024","Ocak 2025"])
    if selected_model=='Şubat 2024':
       sorted_index = modelaylık.iloc[0, :].sort_values(ascending=False).index

# Sort the DataFrame columns based on the sorted index
       sorted_modelaylık = modelaylık[sorted_index]


    
    if selected_model=='Mayıs 2024':
       sorted_index = modelaylık.iloc[0, :].sort_values(ascending=False).index

# Sort the DataFrame columns based on the sorted index
       sorted_modelaylık = modelaylık[sorted_index]

# Set custom colors for each bar
       color_map = px.colors.sequential.Viridis
       fig4 = px.bar(
    x=sorted_modelaylık.columns,
    y=sorted_modelaylık.iloc[0, :].values,
    text=sorted_modelaylık.iloc[0, :].values,
    color=np.arange(len(sorted_modelaylık.columns)),
    color_continuous_scale='Rainbow',
    labels={'y': 'Tahmin','x':'Model'},
    title="Model Predictions"
)
       fig4.update_layout(width=800, height=600)
       fig4.update_layout(coloraxis_showscale=False)
       fig4.update_layout(
       title="Mayıs Ayı Enflasyon Tahmini",
       showlegend=False
)
       fig4.update_traces(texttemplate='%{text:.2f}', textposition='outside', textangle=0)
       fig4.update_layout(font=dict(family="Arial Black", size=14, color="black"))
       st.plotly_chart(fig4)
    if selected_model=='Haziran 2024':
       sorted_index = modelaylık.iloc[1, :].sort_values(ascending=False).index

# Sort the DataFrame columns based on the sorted index
       sorted_modelaylık = modelaylık[sorted_index]

# Set custom colors for each bar
       color_map = px.colors.sequential.Viridis
       fig4 = px.bar(
    x=sorted_modelaylık.columns,
    y=sorted_modelaylık.iloc[1, :].values,
    text=sorted_modelaylık.iloc[1, :].values,
    color=np.arange(len(sorted_modelaylık.columns)),
    color_continuous_scale='Rainbow',
    labels={'y': 'Tahmin','x':'Model'},
    title="Model Predictions"
)
       fig4.update_layout(width=800, height=600)
       fig4.update_layout(coloraxis_showscale=False)
       fig4.update_layout(
       title="Haziran Ayı Enflasyon Tahmini",
       showlegend=False
)
       fig4.update_traces(texttemplate='%{text:.2f}', textposition='outside', textangle=0)
       fig4.update_layout(font=dict(family="Arial Black", size=14, color="black"))
       st.plotly_chart(fig4)
    if selected_model=='Temmuz 2024':
       sorted_index = modelaylık.iloc[2, :].sort_values(ascending=False).index

# Sort the DataFrame columns based on the sorted index
       sorted_modelaylık = modelaylık[sorted_index]

# Set custom colors for each bar
       color_map = px.colors.sequential.Viridis
       fig4 = px.bar(
    x=sorted_modelaylık.columns,
    y=sorted_modelaylık.iloc[2, :].values,
    text=sorted_modelaylık.iloc[2, :].values,
    color=np.arange(len(sorted_modelaylık.columns)),
    color_continuous_scale='Rainbow',
    labels={'y': 'Tahmin','x':'Model'},
    title="Model Predictions"
)
       fig4.update_layout(width=800, height=600)
       fig4.update_layout(coloraxis_showscale=False)
       fig4.update_layout(
       title="Temmuz Ayı Enflasyon Tahmini",
       showlegend=False
)
       fig4.update_traces(texttemplate='%{text:.2f}', textposition='outside', textangle=0)
       fig4.update_layout(font=dict(family="Arial Black", size=14, color="black"))
       st.plotly_chart(fig4)
    if selected_model=='Ağustos 2024':
       sorted_index = modelaylık.iloc[3, :].sort_values(ascending=False).index

# Sort the DataFrame columns based on the sorted index
       sorted_modelaylık = modelaylık[sorted_index]

# Set custom colors for each bar
       color_map = px.colors.sequential.Viridis
       fig4 = px.bar(
    x=sorted_modelaylık.columns,
    y=sorted_modelaylık.iloc[3, :].values,
    text=sorted_modelaylık.iloc[3, :].values,
    color=np.arange(len(sorted_modelaylık.columns)),
    color_continuous_scale='Rainbow',
    labels={'y': 'Tahmin','x':'Model'},
    title="Model Predictions"
)
       fig4.update_layout(width=800, height=600)
       fig4.update_layout(coloraxis_showscale=False)
       fig4.update_layout(
       title="Ağustos Ayı Enflasyon Tahmini",
       showlegend=False
)
       fig4.update_traces(texttemplate='%{text:.2f}', textposition='outside', textangle=0)
       fig4.update_layout(font=dict(family="Arial Black", size=14, color="black"))
       st.plotly_chart(fig4)
    if selected_model=='Eylül 2024':
       sorted_index = modelaylık.iloc[4, :].sort_values(ascending=False).index

# Sort the DataFrame columns based on the sorted index
       sorted_modelaylık = modelaylık[sorted_index]

# Set custom colors for each bar
       color_map = px.colors.sequential.Viridis
       fig4 = px.bar(
    x=sorted_modelaylık.columns,
    y=sorted_modelaylık.iloc[4, :].values,
    text=sorted_modelaylık.iloc[4, :].values,
    color=np.arange(len(sorted_modelaylık.columns)),
    color_continuous_scale='Rainbow',
    labels={'y': 'Tahmin','x':'Model'},
    title="Model Predictions"
)
       fig4.update_layout(width=800, height=600)
       fig4.update_layout(coloraxis_showscale=False)
       fig4.update_layout(
       title="Eylül Ayı Enflasyon Tahmini",
       showlegend=False
)
       fig4.update_traces(texttemplate='%{text:.2f}', textposition='outside', textangle=0)
       fig4.update_layout(font=dict(family="Arial Black", size=14, color="black"))
       st.plotly_chart(fig4)
    if selected_model=='Ekim 2024':
       sorted_index = modelaylık.iloc[5, :].sort_values(ascending=False).index

# Sort the DataFrame columns based on the sorted index
       sorted_modelaylık = modelaylık[sorted_index]

# Set custom colors for each bar
       color_map = px.colors.sequential.Viridis
       fig4 = px.bar(
    x=sorted_modelaylık.columns,
    y=sorted_modelaylık.iloc[5, :].values,
    text=sorted_modelaylık.iloc[5, :].values,
    color=np.arange(len(sorted_modelaylık.columns)),
    color_continuous_scale='Rainbow',
    labels={'y': 'Tahmin','x':'Model'},
    title="Model Predictions"
)
       fig4.update_layout(width=800, height=600)
       fig4.update_layout(coloraxis_showscale=False)
       fig4.update_layout(
       title="Ekim Ayı Enflasyon Tahmini",
       showlegend=False
)
       fig4.update_traces(texttemplate='%{text:.2f}', textposition='outside', textangle=0)
       fig4.update_layout(font=dict(family="Arial Black", size=14, color="black"))
       st.plotly_chart(fig4)
    if selected_model=='Kasım 2024':
       sorted_index = modelaylık.iloc[6, :].sort_values(ascending=False).index

# Sort the DataFrame columns based on the sorted index
       sorted_modelaylık = modelaylık[sorted_index]

# Set custom colors for each bar
       color_map = px.colors.sequential.Viridis
       fig4 = px.bar(
    x=sorted_modelaylık.columns,
    y=sorted_modelaylık.iloc[6, :].values,
    text=sorted_modelaylık.iloc[6, :].values,
    color=np.arange(len(sorted_modelaylık.columns)),
    color_continuous_scale='Rainbow',
    labels={'y': 'Tahmin','x':'Model'},
    title="Model Predictions"
)
       fig4.update_layout(width=800, height=600)
       fig4.update_layout(coloraxis_showscale=False)
       fig4.update_layout(
       title="Kasım Ayı Enflasyon Tahmini",
       showlegend=False
)
       fig4.update_traces(texttemplate='%{text:.2f}', textposition='outside', textangle=0)
       fig4.update_layout(font=dict(family="Arial Black", size=14, color="black"))
       st.plotly_chart(fig4)
    if selected_model=='Aralık 2024':
       sorted_index = modelaylık.iloc[7, :].sort_values(ascending=False).index

# Sort the DataFrame columns based on the sorted index
       sorted_modelaylık = modelaylık[sorted_index]

# Set custom colors for each bar
       color_map = px.colors.sequential.Viridis
       fig4 = px.bar(
    x=sorted_modelaylık.columns,
    y=sorted_modelaylık.iloc[7, :].values,
    text=sorted_modelaylık.iloc[7, :].values,
    color=np.arange(len(sorted_modelaylık.columns)),
    color_continuous_scale='Rainbow',
    labels={'y': 'Tahmin','x':'Model'},
    title="Model Predictions"
)
       fig4.update_layout(width=800, height=600)
       fig4.update_layout(coloraxis_showscale=False)
       fig4.update_layout(
       title="Aralık Ayı Enflasyon Tahmini",
       showlegend=False
)
       fig4.update_traces(texttemplate='%{text:.2f}', textposition='outside', textangle=0)
       fig4.update_layout(font=dict(family="Arial Black", size=14, color="black"))
       st.plotly_chart(fig4)
    
      

    
if page == "Hakkında":
    st.write("Geliştirici : Bora Kaya")

    st.markdown("""**[Inflation Forecast Twitter](https://twitter.com/AiInflatio15273)** """)

    st.markdown("""**[Linkedin](https://www.linkedin.com/in/bora-kaya/)** """)

    st.markdown("""**[Github](https://github.com/kaboya19/)** """)

if page == "Metodoloji":
    st.markdown("<div style='text-align: left;'>"
            "<h1>Metodoloji</h1>"
            "<p>Tahmin için 10 adet ekonomik veri kullanılmaktadır.</p>"
            "<p>1) 3 Aylık USD/TL Hareketli Ortalaması</p>"
            "<p>2) M2 Para Arzı (1 ay gecikmeli)</p>"
            "<p>3) M3 Para Arzı (1 ay gecikmeli)</p>"
            "<p>4) Motorin Fiyatı</p>"
            "<p>5) Politika Faizi</p>"
            "<p>6) Ortalama 3 Aylık Mevduat Faizi</p>"
            "<p>7) Toplam Kredi Hacmi(3 Aylık Hareketli Ortalama)</p>"
            "<p>8) Asgari Ücret Zam Oranı (Sadece zam yapılan aylar)</p>"
            "<p>9) Enflasyon Belirsizliği (TCMB Piyasa Katılımcıları Anketi 12 Ay Sonrası Enflasyon Beklentilerinin Standart Sapması)</p>"
            "<p>10) İşsizlik</p>"
            "<p>11) Aylık Enflasyon(Hedef Değişken)</p>"
            "<p>Her bir bağımsız değişkenin gelecek değerleri Prophet modeliyle tahmin edilmiş, bunlar 6 farklı Yapay Sinir Ağı modeliyle tahmin edilmiştir.Mevcut ay enflasyon tahmini için gerçek veriler,gelecek aylar için Prophet tahminleri kullanılmaktadır.</p>"
            "</div>", unsafe_allow_html=True)
    

if page=="Performans Tablomuz":

   plt.style.use("fivethirtyeight")
   gecmis=pd.DataFrame({"Aylık Enflasyon(%)":[4.75,3.43,3.28,2.93,6.70,4.53,3.16,3.18],"Tahmin(%)":[5.05,3.11,3.38,2.85,6.83,3.70,3.76,3.11]})
   gecmis=gecmis.set_index(pd.date_range(start="2023-09-30",periods=8,freq="M"))
   gecmis=gecmis.set_index(gecmis.index.strftime("%Y-%m"))

   fig, ax = plt.subplots(figsize=(12,8))
   gecmis.plot(kind="bar", ax=ax)

   plt.annotate("4.75", xy=(-0.3,gecmis.iloc[0,0]*0.95), fontweight="bold", fontsize=15)
   plt.annotate("5.05", xy=(0,gecmis.iloc[0,1]*0.95), fontweight="bold", fontsize=15)
   plt.annotate("3.43", xy=(0.7,gecmis.iloc[1,0]*0.95), fontweight="bold", fontsize=15)
   plt.annotate("3.11", xy=(1,gecmis.iloc[1,1]*0.95), fontweight="bold", fontsize=15)
   plt.annotate("3.28", xy=(1.7,gecmis.iloc[2,0]*0.95), fontweight="bold", fontsize=15)
   plt.annotate("3.38", xy=(2,gecmis.iloc[2,1]*0.97), fontweight="bold", fontsize=15)
   plt.annotate("2.93", xy=(2.7,gecmis.iloc[3,0]*0.97), fontweight="bold", fontsize=15)
   plt.annotate("2.85", xy=(3,gecmis.iloc[3,1]*0.93), fontweight="bold", fontsize=15)
   plt.annotate("6.70", xy=(3.7,gecmis.iloc[4,0]*0.95), fontweight="bold", fontsize=15)
   plt.annotate("6.83", xy=(4,gecmis.iloc[4,1]*0.97), fontweight="bold", fontsize=15)
   plt.annotate("4.53", xy=(4.7,gecmis.iloc[5,0]*0.95), fontweight="bold", fontsize=15)
   plt.annotate("3.70", xy=(5,gecmis.iloc[5,1]*0.95), fontweight="bold", fontsize=15)
   plt.annotate("3.16", xy=(5.65,gecmis.iloc[6,0]*0.95), fontweight="bold", fontsize=15)
   plt.annotate("3.76", xy=(6,gecmis.iloc[6,1]*0.95), fontweight="bold", fontsize=15)
   plt.annotate("3.18", xy=(6.6,gecmis.iloc[7,0]*0.95), fontweight="bold", fontsize=15)
   plt.annotate("3.11", xy=(7,gecmis.iloc[7,1]*0.95), fontweight="bold", fontsize=15)

   plt.legend(fontsize=15)
   plt.xticks(rotation=0, fontweight="bold", fontsize=15, color="black")

   st.pyplot(fig)



   

    