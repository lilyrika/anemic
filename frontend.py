from backend import Database

database = Database()
def cur(cmd): database.cur.execute(cmd)
def wipe():
    cur("DELETE FROM Albums")
    cur("DELETE FROM Ratings")
    cur("DELETE FROM Genres")

##########

wipe()

database.add_album("Carrie & Lowell", "Sufjan Stevens", "2015", True)
database.add_album("In The Aeroplane Over The Sea", "Neutral Milk Hotel", "1998")
database.add_album("PetroDragonic Apocalypse", "King Gizzard & The Lizard Wizard", "2023")
database.add_album("Diamond Jubilee", "Cindy Lee", "2024")

database.add_genre(1, "Indie Folk")
database.add_genre(2, "Indie Folk")
database.add_genre(3, "Thrash Metal")
database.add_genre(3, "Progressive Metal")
database.add_genre(4, "Hypnagogic Pop")

database.add_rating(1, 1, 9)
database.add_rating(1, 2, 10)
database.add_rating(1, 3, 10)
database.add_rating(1, 4, 10)

database.update_chart()
database.genre_profile("Indie Folk")
print()
database.genre_profile("Thrash Metal")
print()
database.genre_profile("Hypnagogic Pop")