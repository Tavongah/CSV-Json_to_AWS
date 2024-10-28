from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

# Connection details
neptune_endpoint = 'db-neptune-1.cluster-ro-c5w8mwik4vdi.us-east-2.neptune.amazonaws.com'  # Replace with your Neptune endpoint

try:
    # Establish a connection to the Neptune cluster
    connection = DriverRemoteConnection(f'wss://{neptune_endpoint}/gremlin', 'g')
    graph = Graph()
    g = graph.traversal().withRemote(connection)

    # Example query
    print("Vertices:")
    for vertex in g.V().toList():
        print(vertex)

except Exception as e:
    print("An error occurred while connecting to Neptune:", e)

finally:
    if 'connection' in locals():
        connection.close()

