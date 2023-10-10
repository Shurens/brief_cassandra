from fastapi import FastAPI, Depends
from cassandra.cluster import Cluster
import uvicorn
import random

app = FastAPI()

# cluster = Cluster(['0.0.0.0'],port=9042)
# session = cluster.connect('resto',wait_for_all_pools=True)
# session.execute('USE resto')

cluster1 = Cluster(['localhost'], port=9042)
session1 = cluster1.connect('resto')
session1.execute('USE resto')

cluster2 = Cluster(['localhost'], port=9043)
session2 = cluster2.connect('resto')
session2.execute('USE resto')


def is_node_up(session):
    try:
        session.execute('SELECT * FROM system.local')
        return True
    except Exception:
        return False
    
# Function to select a Cassandra session based on the provided ID.
# If no ID is provided, a session is randomly selected.
def get_session(id: int = None):
    if id is None:
        session = random.choice([session1, session2])
        return session if is_node_up(session) else None
    elif id % 2 == 0:
        return session1 if is_node_up(session1) else None
    else:
        return session2 if is_node_up(session2) else None


# Route pour récupérer les infos d'un restaurant en fonction de son ID
@app.get("/restaurant/{restaurant_id}")
def get_restaurant_info(restaurant_id: int, session = Depends(get_session)):
    query = f"SELECT * FROM restaurant WHERE id = {restaurant_id}"
    result = session.execute(query)
    return result.one()

# Route pour le nom des restaurants en fonction de leur type de cuisine
@app.get("/restaurants_by_cuisine_type/{cuisine_type}")
def get_restaurants_by_cuisine(cuisine_type: str, session = Depends(get_session)):
    query = f"SELECT name FROM restaurant WHERE cuisinetype = '{cuisine_type}'"
    result = session.execute(query)
    restaurant_names = []
    for row in result:
        restaurant_names.append(row.name)
    
    return restaurant_names

# Route pour le nombre d'inspection d'un restaurant en fonction de son ID
@app.get("/restaurant_inspection_count/{restaurant_id}")
def get_inspection_count(restaurant_id: int, session = Depends(get_session)):
    query = f"SELECT COUNT(*) FROM inspection WHERE idrestaurant = {restaurant_id}"
    result = session.execute(query)
    return result.one()[0] #[0] pour le formatage car ça retourne une liste d'une valeur

 
@app.get("/restaurants-by-grade/{grade}")
def get_restaurants_by_grade(grade: str, session = Depends(get_session)):
    query = f"SELECT * FROM inspection WHERE grade = '{grade}' LIMIT 10"
    result = session.execute(query)
    restaurants = []

    for row in result:
        # récup l'id du restaurant à partir de la colonne "idrestaurant" de la table d'inspection
        restaurant_id = row.idrestaurant
        restaurant_query = f"SELECT * FROM restaurant WHERE id = {restaurant_id}"
        restaurant_result = session.execute(restaurant_query)
        restaurant_data = restaurant_result.one()

        if restaurant_data:
            restaurant_dict = {
            "id": restaurant_data.id,
            "name": restaurant_data.name,
            "cuisine_type": restaurant_data.cuisinetype,
            "grade": row.grade,
            }
            restaurants.append(restaurant_dict)

    if restaurants:
        return restaurants
    else:
        return {f"message": "Aucun restaurant trouvé pour ce type de grade"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)