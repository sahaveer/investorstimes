#import plotly.io as pio
#pio.kaleido.scope.chromium_args += ("--single-process",)
#pio.kaleido.scope.mathjax = None

import os
import instaimage
# from PIL import ImageFont
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import pandas as pd

width_val = 1120 #1024
height_val = 360 #574
#aspect_ratio = 16/9  # For a 16:9 aspect ratio
#height_val = width_val / aspect_ratio
# TARGET_FOLDER = "C:/Users/sahaveer/OneDrive/Documents/bhavcopy/"

#write_on_chart = "<i>@itimesalgo        </i>"
write_on_chart = "<i>https://itimesalgo.streamlit.app/</i>"

def check_rows(df, rows):
    """Check if all rows exist in the DataFrame index."""
    missing = [r for r in rows if r not in df.index]
    if missing:
        st.warning(f"Data missing for: {', '.join(missing)}")
        return False
    return True



def go_bar(df, row_name,color_bar,comp_Name,filename):
    if not check_rows(df, [row_name]):
        return
    save_as = f"{filename} {row_name}"
    #fig = ff.create_table(df)
    #st.plotly_chart(fig)
    #st.write(df)                                                   # this is givng data conversion error sometimes
    fig = go.Figure(data = [go.Bar(x = df.columns,y = df.loc[row_name],
                                   text = df.loc[row_name], textposition = 'auto')])
    # go.bar has another attribute - hovertext = ['27% market share', '24% market share', '19% market share']
    fig.update_traces(marker_color=color_bar, marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=1, texttemplate='%{text:.3s}', textposition='outside', textfont=dict(size=18), textfont_color='yellow')
    fig.update_layout(autosize=True, paper_bgcolor="#16181A",plot_bgcolor="#23282D",
                      height=height_val,width=width_val,
                      margin = dict(l=0,r=0,t=0,b=0,pad=10),
                      title={'font':{ 'color':"#e25f5b"},
                             'text': "<b>" + comp_Name.upper() + "</b> : <i>" +  save_as.upper() + '</i>',
                             'y': 0.99,'x': 0.5,'xanchor': 'right','yanchor': 'top'},
                      xaxis_tickfont_size=14,
                      xaxis=dict(showgrid=False,tickfont=dict(color='white'),),
                      yaxis=dict(showgrid=False, title= write_on_chart + '    ' + row_name +' in cr',titlefont_size=16,tickfont_size=1,tickfont=dict(color='white'),),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                      bargap=0.15,font_color = "white")     #legend=dict(x=0,y=1.0,bgcolor='rgba(255, 255, 255, 0)',bordercolor='rgba(255, 255, 255, 0)'),
    # new_df = pd.concat([df.loc[row_name]], axis=1).transpose()
    st.plotly_chart(fig,use_container_width=True)
    # col1, col3 = st.columns([2,1])
    # with col1:
    #     title_text = f"{comp_Name}" # comp_Name.upper() + " " + save_as
    #     key_have = f"GoBar {save_as}"
    #     description = st.text_area(label="👉 Description", value="", height=15,key = key_have)
    # with col3:
    #     if st.button(f'{save_as}.png'):
    #         image_path = './Downloadimages/' + comp_Name.upper() + " " + save_as.upper() + ".png"
    #         savenameas = os.path.basename(image_path)
    #         print("TRYING TO SAVE IMAGE")
    #         fig.update_layout(autosize=True, paper_bgcolor="#16181A", plot_bgcolor="#23282D",)
    #         fig.write_image(image_path, width = 1080, height = 1080)
    #         print("Saved as image")
    #         instaimage.create_instaimage(title_text,description,image_path)

    #fig.write_image("./Downloadimages/fig1.png")
    #st.subheader('Downloads:')
    #generate_html_Download_link(fig)

def both_lines(df,row1,row2,color_bar,color_line,comp_Name,filename):
    if not check_rows(df, [row1, row2]):
        return
    save_as = f"{filename} {row1} {row2}"
    save_as = save_as.replace('%','')
    dat_rows = [df.loc[row1], df.loc[row2]]
    new_df = pd.concat(dat_rows, keys=[row1, row2], axis=1)
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=new_df.index, y=new_df[row1], name=row1, text=new_df[row1]),secondary_y=False)
    fig.update_traces(marker_color=color_bar, marker_line_color='rgb(8,48,107)',
                      marker_line_width=2, opacity=1, texttemplate='%{text:.1s}', textposition='top left', textfont=dict(size=18), textfont_color='yellow')
    fig.add_trace(go.Line(x=new_df.index, y=new_df[row2], name=row2, text=new_df[row2]),secondary_y=True)
    # Add figure title
    fig.update_layout(autosize=True, paper_bgcolor="#16181A",plot_bgcolor="#23282D",
                      height=height_val,width=width_val,
                      margin = dict(l=0,r=0,t=0,b=0, pad=10),
                      title={'font':{'color':"#e25f5b"},'text': "<b>" + comp_Name.upper() + " " + save_as.upper() + "</b> : <i>" + '</i>',
                             'y': 0.99, 'x': 0.5, 'xanchor': 'right', 'yanchor': 'top'},
                      #xaxis_tickfont_size=14,
                      xaxis=dict(showgrid=False, title=row1 , titlefont_size=16, tickfont_size=1),
                      yaxis=dict(showgrid=False, title=row2 , titlefont_size=16, tickfont_size=1),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                      bargap=0.15)  # legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),bargap = 0.15)
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>" + row1 + "</b>", secondary_y=False, showgrid=False,tickfont=dict(color='white'))
    fig.update_yaxes(title_text=write_on_chart + '    ' +"<b>" + row2 + "</b>", secondary_y=True, showgrid=False,tickfont=dict(color='white'))
    fig.update_xaxes(tickfont=dict(color='yellow'),)
    st.plotly_chart(fig, use_container_width=True)
    new_df = new_df.transpose()

    col1, col3 = st.columns([1,1])
    # with col1:
    #     title_text = f"{comp_Name}" #comp_Name.upper() + " " + save_as
    #     key_have = f"bothlines {save_as}"  
    #     description = st.text_area(label="👉 Description", value="", height=68,key = key_have)
    # with col3:
    #     if st.button(f'{save_as}.png', key=save_as):
    #         image_path = './Downloadimages/' + comp_Name.upper() + " " + save_as.upper() + ".png"
    #         savenameas = os.path.basename(image_path)
    #         print("TRYING TO SAVE IMAGE")
    #         fig.update_layout(autosize=True, paper_bgcolor="#16181A", plot_bgcolor="#23282D",)
    #         fig.write_image(image_path, width = 1080, height = 1080)
    #         print("Saved as image")
    #         instaimage.create_instaimage(title_text,description,image_path)

def bar_line(df,row1,row2,color_bar,comp_Name,filename):
    if not check_rows(df, [row1, row2]):
        return
    save_as = f"{filename} {row1} {row2}"
    save_as = save_as.replace('%','')
    dat_rows = [df.loc[row1], df.loc[row2]]
    new_df = pd.concat(dat_rows, keys=[row1, row2], axis=1)
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=new_df.index, y=new_df[row1], name=row1, textposition='auto', text=new_df[row1]),
                  secondary_y=False)
    fig.update_traces(marker_color=color_bar, marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=1, texttemplate='%{text:.3s}', textposition='outside', textfont=dict(size=18), textfont_color='yellow')
    fig.add_trace(go.Scatter(x=new_df.index, y=new_df[row2], name=row2, text=new_df[row2]),
                  secondary_y=True)
    # Add figure title
    fig.update_layout(autosize=True, paper_bgcolor="#16181A",plot_bgcolor="#23282D",
                      height=height_val,width=width_val,
                      margin = dict(l=0,r=0,t=0,b=0, pad=10),
                      title={'font':{'color':"#e25f5b"},'text': "<b>" + comp_Name.upper() + "</b> : <i>" + save_as.upper() + ' Report</i>',
                             'y': 0.99, 'x': 0.5, 'xanchor': 'right', 'yanchor': 'top'},
                      xaxis_tickfont_size=14,
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                      bargap=0.15)  # legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),bargap = 0.15)
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>" + row1 + "</b>", secondary_y=False, showgrid=False,tickfont=dict(color='white'))
    fig.update_yaxes(title_text=write_on_chart + '    ' +"<b>" + row2 + "</b>", secondary_y=True, showgrid=False,tickfont=dict(color='white'))
    fig.update_xaxes(tickfont=dict(color='white'),)
    st.plotly_chart(fig, use_container_width=True)
    new_df = new_df.transpose()
    col1, col3 = st.columns([2,1])
    # with col1:
    #     title_text = f"{comp_Name}" #comp_Name.upper() + " " + save_as
    #     key_have = f"barline {save_as} "
    #     description = st.text_area(label="👉 Description", value="", height=68,key = key_have)
    # with col3:
    #     if st.button(f'{save_as}.png', key=save_as):
    #         image_path = './Downloadimages/' + comp_Name.upper() + " " + save_as.upper() + ".png"
    #         savenameas = os.path.basename(image_path)
    #         print("TRYING TO SAVE IMAGE")
    #         fig.update_layout(autosize=True, paper_bgcolor="#16181A", plot_bgcolor="#23282D",)
    #         fig.write_image(image_path, width = 1080, height = 1080)
    #         print("Saved as image")
    #         instaimage.create_instaimage(title_text,description,image_path)

def qoq_growth(df,row_name,color_bar,comp_Name,filename):
    if not check_rows(df, [row_name]):
        return
    save_as = f"{filename}  {row_name}".upper()
    col_chart1, col2_chart = st.columns([1, 5])
    temp_df = df.loc[row_name]
    df_qoq = (temp_df.pct_change() * 100)
    df_qoq.name = row_name + '_QoQ'
    df_qoq = pd.DataFrame(df_qoq).transpose()
    df2 = pd.concat([df, df_qoq], axis=0)
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # adds bar chart
    fig.add_trace(go.Bar(x=df2.columns, y=df2.loc[row_name], name=row_name, textposition = 'auto',text = df.loc[row_name]),
                   secondary_y=False)
    fig.update_traces(marker_color=color_bar, marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=1, texttemplate='%{text:.3s}', textposition='outside', textfont=dict(size=18), textfont_color='yellow')
    # adds line chart
    fig.add_trace(go.Scatter(x=df2.columns, y=df2.iloc[-1], name=row_name + " QoQ", text = df.iloc[-1]),
                   secondary_y=True)
    # Add figure title
    fig.update_layout(autosize=True, paper_bgcolor="#16181A",plot_bgcolor="#23282D",
                      height=height_val, width=width_val,
                      margin=dict(l=0, r=0, t=0, b=0, pad=10),
                      title={'font':{'color':"#e25f5b"},'text': "<b>" + comp_Name.upper() + "</b> : <i>" + save_as.upper() + '</i>',
                              'y': 0.99, 'x': 0.5, 'xanchor': 'right', 'yanchor': 'top'},
                       xaxis_tickfont_size=14,
                       legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                       bargap=0.15)#legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01),bargap = 0.15)
    # Set y-axes titles
    fig.update_yaxes(title_text=write_on_chart + '    ' +"<b>" + row_name + "</b> in cr ", secondary_y=False,showgrid=False,tickfont=dict(color='white'))
    fig.update_yaxes(title_text="<b> QoQ </b> in % ", secondary_y=True,showgrid=False,tickfont=dict(color='white'))

    # Set x-axis tick color and font color
    fig.update_xaxes(tickfont_color='white')  # Set font color for x-axis tick labels

    new_df = pd.concat([df2.loc[row_name],df2.iloc[-1]], axis=1).transpose()
    latest_sales = new_df.iloc[0, -1]
    qoq = new_df.iloc[1,-1]
    if qoq > 0:
        write_annotation = f"{comp_Name} has clocked {row_name} of {latest_sales:.1f}cr up by {qoq:.1f}% with the previous Q1FY24"
    else:
        write_annotation =   f"{comp_Name} has clocked {row_name} of {latest_sales:.1f}cr down by {qoq:.1f}% with the previous Q1FY24"

    #fig.add_annotation(text=write_annotation, x=0, y=1, xref="paper", yref="paper",showarrow=False, font=dict(size=18, color=color_bar))
    #fig.update_layout(annotations=[dict(text=write_annotation,x=0,y=1,xref='paper',yref='paper',showarrow=False,font=dict(size=18, color=color_bar))])
    st.plotly_chart(fig,use_container_width=True)

    # col1, col3 = st.columns([2,1])
    # with col1:
    #     title_text = f"{comp_Name}" #comp_Name.upper() + " " + save_as
    #     key_have = f"qoq {save_as} "
    #     description = st.text_area(label="👉 Description", value="", height=68,key = key_have)
    # with col3:
    #     if st.button(f'{save_as}.png'):
    #         image_path = './Downloadimages/' + comp_Name.upper() + " " + save_as.upper() + ".png"
    #         savenameas = os.path.basename(image_path)
    #         print("TRYING TO SAVE IMAGE")
    #         fig.update_layout(autosize=True, paper_bgcolor="#16181A", plot_bgcolor="#23282D",)
    #         fig.write_image(image_path, width = 1080, height = 1080)
    #         print("Saved as image")
    #         instaimage.create_instaimage(title_text,description,image_path)

    #st.subheader('Downloads:')
    #excel_link_to_download(df2)
    #generate_html_Download_link(fig)


#not in use
def peer_bar(df,Name,comp1_Name,comp2_Name):   #this has 2 series concatinated with key names
    bar_list = list(df.columns)
    fig = go.Figure(data=[go.Bar(name=bar_list[0], x=df.index, y=df[bar_list[0]], textposition='auto', marker={'color': "#3EC1CD"}),
                          go.Bar(name=bar_list[1], x=df.index, y=df[bar_list[1]], textposition='auto', marker={'color': "#EF3A4C"})])
    # Change the bar mode
    fig.update_layout(autosize=True,barmode='group', bargroupgap=0.1,
                      paper_bgcolor="#16181A", plot_bgcolor="#23282D",
                      height=height_val, width=width_val,
                      margin = dict(l=0,r=0,t=0,b=0, pad=10),
                      title={'font':{'color':"#e25f5b"},'text': '<i>@itimesalgo        ' + Name + " Comparision : </i> <b>" + comp1_Name + '/' + comp2_Name + '</b>',
                             'y': 0.99, 'x': 0.5, 'xanchor': 'right', 'yanchor': 'top'},
                      xaxis_tickfont_size=14,
                      xaxis=dict(showgrid=False,tickfont=dict(color='white'),),
                      yaxis=dict(showgrid=False, title=write_on_chart + '    ' +'INR (cr)', titlefont_size=16, tickfont_size=14,tickfont=dict(color='white'), ),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                      bargap=0.1)   # this barmode = 'group  stack  'relative''
    st.plotly_chart(fig, use_container_width=True)
    new_df = pd.concat([df[bar_list[0]],df[bar_list[1]]], axis=1).transpose()

    col1, col3 = st.columns([6,4])
    #with col1:
        #with st.expander(Name + " DATA"):
            #st.dataframe(new_df.style.format(formatter="{:.1f}"))
    with col3:
        if st.button(f'{Name}.png',key=f'{Name}.png'):
            image_path = './Downloadimages/' + comp1_Name.upper() + '/' + comp2_Name.upper() + " " + Name + ".png"
            savenameas = os.path.basename(image_path)
            print("TRYING TO SAVE IMAGE")
            fig.write_image(image_path, width = 1080, height = 1080)
            print("Saved as image")
#not in use
def group_3_bars(df,row1,row2,row3,comp_Name,filename):
    if not check_rows(df, [row1, row2, row3]):
        return
    save_as = f"{filename}  {row1}  {row2}  {row3}".upper()
    dat_rows = [df.loc[row1], df.loc[row2],df.loc[row3]]
    new_df = pd.concat(dat_rows, keys=[row1, row2,row3], axis=1)
    # Create the text labels for each bar
    text_labels_row1 = new_df[row1].tolist()
    text_labels_row2 = new_df[row2].tolist()
    text_labels_row3 = new_df[row3].tolist()

    # Create the bar chart with text labels for each trace
    fig = go.Figure(data=[
        go.Bar(
            name=row1,
            x=new_df.index,
            y=new_df[row1],
            text=text_labels_row1,  # Provide the text labels for row1 bars
            textposition='auto',
            marker={'color': "#3EC1CD"}
        ),
        go.Bar(
            name=row2,
            x=new_df.index,
            y=new_df[row2],
            text=text_labels_row2,  # Provide the text labels for row2 bars
            textposition='auto',
            marker={'color': "#EF3A4C"}
        ),
        go.Bar(
            name=row3,
            x=new_df.index,
            y=new_df[row3],
            text=text_labels_row3,  # Provide the text labels for row2 bars
            textposition='auto',
            marker={'color': "#53B987"}
        ),

    ])

    # Change the bar mode
    fig.update_layout(
        autosize=True,
        barmode='group',
        bargroupgap=0.1,
        paper_bgcolor="#16181A",
        plot_bgcolor="#23282D",
        height=height_val,
        width=width_val,
        margin=dict(l=0, r=0, t=0, b=0, pad=10),
        title={'font': {'color': "#e25f5b"},
               'text': "<b>" + comp_Name.upper() + ' : </b> <i>' + save_as + '</i>',
               'y': 0.99, 'x': 0.5, 'xanchor': 'right', 'yanchor': 'top'},
        xaxis_tickfont_size=14,
        xaxis=dict(showgrid=False, tickfont=dict(color='white')),
        yaxis=dict(showgrid=False, title=write_on_chart + '    ' +'INR (cr)', titlefont_size=16, tickfont_size=14,
                   tickfont=dict(color='white')),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        bargap=0.1
    )

    # Customize text font color and size
    fig.update_traces(textfont=dict(color='yellow', size=14))
    st.plotly_chart(fig, use_container_width=True)
    new_df = new_df.transpose()

    col1, col3 = st.columns([6,4])
    #with col1:
        #with st.expander(row1 + "/" + row2 + " DATA"):
            #st.dataframe(new_df.style.format(formatter="{:.1f}"))
    with col3:
        if st.button(f'{save_as}.png'):
            image_path = './Downloadimages/' + comp_Name.upper() + " " + save_as +".png"
            savenameas = os.path.basename(image_path)
            print("TRYING TO SAVE IMAGE")
            fig.write_image(image_path, width = 1080, height = 1080)
            print("Saved as image")

def group_2_bars(df,row1,row2,comp_Name,filename):
    if not check_rows(df, [row1, row2]):
        return
    save_as = f"{comp_Name} {filename} {row1} {row2}"
    dat_rows = [df.loc[row1], df.loc[row2]]
    # st.dataframe(dat_rows)
    new_df = pd.concat(dat_rows, keys=[row1, row2], axis=1)
    # Create the text labels for each bar
    text_labels_row1 = new_df[row1].tolist()
    text_labels_row2 = new_df[row2].tolist()

    # Create the bar chart with text labels for each trace
    fig = go.Figure(data=[
        go.Bar(
            name=row1,
            x=new_df.index,
            y=new_df[row1],
            text=text_labels_row1,  # Provide the text labels for row1 bars
            textposition='auto',
            marker={'color': "#3EC1CD"}
        ),
        go.Bar(
            name=row2,
            x=new_df.index,
            y=new_df[row2],
            text=text_labels_row2,  # Provide the text labels for row2 bars
            textposition='auto',
            marker={'color': "#EF3A4C"}
        ),
    ])

    # Change the bar mode
    fig.update_layout(
        autosize=True,
        barmode='group',
        bargroupgap=0.1,
        paper_bgcolor="#16181A",
        plot_bgcolor="#23282D",
        height=height_val,
        width=width_val,
        margin=dict(l=0, r=0, t=0, b=0, pad=10),
        title={'font': {'color': "#e25f5b"},
               'text': "<b>" + comp_Name.upper() + ' : </b> <i>' + save_as + '</i>',
               'y': 0.99, 'x': 0.5, 'xanchor': 'right', 'yanchor': 'top'},
        xaxis_tickfont_size=14,
        xaxis=dict(showgrid=False, tickfont=dict(color='white')),
        yaxis=dict(showgrid=False, title=write_on_chart + '    ' +'INR (cr)', titlefont_size=16, tickfont_size=14,
                   tickfont=dict(color='white')),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        bargap=0.1
    )

    # Customize text font color and size
    fig.update_traces(textfont=dict(color='yellow', size=14))
    st.plotly_chart(fig, use_container_width=True)
    new_df = new_df.transpose()

    col1, col3 = st.columns([2,1])
    #with col1:
        #with st.expander(row1 + "/" + row2 + " DATA"):
            #st.dataframe(new_df.style.format(formatter="{:.1f}"))
    # with col3:
    #     if st.button(f'{save_as}.png'):
    #         image_path = './Downloadimages/' + comp_Name.upper() + " " + save_as +".png"
    #         savenameas = os.path.basename(image_path)
    #         print("TRYING TO SAVE IMAGE")
    #         fig.write_image(image_path, width = 1080, height = 1080)
    #         print("Saved as image")
    # with col1:
    #     title_text = f"{comp_Name}" #comp_Name.upper() + " " + save_as
    #     key_have = f"Group2bars {save_as}"
    #     description = st.text_area(label="👉 Description", value="", height=68,key = key_have)
    # with col3:
    #     if st.button(f'{save_as}.png', key=save_as):
    #         image_path = './Downloadimages/' + comp_Name.upper() + " " + save_as.upper() + ".png"
    #         savenameas = os.path.basename(image_path)
    #         print("TRYING TO SAVE IMAGE")
    #         fig.update_layout(autosize=True, paper_bgcolor="#16181A", plot_bgcolor="#23282D",)
    #         fig.write_image(image_path, width = 1080, height = 1080)
    #         print("Saved as image")
    #         instaimage.create_instaimage(title_text,description,image_path)

# THIS IS SPECIFICALLY DESIGNED FOR CASHFLOWs, Where fixed 4 rows are there
def go_group_bar(df, row_name,color_bar,filename):
    save_as = f"{filename}  {row_name}".upper()
    # Sample data
    bar_list = list(df.index)

    # Create the bar chart with text labels and customize text font size and color
    fig = go.Figure(data=[
        go.Bar(
            name=bar_list[0],
            x=df.columns,
            y=df.iloc[0],
            textposition='auto',
            text=df.iloc[0],
            textfont=dict(
                size=24,  # Set font size for the text inside bars
                color='yellow'  # Set font color for the text inside bars
            )
        ),
        go.Bar(
            name=bar_list[1],
            x=df.columns,
            y=df.iloc[1],
            textposition='auto',
            text=df.iloc[1],
            textfont=dict(
                size=24,  # Set font size for the text inside bars
                color='yellow'  # Set font color for the text inside bars
            )
        ),
        go.Bar(
            name=bar_list[2],
            x=df.columns,
            y=df.iloc[2],
            textposition='auto',
            text=df.iloc[2],
            textfont=dict(
                size=24,  # Set font size for the text inside bars
                color='yellow'  # Set font color for the text inside bars
            )
        ),
        go.Bar(
            name=bar_list[3],
            x=df.columns,
            y=df.iloc[3],
            textposition='auto',
            text=df.iloc[3],
            textfont=dict(
                size=24,  # Set font size for the text inside bars
                color='yellow'  # Set font color for the text inside bars
            )
        )
    ])

    # Change the bar mode and update layout properties
    fig.update_layout(
        autosize=True,
        barmode='group',
        bargroupgap=0.1,
        paper_bgcolor="#16181A",
        plot_bgcolor="#23282D",
        height=height_val,
        width=width_val,
        margin=dict(l=0, r=0, t=0, b=0, pad=10),
        title={'font': {'color': "#e25f5b"}, 'text': '<i>@itimesalgo        </i> <b>' + save_as + '</b> <i>',
               'y': 0.99, 'x': 0.5, 'xanchor': 'right', 'yanchor': 'top'},
        xaxis_tickfont_size=14,
        xaxis=dict(showgrid=False, tickfont=dict(color='white')),
        yaxis=dict(showgrid=False, title=write_on_chart + '    ' +'INR (cr)', titlefont_size=16, tickfont_size=14, tickfont=dict(color='white')),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    # Show the plot
    st.plotly_chart(fig, use_container_width=True)
