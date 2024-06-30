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
                    
                
                st.markdown('<div style="color:#00629b; font-size: 40px;">Kibana Visualizations</div> <hr style="border: 1px solid #00629b; width: 50%; margin-left: 0;">', unsafe_allow_html=True)
                if data is not None:
                    kibana_iframe = '''
                    <iframe src="http://localhost:5601/s/robots/app/dashboards#/view/a0192750-33cd-11ef-9e4a-13c30e4a9272?embed=true&_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now-15m,to:now))&_a=(description:'',filters:!(),fullScreenMode:!f,options:(hidePanelTitles:!f,syncColors:!f,useMargins:!t),panels:!((embeddableConfig:(attributes:(references:!((id:d0cbf270-33c7-11ef-9e4a-13c30e4a9272,name:indexpattern-datasource-current-indexpattern,type:index-pattern),(id:d0cbf270-33c7-11ef-9e4a-13c30e4a9272,name:indexpattern-datasource-layer-461b6069-35d7-4f41-96ac-21eba4051258,type:index-pattern)),state:(datasourceStates:(indexpattern:(layers:('461b6069-35d7-4f41-96ac-21eba4051258':(columnOrder:!('96afb255-1f51-425e-8572-b6a4476be7a7','55e10013-e68b-40ef-8501-95b553db61e4'),columns:('55e10013-e68b-40ef-8501-95b553db61e4':(dataType:number,isBucketed:!f,label:'Count%20of%20records',operationType:count,params:(),scale:ratio,sourceField:Records),'96afb255-1f51-425e-8572-b6a4476be7a7':(dataType:string,isBucketed:!t,label:'Top%20values%20of%20hasEmotionalState.keyword',operationType:terms,params:(missingBucket:!f,orderBy:(columnId:'55e10013-e68b-40ef-8501-95b553db61e4',type:column),orderDirection:desc,otherBucket:!t,size:5),scale:ordinal,sourceField:hasEmotionalState.keyword)),incompleteColumns:())))),filters:!(),query:(language:kuery,query:''),visualization:(layers:!((categoryDisplay:default,groups:!('96afb255-1f51-425e-8572-b6a4476be7a7'),layerId:'461b6069-35d7-4f41-96ac-21eba4051258',layerType:data,legendDisplay:default,metric:'55e10013-e68b-40ef-8501-95b553db61e4',nestedLegend:!f,numberDisplay:percent)),shape:donut)),title:'',type:lens,visualizationType:lnsPie),enhancements:()),gridData:(h:15,i:d427bb20-31a5-4f86-9fba-96e1412b2d5e,w:24,x:0,y:0),panelIndex:d427bb20-31a5-4f86-9fba-96e1412b2d5e,type:lens,version:'7.17.22'),(embeddableConfig:(attributes:(references:!((id:d0cbf270-33c7-11ef-9e4a-13c30e4a9272,name:indexpattern-datasource-current-indexpattern,type:index-pattern),(id:d0cbf270-33c7-11ef-9e4a-13c30e4a9272,name:indexpattern-datasource-layer-1e70b3ed-8382-4013-8bf1-f40e56f5bfd1,type:index-pattern)),state:(datasourceStates:(indexpattern:(layers:('1e70b3ed-8382-4013-8bf1-f40e56f5bfd1':(columnOrder:!(dc29c226-bf1a-4698-aed5-01ed00a07cae,'0e333881-980d-488e-92b8-ea63d6e1b8b8'),columns:('0e333881-980d-488e-92b8-ea63d6e1b8b8':(dataType:number,isBucketed:!f,label:'Count%20of%20records',operationType:count,scale:ratio,sourceField:Records),dc29c226-bf1a-4698-aed5-01ed00a07cae:(dataType:string,isBucketed:!t,label:'Top%20values%20of%20hasEmotionalState.keyword',operationType:terms,params:(missingBucket:!f,orderBy:(columnId:'0e333881-980d-488e-92b8-ea63d6e1b8b8',type:column),orderDirection:desc,otherBucket:!t,size:5),scale:ordinal,sourceField:hasEmotionalState.keyword)),incompleteColumns:())))),filters:!(),query:(language:kuery,query:''),visualization:(axisTitlesVisibilitySettings:(x:!t,yLeft:!t,yRight:!t),fittingFunction:None,gridlinesVisibilitySettings:(x:!t,yLeft:!t,yRight:!t),labelsOrientation:(x:0,yLeft:0,yRight:0),layers:!((accessors:!('0e333881-980d-488e-92b8-ea63d6e1b8b8'),layerId:'1e70b3ed-8382-4013-8bf1-f40e56f5bfd1',layerType:data,position:top,seriesType:bar_stacked,showGridlines:!f,xAccessor:dc29c226-bf1a-4698-aed5-01ed00a07cae)),legend:(isVisible:!t,position:right),preferredSeriesType:bar_stacked,tickLabelsVisibilitySettings:(x:!t,yLeft:!t,yRight:!t),valueLabels:hide,yLeftExtent:(mode:full),yRightExtent:(mode:full))),title:'',type:lens,visualizationType:lnsXY),enhancements:()),gridData:(h:15,i:d4e466d5-02ee-4b2a-9631-9250ced8219b,w:24,x:24,y:0),panelIndex:d4e466d5-02ee-4b2a-9631-9250ced8219b,type:lens,version:'7.17.22'),(embeddableConfig:(attributes:(references:!((id:d0cbf270-33c7-11ef-9e4a-13c30e4a9272,name:indexpattern-datasource-current-indexpattern,type:index-pattern),(id:d0cbf270-33c7-11ef-9e4a-13c30e4a9272,name:indexpattern-datasource-layer-a777d4e3-e3d0-47ed-9036-2bf30d4445ef,type:index-pattern)),state:(datasourceStates:(indexpattern:(layers:(a777d4e3-e3d0-47ed-9036-2bf30d4445ef:(columnOrder:!('733afeaa-3169-4d7a-869b-7c79f887c9ca','5ed5d4fd-262a-495e-80ea-54b49707f3c5',ee5d79e0-02cb-4e70-a6aa-a92e4e8c8620),columns:('5ed5d4fd-262a-495e-80ea-54b49707f3c5':(customLabel:!t,dataType:number,filter:(language:kuery,query:'type.keyword%20:%20%22Human%22%20'),isBucketed:!f,label:Human,operationType:unique_count,scale:ratio,sourceField:type.keyword),'733afeaa-3169-4d7a-869b-7c79f887c9ca':(dataType:string,isBucketed:!t,label:Filters,operationType:filters,params:(filters:!((input:(language:kuery,query:''),label:''))),scale:ordinal),ee5d79e0-02cb-4e70-a6aa-a92e4e8c8620:(customLabel:!t,dataType:number,filter:(language:kuery,query:'type.keyword%20:%20%22Robot%22%20'),isBucketed:!f,label:Robot,operationType:unique_count,scale:ratio,sourceField:type.keyword)),incompleteColumns:())))),filters:!(),query:(language:kuery,query:''),visualization:(axisTitlesVisibilitySettings:(x:!t,yLeft:!t,yRight:!t),fittingFunction:None,gridlinesVisibilitySettings:(x:!t,yLeft:!t,yRight:!t),labelsOrientation:(x:0,yLeft:0,yRight:0),layers:!((accessors:!('5ed5d4fd-262a-495e-80ea-54b49707f3c5',ee5d79e0-02cb-4e70-a6aa-a92e4e8c8620),layerId:a777d4e3-e3d0-47ed-9036-2bf30d4445ef,layerType:data,position:top,seriesType:bar,showGridlines:!f,xAccessor:'733afeaa-3169-4d7a-869b-7c79f887c9ca')),legend:(isVisible:!t,position:right,showSingleSeries:!t),preferredSeriesType:bar,tickLabelsVisibilitySettings:(x:!t,yLeft:!t,yRight:!t),valueLabels:inside,xTitle:'Humans%20and%20robots',yLeftExtent:(mode:full),yRightExtent:(mode:full),yTitle:Amount)),title:'',type:lens,visualizationType:lnsXY),enhancements:()),gridData:(h:15,i:'59792b21-81f1-496d-bb27-470d6f865f47',w:24,x:0,y:15),panelIndex:'59792b21-81f1-496d-bb27-470d6f865f47',type:lens,version:'7.17.22')),query:(language:kuery,query:''),tags:!(),timeRestore:!f,title:KG,viewMode:view)" height="600" width="800"></iframe>
                    '''
                    components.html(kibana_iframe, height=500)
                else:
                    st.warning("Please upload a CSV file in the 'Upload CSV' tab")
                
                st.markdown('<div style="color:#00629b; font-size: 35px;"> </div>', unsafe_allow_html=True)    
                st.markdown('<div style="color:#00629b; font-size: 35px;">Display data on status changes</div>', unsafe_allow_html=True)
                
                st.markdown('<div style="color:#00629b; font-size: 35px;">Emotions1</div>', unsafe_allow_html=True)
                
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
                
                st.markdown('<div style="color:#00629b; font-size: 35px;">Emotions2</div>', unsafe_allow_html=True)
                    
                if selected_robot:
                    result_data = get_interactions_for_robot(selected_robot)
                    st.dataframe(result_data)
                    
                    # Filtrar los datos para EmotionalState no nulos
                    emotional_data = result_data[result_data['EmotionalState'].notnull()]

                    if not emotional_data.empty:
                        # Formatear las fechas
                        emotional_data['DateEmotionalState'] = emotional_data['DateEmotionalState'].str.lstrip('^')
                        emotional_data['DateEmotionalState'] = pd.to_datetime(emotional_data['DateEmotionalState'], format='%Y-%m-%dT%H:%M:%SZ')

                        # Generar la gráfica
                        fig = px.scatter(emotional_data, x='DateEmotionalState', y='EmotionalState', title='Emotional States Over Time', labels={'DateEmotionalState': 'Date', 'EmotionalState': 'Emotional State'})

                        fig.update_traces(marker=dict(size=10, color='blue'), selector=dict(mode='markers'))
                        fig.update_layout(xaxis_title='Date', yaxis_title='Emotional State', showlegend=False)
                        st.plotly_chart(fig)   
                    
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

