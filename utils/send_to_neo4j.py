#!/usr/bin/env python
#
# send_to_neo4j.py - Get mail from gmail api
#
# Created by Bensuperpc at 05, March of 2020
#
# Released into the Private domain with MIT licence
# https://opensource.org/licenses/MIT
#
# Written with VisualStudio code 1.4.2 and python 3.7.8
# Script compatibility : Linux (Ubuntu ad debian based), Windows, mac
#
# ==============================================================================

from neo4j import GraphDatabase, basic_auth

def send(data, mdp = "12345678"):

    driver = GraphDatabase.driver(
        "bolt://localhost", auth=basic_auth("neo4j", mdp))
    session = driver.session()
    
    #insert_query = '''MATCH (n:Person) DETACH DELETE n'''
    
    #session.run(insert_query)

    insert_query = '''
    UNWIND {pairs} as pair
    MERGE (p1:Person {name:pair[0]})
    MERGE (p2:Person {name:pair[1]})
    MERGE (p1)-[:SEND]-(p2);
    '''
    
    insert_querys = '''
    UNWIND {pairs} as pair
    MERGE (p1:Person {name:pair[0]})
    MERGE (p2:Person {name:pair[1]})
    MERGE (p3:Subject {name:pair[2]})
    MERGE (p1)-[:Receive]-(p3)
    MERGE (p2)-[:Receive]-(p3);
    '''
    
    #CREATE (p1)-[:SEND]->(p2);

    #print(data)
    
    session.run(insert_querys, parameters={"pairs": data})

    # Friends of a friend
    
    foaf_query = '''
    MATCH (person:Person)-[:SEND]-(friend)-[:SEND]-(foaf) 
    WHERE person.name = {name}
    AND NOT (person)-[:SEND]-(foaf)
    RETURN foaf.name AS name
    '''

    results = session.run(foaf_query, parameters={"name": "Joe"})
    for record in results:
        print('Joe s Friends of a friend:', record["name"])

    # Common friends

    common_friends_query = """
    MATCH (user:Person)-[:SEND]-(friend)-[:SEND]-(foaf:Person)
    WHERE user.name = {user} AND foaf.name = {foaf}
    RETURN friend.name AS friend
    """

    results = session.run(common_friends_query, parameters={
        "user": "Joe", "foaf": "Sally"})
    for record in results:
        print('Joe Common friends of Sally:', record["friend"])

    # Connecting paths

    connecting_paths_query = """
    MATCH path = shortestPath((p1:Person)-[:SEND*..6]-(p2:Person))
    WHERE p1.name = {name1} AND p2.name = {name2}
    RETURN path
    """

    results = session.run(connecting_paths_query, parameters={
        "name1": "Joe", "name2": "Billy"})
    for record in results:
        print(record["path"])
    session.close()


if __name__ == '__main__':
    data = [['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['sylvain.fouchard', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['william.lefort', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['shigeru.miyamoto', 'lola.pointer'], ['sylvain.fouchard', 'lola.pointer'], ['sylvain.fouchard', 'lola.pointer'], ['lola.pointer', 'sylvain.fouchard'], ['william.lefort', 'lola.pointer'], ['nicolas.clerc', 'lola.pointer'], ['nicolas.clerc', 'lola.pointer'], ['william.lefort', 'lola.pointer'], ['sylvain.fouchard', 'lola.pointer'], ['sylvain.fouchard', 'lola.pointer'], ['sylvain.fouchard', 'nathalie.domengee'], ['sylvain.fouchard', 'nicolas.clerc'], ['sylvain.fouchard', 'lola.pointer'], ['lola.pointer', 'sylvain.fouchard'], ['lola.pointer', 'sylvain.fouchard'], ['sylvain.fouchard', 'lola.pointer'], ['sylvain.fouchard', 'lola.pointer'], ['lola.pointer', 'sylvain.fouchard'], ['lola.pointer', 'sylvain.fouchard'], ['william.lefort',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           'lola.pointer'], ['lola.pointer', 'sylvain.fouchard'], ['lola.pointer', 'nicolas.clerc'], ['sylvain.fouchard', 'lola.pointer'], ['lola.pointer', 'sylvain.fouchard'], ['lola.pointer', 'nicolas.clerc'], ['lola.pointer', 'sylvain.fouchard'], ['sylvain.fouchard', 'lola.pointer'], ['william.lefort', 'lola.pointer'], ['lola.pointer', 'nicolas.clerc'], ['sylvain.fouchard', 'lola.pointer'], ['sylvain.fouchard', 'lola.pointer'], ['sylvain.fouchard', 'lola.pointer'], ['sylvain.fouchard', 'lola.pointer'], ['sylvain.fouchard', 'lola.pointer'], ['sylvain.fouchard', 'lola.pointer'], ['sylvain.fouchard', 'lola.pointer'], ['lola.pointer', 'sylvain.fouchard'], ['lola.pointer', 'sylvain.fouchard'], ['lola.pointer', 'sylvain.fouchard'], ['lola.pointer', 'sylvain.fouchard'], ['william.lefort', 'lola.pointer'], ['sylvain.fouchard', 'lola.pointer'], ['nicolas.clerc', 'laurent.villeneuve'], ['nicolas.clerc', 'lola.pointer'], ['william.lefort', 'lola.pointer'], ['lola.pointer', 'sylvain.fouchard'], ['nicolas.clerc', 'laurent.villeneuve'], ['nicolas.clerc', 'lola.pointer'], ['william.lefort', 'lola.pointer'], ['lola.pointer', 'sylvain.fouchard'], ['william.lefort', 'lola.pointer'], ['william.lefort', 'lola.pointer'], ['william.lefort', 'lola.pointer'], ['william.lefort', 'lola.pointer'], ['sylvain.fouchard', 'lola.pointer'], ['sylvain.fouchard', 'lola.pointer'], ['sylvain.fouchard', 'lola.pointer'], ['sylvain.fouchard', 'lola.pointer'], ['lola.pointer', 'sylvain.fouchard'], ['sylvain.fouchard', 'lola.pointer'], ['sylvain.fouchard', 'lola.pointer'], ['lola.pointer', 'sylvain.fouchard'], ['sylvain.fouchard', 'lola.pointer'], ['lola.pointer', 'sylvain.fouchard'], ['william.lefort', 'lola.pointer'], ['lola.pointer', 'sylvain.fouchard'], ['lola.pointer', 'sylvain.fouchard'], ['sylvain.fouchard', 'lola.pointer'], ['lola.pointer', 'sylvain.fouchard'], ['sylvain.fouchard', 'lola.pointer'], ['lola.pointer', 'sylvain.fouchard'], ['sylvain.fouchard', 'lola.pointer'], ['lola.pointer', 'sylvain.fouchard'], ['lola.pointer', 'sylvain.fouchard'], ['lola.pointer', 'sylvain.fouchard'], ['lola.pointer', 'sylvain.fouchard']]
    send(data=data)
