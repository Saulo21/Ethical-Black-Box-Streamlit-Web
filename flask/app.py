from flask import Flask, request, jsonify
from neo4j import GraphDatabase
import pandas as pd
import io

app = Flask(__name__)

# Configura la conexión a Neo4j
uri = "bolt://localhost:7687"
user = "neo4j"
password = "saulo123"
driver = GraphDatabase.driver(uri, auth=(user, password))

def add_data_to_neo4j(df):
    with driver.session() as session:
        for index, row in df.iterrows():
            session.run(
                """
                MERGE (n1:Node {id: $node1})
                MERGE (n2:Node {id: $node2})
                MERGE (n1)-[:RELATION {label: $label}]->(n2)
                """,
                node1=row['node1'],
                node2=row['node2'],
                label=row['label']
            )

@app.route('/')
def index():
    return "Bienvenido a la API de carga de CSV. Usa la ruta /upload_csv para subir tus archivos."

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    file = request.files['file']
    data = file.read().decode('utf-8')
    df = pd.read_csv(io.StringIO(data))

    print(df.head())  # Agregar esto para ver las primeras filas del DataFrame y las columnas disponibles

    add_data_to_neo4j(df)
    return jsonify({"message": "Data added successfully"}), 200

@app.route('/graphs', methods=['GET'])
def get_graphs():
    with driver.session() as session:
        result = session.run("MATCH (n:Node) RETURN DISTINCT n.id AS id")
        graphs = [record["id"] for record in result]
    return jsonify(graphs), 200

if __name__ == '__main__':
    app.run(debug=True)