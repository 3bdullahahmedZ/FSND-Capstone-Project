# FSND-Capstone-Project

## Requirments
- Python 3.9
- Virtual env

```bash
pip install -r requirements.txt
```

## Documentation

` GET '/actors'`
- Fetches a dictionary of actors with attributes id, name, age, gender and movies they are in 
- Request Arguments: None
- Request Body: None
- Returns: A list of actors and a success state
```json
{
    "actors": [
        {
            "age": 58,
            "gender": "male",
            "id": 3,
            "movies": [],
            "name": "Brad Pitt"
        }
    ],
    "success": true
}
```

` POST '/actors'`
- Adds an new actor with the given attributes
- Request Arguments: None
- Request Body:
```json
{
    "name": "Brad Pitt",
    "gender": "male",
    "age": 58
}
```
- Returns: Added actor's attributes and success state
```json
{
    "actor": {
        "age": 58,
        "gender": "male",
        "id": 3,
        "movies": [],
        "name": "Brad Pitt"
    },
    "success": true
}
```

` PATCH '/actor/<int:actor_id>'`
- Modifies actor with the given id 
- Request Arguments: Actor id
- Request Body:
```json 
{
    "age": 59
}
```
- Returns: Actor after modification and success state
```json
{
    "actor": {
        "age": 59,
        "gender": "male",
        "id": 3,
        "movies": [],
        "name": "Brad Pitt"
    },
    "success": true
}
```

` DELETE '/actors/<int:actor_id>'`
- Deletes actor with the given id
- Request Arguments: Actor id
- Request Body: None
- Returns: Id of deleted actor and success state
```json
{
    "deleted": 1,
    "success": true
}
```

` GET '/movies'`
- Fetches a dictionary of movies with attributes id, title, release_date, and the cast
- Request Arguments: None
- Request Body: None
- Returns: A list of actors and a success state
```json
{
    "movies": [
        {
            "actors": [
                {
                    "id": 3,
                    "name": "Brad Pitt"
                }
            ],
            "id": 2,
            "release_date": "1 Aug 2022",
            "title": "Bullet Train"
        }
    ],
    "success": true
}
```

` POST '/movies'`
- Adds an new movie with the given attributes
- Request Arguments: None
- Request Body:
```json
{
    "title": "Bullet Train",
    "release_date": "1 Aug 2022",
    "cast": [3]
}
```
- Returns: Success state
```json
{
    "success": true
}
```

` PATCH '/movies/<int:movie_id>'`
- Modifies movie with the given id 
- Request Arguments: Movie id
- Request Body:
```json 
{
    "release_date": "2 Aug 2022"
}
```
- Returns: Movie after modification and success state
```json
{
    "movie": {
        "actors": [
            {
                "id": 3,
                "name": "Brad Pitt"
            }
        ],
        "id": 2,
        "release_date": "2 Aug 2022",
        "title": "Bullet Train"
    },
    "success": true
}
```

` DELETE '/movies/<int:movie_id>'`
- Deletes movie with the given id
- Request Arguments: movie id
- Request Body: None
- Returns: Id of deleted movie and success state
```json
{
    "deleted": 1,
    "success": true
}
```






