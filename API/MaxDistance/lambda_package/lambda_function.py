import json
from neo4j import GraphDatabase
import os

def lambda_handler(event, context):
    uri = os.environ['NEO4J_URI']
    user = os.environ['NEO4J_USER']
    password = os.environ['NEO4J_PASSWORD']

    start_word = event.get("start_word")
    end_word = event.get("end_word")
    mode = event.get("mode", "steps")
    max_depth = event.get("max_depth", 10)

    if not start_word or not end_word:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "start_word and end_word are required"})
        }

    if mode not in ["steps", "weight"]:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid mode. Choose 'steps' or 'weight'"})
        }

    driver = GraphDatabase.driver(uri, auth=(user, password))

    try:
        with driver.session() as session:
            if mode == "steps":
                result = session.read_transaction(find_longest_path_by_steps, start_word, end_word, max_depth)
            elif mode == "weight":
                result = session.read_transaction(find_longest_path_by_weight, start_word, end_word, max_depth)
        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
    finally:
        driver.close()

def find_longest_path_by_steps(tx, start_word, end_word, max_depth):
    query = f"""
    MATCH p = (start:Word)-[:RELATED*..{max_depth}]-(end:Word)
    WHERE start.id = $start_word AND end.id = $end_word
    RETURN p, length(p) AS pathLength
    ORDER BY pathLength DESC
    LIMIT 1
    """
    result = tx.run(query, start_word=start_word, end_word=end_word)
    longest_path = []
    for record in result:
        path = record["p"]
        path_length = record["pathLength"]
        longest_path.append({
            "nodes": [node["id"] for node in path.nodes],
            "edges": [edge["weight"] for edge in path.relationships],
            "length": path_length
        })
    return longest_path

def find_longest_path_by_weight(tx, start_word, end_word, max_depth):
    query = f"""
    MATCH p = (start:Word)-[:RELATED*..{max_depth}]-(end:Word)
    WHERE start.id = $start_word AND end.id = $end_word
    WITH p, reduce(totalWeight = 0, r IN relationships(p) | totalWeight + r.weight) AS totalWeight
    RETURN p, totalWeight
    ORDER BY totalWeight DESC
    LIMIT 1
    """
    result = tx.run(query, start_word=start_word, end_word=end_word)
    longest_path = []
    for record in result:
        path = record["p"]
        total_weight = record["totalWeight"]
        longest_path.append({
            "nodes": [node["id"] for node in path.nodes],
            "edges": [edge["weight"] for edge in path.relationships],
            "total_weight": total_weight
        })
    return longest_path
