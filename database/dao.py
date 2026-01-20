from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_all_artists(n_alb):

        conn = DBConnect.get_connection()
        result = {}
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT distinct a.id,a.name, count(*) as num_album
                FROM artist a,album al
                where a.id = al.artist_id 
                group by a.id,a.name
                having count(*)>=%s
                """
        cursor.execute(query,(n_alb,))
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'],num_album= row['num_album'])
            result[row['id']]= artist
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def get_conessioni(artisti):

        conn = DBConnect.get_connection()
        result = {}
        cursor = conn.cursor(dictionary=True)
        query = """select a1.artist_id as art1, a2.artist_id as art2, count(distinct t1.genre_id) as generi_comune
                   from album a1, album a2, track t1, track t2
                   where a1.artist_id != a2.artist_id and a1.id = t1.album_id  and a2.id = t2.album_id and t1.genre_id = t2.genre_id
                   group by  a1.artist_id, a2.artist_id \
                """
        cursor.execute(query)
        for row in cursor:
            if row['art1'] in artisti and row['art2'] in artisti:
                result[row['art1'],row['art2']] = row['generi_comune']
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_d_min(d):

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor()
        query = """select distinct a.artist_id
                        from track t, album a
                        where a.id = t.album_id and  t.milliseconds/60000  >= %s
                """
        cursor.execute(query,(d,))
        for row in cursor:
           result.append(row)

        cursor.close()
        conn.close()
        return result