import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de la página
st.set_page_config(
    page_title="Análisis de la Ethical Black Box",
    page_icon="📊",
    layout="wide"
)

# Logo en la parte superior centrado
c1, c2, c3 = st.columns([1, 3, 1])

with c1:
    st.image('images/logo_amor_azulupm.png', width=300)

# Logo y título
c1, c2, c3 = st.columns([1, 3, 1])
    
with c2:
    st.caption("")
    new_title = '''
    <div style="
        text-align: center;
        color: #00629b;
        font-size: 80px;
        font-weight: bold;
        font-family: 'Arial', sans-serif;
        background: linear-gradient(90deg, rgba(0,98,155,1) 0%, rgba(0,170,224,1) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    ">
        Ethical Black Box
    </div>
    <hr style="border: 1px solid #00629b;">
    '''
    st.markdown(new_title, unsafe_allow_html=True)

# Cargar CSS
css_file = open("config/estiloMain.css", "r").read()
st.markdown(f'<style>{css_file}</style>', unsafe_allow_html=True)

# Sidebar para navegación
with st.sidebar:
    tab_title = '<p style="color:#00629b; font-size: 40px; margin-bottom: 0;">Control Panel</p>'
    st.markdown(tab_title, unsafe_allow_html=True)
    
    st.image('images/logo_gsi.png', width=75)
    
    st.markdown(
        """
        <div style="font-size: 20px; margin-top: 10px;">
            App created by 
            <a href="https://gsi.upm.es" style="color: #00629b;">Intelligent Systems Group</a>.
        </div>
        """,
        unsafe_allow_html=True
    )

# Función para cargar el archivo CSV
def cargar_csv():
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        return data
    return None

# Tabs
tab1, tab2, tab3 = st.tabs(["Upload CSV", "Robot Statistics", "Human Statistics"])

with tab1:
    st.markdown('<div style="color:#00629b; font-size: 40px;">Upload CSV file</div>', unsafe_allow_html=True)
    data = cargar_csv()
    if data is not None:
        st.success("File successfully uploaded")
        st.markdown('<div style="color:#00629b; font-size: 35px;">CSV analysis</div>', unsafe_allow_html=True)
        st.dataframe(data)

    st.markdown('<div style="color:#00629b; font-size: 40px;">Knowledge Graph</div> <hr style="border: 1px solid #00629b; width: 50%; margin-left: 0;">', unsafe_allow_html=True)
    if data is not None:
        # Leer el archivo HTML
        with open("graph.html", "r", encoding='utf-8') as f:
            html_content = f.read()

        # Mostrar el contenido HTML en Streamlit
        components.html(html_content, height=600)
    else:
        st.warning("Please upload a CSV file in the 'Upload CSV' tab")

with tab2:
    st.markdown('<div style="color:#00629b; font-size: 35px;">Robot Statistics</div>', unsafe_allow_html=True)
    if data is not None:
        if 'node1' in data.columns and 'node2' in data.columns:
            # Contar robots y humanos
            robots = data[data['node2'] == 'Robot']['node1'].unique()

            num_robots = len(robots)
            
            st.markdown(f'<div style="color:#00a9e0; font-size: 20px;">Number of Robots: {num_robots}</div>', unsafe_allow_html=True)
            st.markdown(f"<div class='icon'> {'🤖 ' * num_robots}</div>", unsafe_allow_html=True)
            st.markdown(f'<div style="color:#00a9e0; font-size: 20px;"> </div>', unsafe_allow_html=True)
            
        # Lógica adicional para obtener el valor de label para cada robot y humano
        st.markdown('<div style="color:#00629b; font-size: 35px;">Information about each Robot</div>', unsafe_allow_html=True)
        if 'node1' in data.columns and 'node2' in data.columns and 'label' in data.columns:
            # Filtrar los nombres de los robots
            robot_names = data[data['node2'] == 'Robot']['node1'].unique()

            results = []
            for robot in robot_names:
                label_value = data[(data['node1'] == robot) & (data['label'] == 'type')]['node2'].values
                label_value1 = data[(data['node1'] == robot) & (data['label'] == 'label')]['node2'].values
                if len(label_value) > 0:
                    results.append((robot, label_value[0], label_value1[0]))

            if results:
                results_data = pd.DataFrame(results, columns=['Robot', 'Label Value', 'name'])
                st.dataframe(results_data)
            else:
                st.warning("No se encontraron valores para los robots especificados.")

            if 'label' in data.columns and 'node1' in data.columns and 'node2' in data.columns:
                
                def get_interactions_for_all_robots(data):
                    # Obtener todos los robots
                    robots = data[data['node2'] == 'Robot']['node1'].unique()
    
                    # Inicializar listas para almacenar los resultados
                    robots_list = []
                    interaction_list = []
                    date_interaction_list = []
                    emotional_state_list = []
                    date_emotional_state_list = []

                    # Iterar sobre cada robot
                    for selected_robot in robots:
                        # Filtrar las interacciones realizadas por el robot seleccionado
                        interactions = data[(data['label'] == 'performedBy') & (data['node2'] == selected_robot) | 
                                    (data['label'] == 'objectOfAction') & (data['node2'] == selected_robot)]
        
                        # Iterar sobre cada interacción
                        for _, interaction_row in interactions.iterrows():
                            interaction = interaction_row['node1']
            
                            # Obtener la fecha de la interacción
                            date_interaction = data[(data['node1'] == interaction) & (data['label'] == 'date')]['node2'].values
                            date_interaction = date_interaction[0] if date_interaction else None
            
                            # Obtener el estado emocional causado por la interacción
                            emotional_state_rows = data[(data['label'] == 'causedBy') & (data['node2'] == interaction)]
                            if not emotional_state_rows.empty:
                                emotional_state_node = emotional_state_rows['node1'].values[0]
                                emotional_state = data[(data['node1'] == emotional_state_node) & (data['label'] == 'hasEmotionalState')]['node2'].values
                                emotional_state = emotional_state[0] if emotional_state else None

                                # Obtener la fecha del estado emocional
                                date_emotional_state = data[(data['node1'] == emotional_state_node) & (data['label'] == 'date')]['node2'].values
                                date_emotional_state = date_emotional_state[0] if date_emotional_state else None
                            else:
                                emotional_state = None
                                date_emotional_state = None

                            # Añadir los resultados a las listas
                            robots_list.append(selected_robot)
                            interaction_list.append(interaction)
                            date_interaction_list.append(date_interaction)
                            emotional_state_list.append(emotional_state)
                            date_emotional_state_list.append(date_emotional_state)

                    # Crear el DataFrame resultante
                    result_data = pd.DataFrame({
                        'Robot': robots_list,
                        'Interaction': interaction_list,
                        'DateInteraction': date_interaction_list,
                        'EmotionalState': emotional_state_list,
                        'DateEmotionalState': date_emotional_state_list
                     })

                    return result_data

            st.markdown('<div style="color:#00629b; font-size: 35px;">Emotions resume for all robots</div>', unsafe_allow_html=True)
            st.markdown('<div style="color:#00a9e0; font-size: 20px; text-align: left;"> </div>', unsafe_allow_html=True)

            result_data = get_interactions_for_all_robots(data)

            # Filtrar los datos para EmotionalState no nulos
            emotional_data = result_data[result_data['EmotionalState'].notnull()]

            if not emotional_data.empty:
                # Formatear las fechas
                emotional_data['DateEmotionalState'] = emotional_data['DateEmotionalState'].str.lstrip('^')
                emotional_data['DateEmotionalState'] = pd.to_datetime(emotional_data['DateEmotionalState'], format='%Y-%m-%dT%H:%M:%SZ')

                # Asignar colores específicos a cada emoción
                unique_emotions = emotional_data['EmotionalState'].unique()
                emotion_colors = px.colors.qualitative.Plotly[:len(unique_emotions)]
                emotion_color_map = dict(zip(unique_emotions, emotion_colors))

                # Asignar colores específicos a cada robot
                unique_robots = emotional_data['Robot'].unique()
                robot_colors = px.colors.qualitative.Plotly[:len(unique_robots)]
                robot_color_map = dict(zip(unique_robots, robot_colors))

                # Generar la gráfica de estados emocionales a lo largo del tiempo
                fig_time = px.line(emotional_data, x='DateEmotionalState', y='EmotionalState', 
                                title='Emotional States Over Time', 
                                labels={'DateEmotionalState': 'Date', 'EmotionalState': 'Emotional State'},
                                color='Robot', 
                                markers=True,
                                template='plotly_dark',
                                color_discrete_map=robot_color_map)

                fig_time.update_traces(marker=dict(size=10), selector=dict(mode='markers'))
                fig_time.update_layout(xaxis_title='Date', yaxis_title='Emotional State', showlegend=False)

                # Generar la gráfica de recuento de sentimientos
                emotional_count = emotional_data['EmotionalState'].value_counts().reset_index()
                emotional_count.columns = ['EmotionalState', 'Count']

                fig_count = px.bar(emotional_count, x='EmotionalState', y='Count', 
                                title='Count of Emotional States', 
                                labels={'EmotionalState': 'Emotional State', 'Count': 'Count'},
                                color='EmotionalState',
                                color_discrete_map=emotion_color_map,
                                template='plotly_dark')

                fig_count.update_layout(xaxis_title='Emotional State', yaxis_title='Count', showlegend=False)

                # Crear la leyenda de emociones
                emotion_legend_items = []
                for emotion, color in emotion_color_map.items():
                    emotion_legend_items.append(f"<div style='display: flex; align-items: center; margin-right: 20px;'>"
                                                f"<div style='width: 20px; height: 20px; background-color: {color}; margin-right: 10px;'></div>"
                                                f"<div style='font-size: 16px;'>{emotion}</div></div>")
                emotion_legend_html = "<div style='display: flex; flex-wrap: wrap; justify-content: center; margin-bottom: 20px;'>" + "".join(emotion_legend_items) + "</div>"

                # Crear la leyenda de robots
                robot_legend_items = []
                for robot, color in robot_color_map.items():
                    robot_legend_items.append(f"<div style='display: flex; align-items: center; margin-right: 20px;'>"
                                            f"<div style='width: 20px; height: 20px; background-color: {color}; margin-right: 10px;'></div>"
                                            f"<div style='font-size: 16px;'>{robot}</div></div>")
                robot_legend_html = "<div style='display: flex; flex-wrap: wrap; justify-content: center; margin-bottom: 20px;'>" + "".join(robot_legend_items) + "</div>"

                # Mostrar ambas gráficas una al lado de la otra con sus leyendas respectivas
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(robot_legend_html, unsafe_allow_html=True)
                    st.plotly_chart(fig_time)

                with col2:
                    st.markdown(emotion_legend_html, unsafe_allow_html=True)
                    st.plotly_chart(fig_count)
   
                
                
                # Filtrar por node1 cuando node2 = 'Robot'
                robots = data[data['node2'] == 'Robot']
                robot_names = robots['node1'].unique()

                
                st.markdown('<div style="color:#00629b; font-size: 35px;">Statistics for each robot</div>', unsafe_allow_html=True)
                st.markdown('<div style="color:#00a9e0; font-size: 20px; text-align: left;">Select a robot</div>', unsafe_allow_html=True)
                selected_robot = st.selectbox("", robot_names)
                st.markdown('<div style="color:#00a9e0; font-size: 20px; text-align: left;"> </div>', unsafe_allow_html=True)
                
                interactions = data[data['node2'] == 'Action']

                st.markdown(f'<div style="color:#00629b; font-size: 35px;">Interactions carried out by {selected_robot}:</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 1])

                total_Robot_Interactions = 0

                with col1:
                    for _, interaction in interactions.iterrows():
                        interaction_id = interaction['node1']
                        interactionByRobot = data[(data['label'] == "performedBy") & (data['node2'] == selected_robot) & (data['node1'] == interaction_id)]

                        if not interactionByRobot.empty:
                            total_Robot_Interactions += 1

                    st.markdown(f'<div style="color:#00a9e0; font-size: 20px;">Overview</div>', unsafe_allow_html=True)
                    st.metric(label="Total Interactions", value=total_Robot_Interactions, delta=f"{total_Robot_Interactions} 🟢")

                    st.markdown('<div style="color:#00a9e0; font-size: 20px; text-align: left;">Interactions Status</div>', unsafe_allow_html=True)
                    st.success(f"The robot {selected_robot} has carried out a total of {total_Robot_Interactions} interactions.")
                
                st.markdown('<div style="color:#00629b; font-size: 35px;"> </div>', unsafe_allow_html=True)
                
                def get_interactions_for_robot(selected_robot):
                    # Filtrar las interacciones realizadas por el robot seleccionado
                    interactions = data[(data['label'] == 'performedBy') & (data['node2'] == selected_robot) | (data['label'] == 'objectOfAction') & (data['node2'] == selected_robot)]
                    
                    # Inicializar listas para almacenar los resultados
                    interaction_list = []
                    date_interaction_list = []
                    emotional_state_list = []
                    date_emotional_state_list = []

                    # Iterar sobre cada interacción
                    for _, interaction_row in interactions.iterrows():
                        interaction = interaction_row['node1']
        
                        # Obtener la fecha de la interacción
                        date_interaction = data[(data['node1'] == interaction) & (data['label'] == 'date')]['node2'].values
                        date_interaction = date_interaction[0] if date_interaction else None
        
                        # Obtener el estado emocional causado por la interacción
                        emotional_state_rows = data[(data['label'] == 'causedBy') & (data['node2'] == interaction)]
                        if not emotional_state_rows.empty:
                            emotional_state_node = emotional_state_rows['node1'].values[0]
                            emotional_state = data[(data['node1'] == emotional_state_node) & (data['label'] == 'hasEmotionalState')]['node2'].values
                            emotional_state = emotional_state[0] if emotional_state else None

                            # Obtener la fecha del estado emocional
                            date_emotional_state = data[(data['node1'] == emotional_state_node) & (data['label'] == 'date')]['node2'].values
                            date_emotional_state = date_emotional_state[0] if date_emotional_state else None
                        else:
                            emotional_state = None
                            date_emotional_state = None

                        # Añadir los resultados a las listas
                        interaction_list.append(interaction)
                        date_interaction_list.append(date_interaction)
                        emotional_state_list.append(emotional_state)
                        date_emotional_state_list.append(date_emotional_state)

                    # Crear el DataFrame resultante
                    result_data = pd.DataFrame({
                    'Robot': selected_robot,
                    'Interaction': interaction_list,
                    'DateInteraction': date_interaction_list,
                    'EmotionalState': emotional_state_list,
                    'DateEmotionalState': date_emotional_state_list
    })

                    return result_data
                
                st.markdown('<div style="color:#00629b; font-size: 35px;"></div>', unsafe_allow_html=True)
                st.markdown('<div style="color:#00629b; font-size: 35px;">Emotions for each robot</div>', unsafe_allow_html=True)
                st.markdown('<div style="color:#00629b; font-size: 35px;"></div>', unsafe_allow_html=True)
                                    
                if selected_robot:
                    result_data = get_interactions_for_robot(selected_robot)
                    
                    # Filtrar los datos para EmotionalState no nulos
                    emotional_data = result_data[result_data['EmotionalState'].notnull()]

                    if not emotional_data.empty:
                        # Formatear las fechas
                        emotional_data['DateEmotionalState'] = emotional_data['DateEmotionalState'].str.lstrip('^')
                        emotional_data['DateEmotionalState'] = pd.to_datetime(emotional_data['DateEmotionalState'], format='%Y-%m-%dT%H:%M:%SZ')

                        # Asignar colores específicos a cada emoción
                        unique_emotions = emotional_data['EmotionalState'].unique()
                        colors = px.colors.qualitative.Plotly[:len(unique_emotions)]
                        color_map = dict(zip(unique_emotions, colors))

                        # Generar la gráfica de estados emocionales a lo largo del tiempo
                        fig_time = px.scatter(emotional_data, x='DateEmotionalState', y='EmotionalState', 
                              title='Emotional States Over Time', 
                              labels={'DateEmotionalState': 'Date', 'EmotionalState': 'Emotional State'},
                              color='EmotionalState',
                              color_discrete_map=color_map,
                              template='plotly_dark')

                        fig_time.update_traces(marker=dict(size=10), selector=dict(mode='markers'))
                        fig_time.update_layout(xaxis_title='Date', yaxis_title='Emotional State', showlegend=False)

                        # Generar la gráfica de recuento de sentimientos
                        emotional_count = emotional_data['EmotionalState'].value_counts().reset_index()
                        emotional_count.columns = ['EmotionalState', 'Count']

                        fig_count = px.bar(emotional_count, x='EmotionalState', y='Count', 
                           title='Count of Emotional States', 
                           labels={'EmotionalState': 'Emotional State', 'Count': 'Count'},
                           color='EmotionalState',
                           color_discrete_map=color_map,
                           template='plotly_dark')

                        fig_count.update_layout(xaxis_title='Emotional State', yaxis_title='Count', showlegend=False)

                        # Crear la leyenda utilizando Streamlit
                        legend_items = []
                        for emotion, color in color_map.items():
                            legend_items.append(f"<div style='display: flex; align-items: center; margin-right: 20px;'>"
                                                f"<div style='width: 20px; height: 20px; background-color: {color}; margin-right: 10px;'></div>"
                                                f"<div style='font-size: 16px;'>{emotion}</div></div>")
                        legend_html = "<div style='display: flex; flex-wrap: wrap; justify-content: center; margin-bottom: 20px;'>" + "".join(legend_items) + "</div>"

                        st.markdown(legend_html, unsafe_allow_html=True)

                        # Mostrar ambas gráficas una al lado de la otra
                        col1, col2 = st.columns(2)
                        col1.plotly_chart(fig_time)
                        col2.plotly_chart(fig_count)
                
                
                    
            else:
                st.warning("Please upload a CSV file in the 'Upload CSV' tab")
    else:
        st.warning("Please upload a CSV file in the 'Upload CSV' tab")

with tab3:
    st.markdown('<div style="color:#00629b; font-size: 35px;">Human Statistics</div>', unsafe_allow_html=True)
    if data is not None:
        if 'node1' in data.columns and 'node2' in data.columns:
            # Contar humanos
            humans = data[data['node2'] == 'Human']['node1'].unique()
            num_humans = len(humans)
            
            st.markdown(f'<div style="color:#00a9e0; font-size: 20px;">Number of Humans: {num_humans}</div>', unsafe_allow_html=True)
            st.markdown(f"<div class='icon'> {'🧍' * num_humans}</div>", unsafe_allow_html=True)

        # Lógica adicional para obtener el valor de label para cada humano
        st.markdown('<div style="color:#00629b; font-size: 35px;">Information about each Human</div>', unsafe_allow_html=True)
        st.markdown('<div style="color:#00629b; font-size: 35px;"> </div>', unsafe_allow_html=True)
        
        if 'node1' in data.columns and 'node2' in data.columns and 'label' in data.columns:
            # Filtrar los nombres de los humanos
            human_names = data[data['node2'] == 'Human']['node1'].unique()

            results = []
            for human in human_names:
                label_value = data[(data['node1'] == human) & (data['label'] == 'type')]['node2'].values
                label_value1 = data[(data['node1'] == human) & (data['label'] == 'label')]['node2'].values
                if len(label_value) > 0:
                    results.append((human, label_value[0], label_value1[0]))

            if results:
                results_data = pd.DataFrame(results, columns=['Human', 'Label Value', 'name'])
                st.dataframe(results_data)
            else:
                st.warning("No se encontraron valores para los humanos especificados.")
                
            if 'label' in data.columns and 'node1' in data.columns and 'node2' in data.columns:
                # Filtrar por node1 cuando node2 = 'Human'
                humans = data[data['node2'] == 'Human']
                human_names = humans['node1'].unique()

                st.markdown('<div style="color:#00a9e0; font-size: 20px; text-align: left;">Select a human</div>', unsafe_allow_html=True)
                selected_human = st.selectbox("", human_names)
                st.markdown('<div style="color:#00a9e0; font-size: 20px; text-align: left;"> </div>', unsafe_allow_html=True)

                interactions = data[data['node2'] == 'Action']

                st.markdown(f'<div style="color:#00a9e0; font-size: 20px;">Interactions carried out by {selected_human}:</div>', unsafe_allow_html=True)

                col1, col2 = st.columns([1, 1])

                total_Human_Interactions = 0

                with col1:
                    for _, interaction in interactions.iterrows():
                        interaction_id = interaction['node1']
                        interactionByHuman = data[(data['label'] == "performedBy") & (data['node2'] == selected_human) & (data['node1'] == interaction_id)]

                        if not interactionByHuman.empty:
                            total_Human_Interactions += 1
                            st.write(f"Interaction: {interaction_id}")
                            st.write(interactionByHuman)

                with col2:
                    st.markdown('<div style="color:#00629b; font-size: 35px;">Overview</div>', unsafe_allow_html=True)
                    st.metric(label="Total Interactions", value=total_Human_Interactions, delta=f"{total_Human_Interactions} 🟢")

                    st.markdown('<div style="color:#00629b; font-size: 35px;">Interactions Status</div>', unsafe_allow_html=True)
                    st.success(f"The human {selected_human} has carried out a total of {total_Human_Interactions} interactions.")

                    st.markdown('<div style="color:#00629b; font-size: 35px;">Progress</div>', unsafe_allow_html=True)
                    st.progress(total_Human_Interactions / len(interactions) if len(interactions) > 0 else 0)

                st.markdown('<div style="color:#00629b; font-size: 35px;"> </div>', unsafe_allow_html=True)    
                st.markdown('<div style="color:#00629b; font-size: 35px;">Display data on status changes</div>', unsafe_allow_html=True)

                # Agregar un contenedor expandible
                with st.expander(f"Emotional state changes by {selected_human}"):
                    interaction_names = []
                    emotional_states_data = []

                    for _, interaction in interactions.iterrows():
                        interaction_id = interaction['node1']
                        emotionalStates = data[(data['label'] == 'hasEmotionalState') & (data['node1'] == selected_human)]

                        if not emotionalStates.empty:
                            for _, state in emotionalStates.iterrows():
                                state_value = state['node2']
                                emotional_states_data.append((selected_human, state_value))
                                interaction_names.append(interaction_id)

                    if emotional_states_data:
                        emotional_states_data = pd.DataFrame(emotional_states_data, columns=['Human', 'Emotional State'])
                        st.dataframe(emotional_states_data)
                    else:
                        st.warning(f"No emotional state data found for {selected_human}")

                    st.markdown('<div style="color:#00629b; font-size: 35px;">Graph of Emotional States</div>', unsafe_allow_html=True)

                    if emotional_states_data:
                        fig = go.Figure()

                        emotional_states_count = emotional_states_data['Emotional State'].value_counts()
                        fig.add_trace(go.Bar(
                            x=emotional_states_count.index,
                            y=emotional_states_count.values,
                            marker_color='blue'
                        ))

                        fig.update_layout(
                            title=f"Emotional State Distribution for {selected_human}",
                            xaxis_title="Emotional State",
                            yaxis_title="Count",
                            title_x=0.5
                        )

                        st.plotly_chart(fig)
                    else:
                        st.warning(f"No emotional state data found for {selected_human}")
            else:
                st.warning("Please upload a CSV file in the 'Upload CSV' tab")
    else:
        st.warning("Please upload a CSV file in the 'Upload CSV' tab")
        
        # Pie de página
st.markdown(
    """
    <hr style="border: 1px solid #00629b;">
    """,
    unsafe_allow_html=True
)

# Crear una columna vacía a la izquierda y a la derecha para centrar el contenido
col1, col2, col3 = st.columns([0.1, 3, 0.1])

with col2:
    # Usar columnas internas para alinear la imagen y el texto
    col2a, col2b, col2c, col2d = st.columns([0.8, 2, 1.5, 1.5])
    with col2a:
        st.image('images/logo_gsi.png', width=75)
    with col2b:
        st.markdown(
            """
            <div style="font-size: 20px; margin-top: 20px;">
                App created by 
                <a href="https://gsi.upm.es" style="color: #00629b;">Intelligent Systems Group</a>.
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2c:
        st.image('images/logo_amor_azulupm.png', width=200)   
    with col2d:
        st.image('images/ministerio.png', width=200)     
         
    # Añadir un padding inferior para el pie de página
    st.markdown(
        """
        <div style="padding-bottom: 30px;"></div>
        """,
        unsafe_allow_html=True
    )

