import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import requests

# Configuración de la página
st.set_page_config(
    page_title="Análisis de la Ethical Black Box",
    page_icon="📊",
    layout="wide"
)

# Logo y título
c1, c2 = st.columns([0.2, 0.7])

with c1:
    st.image('images/logo.png', width=110)
    
with c2:
    st.caption("")
    new_title = '<p style="color:#00629b; font-size: 80px;">Ethical Black Box</p> <hr style="border: 1px solid #00629b;">'
    st.markdown(new_title, unsafe_allow_html=True)

# Cargar CSS
css_file = open("config/estiloMain.css", "r").read()
st.markdown(f'<style>{css_file}</style>', unsafe_allow_html=True)

# Función para cargar el archivo CSV
def cargar_csv():
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.success("File successfully uploaded")
        st.dataframe(data)
        
        # Enviar el archivo CSV al servidor Flask
        response = requests.post(
            'http://127.0.0.1:5000/upload_csv',
            files={'file': uploaded_file.getvalue()}
        )
        
        if response.status_code == 200:
            st.success("Data successfully sent to Neo4j")
        else:
            st.error(f"Failed to send data to Neo4j: {response.json().get('error', 'Unknown error')}")
        
        return data
    return None

# Función para obtener la lista de grafos desde Flask
def obtener_grafos():
    response = requests.get('http://127.0.0.1:5000/graphs')
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to retrieve graphs: {response.json().get('error', 'Unknown error')}")
        return []

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

    # Obtener y mostrar la lista de grafos en un desplegable
    st.markdown('<div style="color:#00a9e0; font-size: 20px;">Select a Graph</div>', unsafe_allow_html=True)
    graphs = obtener_grafos()
    selected_graph = st.selectbox("", graphs)
    st.markdown(f"Selected Graph: {selected_graph}")

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
                results_df = pd.DataFrame(results, columns=['Robot', 'Label Value', 'name'])
                st.dataframe(results_df)
            else:
                st.warning("No se encontraron valores para los robots especificados.")

            if 'label' in data.columns and 'node1' in data.columns and 'node2' in data.columns:
                # Filtrar por node1 cuando node2 = 'Robot'
                robots = data[data['node2'] == 'Robot']
                robot_names = robots['node1'].unique()

                st.markdown('<div style="color:#00a9e0; font-size: 20px; text-align: left;">Select a robot</div>', unsafe_allow_html=True)
                selected_robot = st.selectbox("", robot_names)
                st.markdown('<div style="color:#00a9e0; font-size: 20px; text-align: left;"> </div>', unsafe_allow_html=True)
                
                interactions = data[data['node2'] == 'Action']

                st.markdown(f'<div style="color:#00a9e0; font-size: 20px;">Interactions carried out by {selected_robot}:</div>', unsafe_allow_html=True)

                col1, col2 = st.columns([1, 1])

                total_Robot_Interactions = 0

                with col1:
                    for _, interaction in interactions.iterrows():
                        interaction_id = interaction['node1']
                        interactionByRobot = data[(data['label'] == "performedBy") & (data['node2'] == selected_robot) & (data['node1'] == interaction_id)]

                        if not interactionByRobot.empty:
                            total_Robot_Interactions += 1
                            st.write(f"Interaction: {interaction_id}")
                            st.write(interactionByRobot)

                with col2:
                    st.markdown('<div style="color:#00629b; font-size: 35px;">Overview</div>', unsafe_allow_html=True)
                    st.metric(label="Total Interactions", value=total_Robot_Interactions, delta=f"{total_Robot_Interactions} 🟢")

                    st.markdown('<div style="color:#00629b; font-size: 35px;">Interactions Status</div>', unsafe_allow_html=True)
                    st.success(f"The robot {selected_robot} has carried out a total of {total_Robot_Interactions} interactions.")

                    st.markdown('<div style="color:#00629b; font-size: 35px;">Progress</div>', unsafe_allow_html=True)
                    st.progress(total_Robot_Interactions / len(interactions) if len(interactions) > 0 else 0)
                    
                
                st.markdown('<div style="color:#00629b; font-size: 35px;"> </div>', unsafe_allow_html=True)    
                st.markdown('<div style="color:#00629b; font-size: 35px;">Display data on status changes</div>', unsafe_allow_html=True)
                
                # Agregar un contenedor expandible
                with st.expander(f"Emotional state changes by {selected_robot}"):
                    interaction_names = []
                    emotional_states_data = []

                    for _, interaction in interactions.iterrows():
                        interaction_id = interaction['node1']
                        emotionalStates = data[data['node2'] == interaction_id]

                        if not emotionalStates.empty:
                            emotionalStates_node1_values = emotionalStates['node1'].unique()
                            emotionalStatesInteractions = data[data['node1'].isin(emotionalStates_node1_values)]

                            if not emotionalStatesInteractions.empty:
                                st.write(f"Interaction: {interaction_id}")
                                st.write(emotionalStatesInteractions)
                                interaction_names.append(interaction_id)
                                emotional_states_data.append(emotionalStatesInteractions)

                # Modificar los datos de la gráfica para incluir información detallada
                timeline_data = pd.DataFrame({
                    'Interaction': interaction_names,
                    'Index': range(len(interaction_names)),
                    'Details': ['<br>'.join(map(str, df.values.tolist())) for df in emotional_states_data]
                })

                # Crear la gráfica con plotly
                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=timeline_data['Index'],
                    y=[1] * len(timeline_data),
                    mode='markers+text',
                    marker=dict(size=12, color='#636EFA'),
                    text=timeline_data['Interaction'],
                    hovertext=timeline_data['Details'],
                    textposition="top center"
                ))

                # Configurar el diseño de la gráfica
                st.markdown('<div style="color:#00a9e0; font-size: 20px; text-align: left;"> </div>', unsafe_allow_html=True)
                st.markdown('<div style="color:#00a9e0; font-size: 20px; text-align: left;">Timeline of Interactions</div>', unsafe_allow_html=True)
                
                fig.update_layout(
                    showlegend=False,
                    xaxis=dict(
                        showline=False, showgrid=False, showticklabels=False
                    ),
                    yaxis=dict(
                        showline=False, showgrid=False, showticklabels=False
                    ),
                    plot_bgcolor='#FFFFFF'
                )

                # Mostrar la gráfica en Streamlit
                st.plotly_chart(fig, use_container_width=True)

        else:
            st.error("El archivo CSV no contiene las columnas necesarias ('node1', 'node2', 'label').")
    else:
        st.warning("Please upload a CSV file in the 'Upload CSV' tab")

with tab3:
    st.markdown('<div style="color:#00629b; font-size: 35px;">Human Statistics</div>', unsafe_allow_html=True)
    if data is not None:
        if 'node1' in data.columns and 'node2' in data.columns:
            # Contar robots y humanos
            humans = data[data['node2'] == 'Human']['node1'].unique()

            num_humans = len(humans)

            st.markdown(f'<div style="color:#00a9e0; font-size: 20px;">Number of Humans: {num_humans}</div>', unsafe_allow_html=True)
            st.markdown(f"<div class='icon'> {'👨 ' * num_humans}</div>", unsafe_allow_html=True)
            st.markdown(f'<div style="color:#00a9e0; font-size: 20px;"> </div>', unsafe_allow_html=True)
        
        # Lógica adicional para obtener el valor de label para cada robot y humano
        st.markdown('<div style="color:#00629b; font-size: 35px;">Information about each Human</div>', unsafe_allow_html=True)
        if 'node1' in data.columns and 'node2' in data.columns and 'label' in data.columns:
            # Filtrar los nombres de los robots
            human_names = data[data['node2'] == 'Human']['node1'].unique()

            humans_results = []
            for human in human_names:
                label_value = data[(data['node1'] == human) & (data['label'] == 'type')]['node2'].values
                label_value1 = data[(data['node1'] == human) & (data['label'] == 'label')]['node2'].values
                if len(label_value) > 0:
                    humans_results.append((human, label_value[0], label_value1[0]))

            if humans_results:
                human_results_df = pd.DataFrame(humans_results, columns=['Human', 'Label Value', 'name'])
                st.dataframe(human_results_df)
            else:
                st.warning("No se encontraron valores para los robots especificados.")
                    
    if data is not None:
        # Filtrar por node1 cuando node2 = 'Human'
        humans = data[data['node2'] == 'Human']
        humans_names = humans['node1'].unique()

        st.markdown('<div style="color:#00a9e0; font-size: 20px; text-align: left;">Select a human</div>', unsafe_allow_html=True)
        selected_human = st.selectbox("", humans_names)
        st.markdown('<div style="color:#00a9e0; font-size: 20px; text-align: left;"> </div>', unsafe_allow_html=True)

        interactionsHuman = data[data['node2'] == 'Action']

        st.markdown(f'<div style="color:#00a9e0; font-size: 20px;">Interactions carried out by {selected_human}:</div>', unsafe_allow_html=True)


        col1, col2 = st.columns([1, 1])

        total_Human_Interactions = 0

        with col1:
            for _, interaction in interactionsHuman.iterrows():
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
            st.progress(total_Human_Interactions / len(interactionsHuman) if len(interactionsHuman) > 0 else 0)

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
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Usar columnas internas para alinear la imagen y el texto
    col2a, col2b = st.columns([1, 4])
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
    # Añadir un padding inferior para el pie de página
    st.markdown(
        """
        <div style="padding-bottom: 30px;"></div>
        """,
        unsafe_allow_html=True
    )
