
Main goal: recommend songs for a given audience. The database is a set of tracks per user with a given score based on the user's tastes.

### Installation

- Setup environment

```
virtualenv venv
source venv/bin/activate
pip install -r requirements
```

- Jupyter python 2 kernel (if necessary)

```
python2 -m ipykernel install --user
```

- Download the data

```
mkdir data
```

Download the json file into this folder.

Structure of the data : Array of array of tracks

```json
  {
    "artist": "Name",
    "genre": "Disco",
    "id": 1234,
    "score": 0.123456789
  }
```


- Run the jupyter notebook

```
jupyter notebook
```

### Exploration

The exploratoring part can be seen using [exploratory.ipynb](https://github.com/tillmd/???/blob/master/exploratory.ipynb)

We examine the basics statistics of the database, some tops, the score distribution. We also compute the correlation between artists that we will use in our recommendation process.

### Recommendation

We want to recommend songs for an audience who have different tastes.
The main strategy is :

  - A track oriented recommendation
    + Find common tracks to each user with a high score
    + From this track find a correlated track unknow from the users
    + If one user doesn't know the song, the correlated song can be known by him. Thus N-1 people will like the song, and one user will be happy to say he knew this song.
  - An artist oriented recommendation
    + Same behavior to choose an artist
    + (not implemented) The song can then be pick in the artist catalog according to the knowledge of the users 

We didn't use the `genre` field because of its unprecision :

```json
    {
      "artist": "Mozart",
      "genre": "Electro",
      "id": 399137,
      "score": 0.6105205207831543
    },
```

```json
    {
      "artist": "2be3",
      "genre": "Funk",
      "id": 988837,
      "score": 0.9371904213393983
    },
```

```json
    {
      "artist": "The Offspring",
      "genre": "RnB",
      "id": 515570,
      "score": 0.8552045099017862
    },
```

```json
    {
      "artist": "Booba",
      "genre": "Disco",
      "id": 346766,
      "score": 0.2840838314868537
    },
```

