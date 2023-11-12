import sys
import xlrd as xls

import db

conn = None

def main():
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

def create_table_if_not_exists():
    cur = conn.cursor()
    create_table = '''
    CREATE TABLE IF NOT EXISTS agent_outposts (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name VARCHAR(255) NOT NULL,
        location geography(Point, 4326) NOT NULL,
        latitude DOUBLE PRECISION NOT NULL,
        longitude DOUBLE PRECISION NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT now(),
        updated_at TIMESTAMP NOT NULL DEFAULT now()
    )
    '''

    cur.execute(create_table)
    conn.commit()


def drop_table():
    cur = conn.cursor()
    drop_table = 'DROP TABLE IF EXISTS agent_outposts;'

    cur.execute(drop_table)
    conn.commit()

if __name__ == '__main__':
    conn = db.connect()

    migration = None
    if len(sys.argv) > 1:
        migration = sys.argv[1]

    if migration == 'up':
        create_table_if_not_exists()
    elif migration == 'down':
        drop_table()
    elif migration is None:
        main()
