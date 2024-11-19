import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title="Программирование урожая КАТРУ с учетом фитосанитарных работ")
# Load your DataFrame
df =pd.read_excel("https://github.com/sc-katu/yieldprogramming/raw/main/2023_yield_programming.xlsx")


# Main content
st.title('Программирование урожая с учетом фитосанитарных работ')
markdown_table = """
    | Уровень защиты                  | Описание                                       |
    |-----------------------|----------------------------------------------------|
    | Экологизированный вариант            | Протравка семян - Клорид Экстра-1,5, к.с. + Альбит-0,1, т.пс; по вегетации - Эфир Экстра 905, к.э.-0,3 + Галлантный 75%-0,010, с.т.с. + Грами Супер-0,6, к.э. + Альбит-0,015, т.пс; дополнительно – Пропикон-0,5, к.э. + Инсект-0,15, с.к. + Агростимулин-0,04, в.с.р.            |
    | Эталон         | ОПротравка семян – Юнта-1,75,к.с.; по вегетации - Эфир Экстра 905-0,5, к.э. + Галлантный-0,015, 75%, с.т.с. + Грами Супер-0,6, к.э.; дополнительно – Про-пикон-0,5, к.э. + Инсект-0,15, с.к.                      |
    | Фон        | 20, 30, 35, 40 ц/га      |
    | Посев            | Производился по пару и по стерне               |
    
    """
    
    # Display the Markdown table
st.markdown(markdown_table)


    # Create filters for 'Сорт культура', 'Фон', 'Посев', 'Уровень удобрений', 'Уровень защиты'
crop_varieties = df['Сорт культура'].unique()
selected_crop_variety = st.selectbox('Выберите Сорт:', crop_varieties)

subset_df = df[df['Сорт культура'] == selected_crop_variety]

background_varieties = subset_df['Фон'].unique()
selected_background = st.selectbox('Выберите фон', background_varieties)

subset_df = subset_df[subset_df['Фон'] == selected_background]

sowing_varieties = subset_df['Посев'].unique()
selected_sowing = st.selectbox('Выберите посев', sowing_varieties)

subset_df = subset_df[subset_df['Посев'] == selected_sowing]

fertilization_levels = subset_df['Уровень удобрений'].unique()
selected_fertilization = st.selectbox('Выберите уровень удобрений:', fertilization_levels)

subset_df = subset_df[subset_df['Уровень удобрений'] == selected_fertilization]

protection_levels = subset_df['Уровень защиты'].unique()
selected_protection = st.selectbox('Выберите уровень:', protection_levels)

subset_df = subset_df[subset_df['Уровень защиты'] == selected_protection]

if st.button("Рассчитать урожайность"):
    if not subset_df.empty:
        # Display selected row as a box
        #st.subheader('Выбранные параметры')
        selected_row = subset_df.index.item()
        print(type(selected_row))
       
        
        selected_data = subset_df.loc[selected_row]
        #st.write(selected_data)
    
        # Display 'Максимально возможная урожайность' and 'Разница урожайности'
        st.subheader('Максимально возможная урожайность и Возможное увеличение урожая в га')
        st.write(f"<b>Рассчитанная урожайность</b>: {round(selected_data['Рассчитанная урожайность'],2)} ц/га",unsafe_allow_html=True)
        st.write(f"<b>Максимально возможная урожайность</b>: {round(selected_data['Максимально возможная урожайность'],2)} ц/га",unsafe_allow_html=True)
        st.write(f"<b>Возможное увеличение урожая на</b>: {round(selected_data['Разница урожайности'],2)} ц/га",unsafe_allow_html=True)
    
        # Create a bar plot for 'Инсектициды', 'Гербициды', 'Фунгициды'
        st.subheader('Влияние защитных мероприятий на урожай')
        pesticide_columns = ['Инсектициды', 'Гербициды', 'Фунгициды','Протравка семян']
        pesticide_data = selected_data[pesticide_columns]
        plt.figure(figsize=(10, 6))
        plt.bar(pesticide_data.index, pesticide_data.values)
        plt.xlabel('Тип  обработки')
        plt.ylabel('ц/га')
        plt.title('Увеличение урожая в ц/га')
        st.pyplot()
        st.set_option('deprecation.showPyplotGlobalUse', False)
       
    
        # Create a Plotly Express bar chart
        custom_colors = ['#FF5712', '#33FF', '#5733FF', '#33FFFF']
        fig = px.bar(pesticide_data, x=pesticide_data.index, y=pesticide_data.values, title='Увеличение урожая в ц/га',color_discrete_sequence=custom_colors,
                     animation_group=pesticide_data.index)
        fig.update_traces(texttemplate='%{y} га', textposition='outside')
        # Customize the chart layout
        fig.update_layout(
            xaxis_title='Тип обработки',
            yaxis_title='ц/га',
            width=800,        # Width in pixels
            height=600,
            showlegend=False  # Hide the legend
        )
        
        # Display the chart using Plotly
        st.plotly_chart(fig)




# # Sidebar for selecting columns
# st.sidebar.title('Select Columns')
# selected_columns = st.sidebar.multiselect(
#     'Choose columns to display:',
#     df.columns
# )

# # Main content
# st.title('Программирование урожая')

# if not selected_columns:
#     st.warning('Please select at least one column from the sidebar.')
# else:
#     # Create a subset of the DataFrame with selected columns
#     subset_df = df[selected_columns]

#     # Create filters for 'Сорт культура', 'Фон', 'Посев', 'Уровень удобрений', 'Уровень защиты'
#     crop_varieties = subset_df['Сорт культура'].unique()
#     selected_crop_variety = st.selectbox('Select a crop variety:', crop_varieties)

#     subset_df = subset_df[subset_df['Сорт культура'] == selected_crop_variety]

#     if not subset_df.empty:
#         backgrounds = subset_df['Фон'].unique()
#         selected_background = st.selectbox('Select a background:', backgrounds)

#         subset_df = subset_df[subset_df['Фон'] == selected_background]

#         sowings = subset_df['Посев'].unique()
#         selected_sowing = st.selectbox('Select a sowing:', sowings)

#         subset_df = subset_df[subset_df['Посев'] == selected_sowing]

#         fertilization_levels = subset_df['Уровень удобрений'].unique()
#         selected_fertilization = st.selectbox('Select a fertilization level:', fertilization_levels)

#         subset_df = subset_df[subset_df['Уровень удобрений'] == selected_fertilization]

#         protection_levels = subset_df['Уровень защиты'].unique()
#         selected_protection = st.selectbox('Select a protection level:', protection_levels)

#         subset_df = subset_df[subset_df['Уровень защиты'] == selected_protection]

#         # Display selected row as a box
#         st.subheader('Selected Row')
#         selected_row = st.selectbox('Select a row:', subset_df.index)
#         selected_data = subset_df.loc[selected_row]
#         st.write(selected_data)

#         # Display 'Максимально возможная урожайность' and 'Разница урожайности'
#         st.subheader('Максимально возможная урожайность and Разница урожайности')
#         st.write(f"Максимально возможная урожайность: {selected_data['Максимально возможная урожайность']}")
#         st.write(f"Разница урожайности: {selected_data['Разница урожайности']}")

#         # Create a bar plot for 'Инсектициды', 'Гербициды', 'Фунгициды'
#         st.subheader('Pesticide Usage Plot')
#         pesticide_columns = ['Инсектициды', 'Гербициды', 'Фунгициды']
#         pesticide_data = selected_data[pesticide_columns]
#         plt.figure(figsize=(10, 6))
#         plt.bar(pesticide_data.index, pesticide_data.values)
#         plt.xlabel('Pesticide Type')
#         plt.ylabel('Usage')
#         plt.title('Pesticide Usage')
#         st.pyplot()

#     else:
#         st.warning(f"No data available for the selected criteria.")

