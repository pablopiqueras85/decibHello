import duckdb, time
t=time.time()
con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs; INSTALL spatial; LOAD spatial; CREATE SECRET anon (TYPE s3, KEY_ID '', SECRET '', REGION 'us-west-2');")
q = """
COPY (
SELECT id, names.primary AS nombre, taxonomy.primary AS categoria, basic_category, taxonomy.hierarchy AS jerarquia, operating_status, confidence,
       ST_X(geometry) AS lon, ST_Y(geometry) AS lat, sources[1].dataset AS fuente, sources[1].update_time AS actualizado
FROM read_parquet('s3://overturemaps-us-west-2/release/2026-09-23.1/theme=places/type=place/*', hive_partitioning=1)
WHERE bbox.xmin BETWEEN 2.05 AND 2.23 AND bbox.ymin BETWEEN 41.32 AND 41.47
) TO 'overture/bcn_places.parquet' (FORMAT PARQUET)
"""
con.execute(q)
print('s', round(time.time()-t))
print(con.execute("SELECT count(*), count(*) FILTER (WHERE operating_status='open') FROM 'overture/bcn_places.parquet'").fetchall())
print(con.execute("SELECT categoria, count(*) n FROM 'overture/bcn_places.parquet' WHERE categoria ILIKE '%bar%' OR categoria ILIKE '%pub%' OR categoria ILIKE '%club%' OR categoria ILIKE '%lounge%' OR categoria ILIKE '%restaurant' GROUP BY 1 ORDER BY n DESC LIMIT 20").fetchall())
print(con.execute("SELECT operating_status, count(*) FROM 'overture/bcn_places.parquet' GROUP BY 1").fetchall())
print(con.execute("SELECT fuente, count(*) FROM 'overture/bcn_places.parquet' GROUP BY 1").fetchall())
print(con.execute("SELECT basic_category, count(*) n FROM 'overture/bcn_places.parquet' GROUP BY 1 ORDER BY n DESC LIMIT 25").fetchall())
