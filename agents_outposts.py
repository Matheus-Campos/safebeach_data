import os
import xlrd as xls
import psycopg2 as pg

def main():
    db_host = os.getenv('DB_HOST', 'db')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'root')
    db_name = os.getenv('DB_NAME', 'safebeach')
    conn = pg.connect(host=db_host, user=db_user, password=db_password, database=db_name)

    wb = xls.open_workbook('data/Postos de Guarda Vidas.xls')
    sheet = wb.sheet_by_index(0)
    attr_names = ['name', 'lat', 'lng']

    outposts = map(lambda row: parse_to_outpost(sheet, attr_names, row), range(sheet.nrows)[1:])
    for outpost in outposts:
        insert_outpost_into_db(conn, outpost)

def parse_to_outpost(sheet, attr_names, row):
    outpost = {}
    for i in range(len(attr_names)):
        attr = attr_names[i]
        outpost[attr] = sheet.cell(row, i).value
    return outpost

def insert_outpost_into_db(conn, outpost):
    cursor = conn.cursor()
    sql = f"""
        INSERT INTO agent_outposts (name, latitude, longitude, location) VALUES
            ('{outpost['name']}', {outpost['lat']}, {outpost['lng']}, 'POINT({outpost['lat']} {outpost['lng']})');
    """
    cursor.execute(sql)
    conn.commit()

if __name__ == '__main__':
    main()
