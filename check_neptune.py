from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

# Connect to your Neptune endpoint
neptune_endpoint = 'wss://db-neptune-1.cluster-c5w8mwik4vdi.us-east-2.neptune.amazonaws.com:8182/gremlin'
graph = Graph()

try:
    # Create a connection to the Neptune database
    connection = DriverRemoteConnection(neptune_endpoint, 'g')
    g = graph.traversal().withRemote(connection)

    # Query to fetch all vertices
    vertices = g.V().elementMap().toList()
    print("Vertices:")
    for vertex in vertices:
        print(vertex)

    # Query to fetch all edges
    edges = g.E().elementMap().toList()
    print("\nEdges:")
    for edge in edges:
        print(edge)

except Exception as e:
    print(f"Error connecting to Neptune: {e}")

finally:
    if 'connection' in locals():
        try:
            connection.close()
            print("Connection closed successfully.")
        except Exception as close_exception:
            print(f"Error closing connection: {close_exception}")

