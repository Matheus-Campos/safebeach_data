CREATE_AGENT_OUTPOSTS_TABLE = """
    CREATE TABLE IF NOT EXISTS agent_outposts (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name VARCHAR(255) NOT NULL,
        location geography(Point, 4326) NOT NULL,
        latitude DOUBLE PRECISION NOT NULL,
        longitude DOUBLE PRECISION NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT now(),
        updated_at TIMESTAMP NOT NULL DEFAULT now()
    )
    """

DROP_AGENT_OUTPOSTS_TABLE = "DROP TABLE IF EXISTS agent_outposts;"

INSERT_AGENT_OUTPOST = "INSERT INTO agent_outposts (name, latitude, longitude, location) VALUES (%s, %s, %s, %s);"

CREATE_SHARK_INCIDENTS_TABLE = """
    CREATE TABLE IF NOT EXISTS shark_incidents (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        victim_survived BOOLEAN DEFAULT true,
        date DATE NOT NULL,
        moon_phase moon_phase NOT NULL,
        wound VARCHAR(255),
        next_to VARCHAR(255),
        beach VARCHAR(255) NOT NULL,
        city VARCHAR(255) NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT now(),
        updated_at TIMESTAMP NOT NULL DEFAULT now()
    );
    """

CREATE_MOON_PHASE_TYPE = (
    "CREATE TYPE moon_phase AS ENUM ('new', 'waxing', 'full', 'waning');"
)

DROP_SHARK_INCIDENTS_TABLE = "DROP TABLE IF EXISTS shark_incidents;"

DROP_MOON_PHASE_TYPE = "DROP TYPE IF EXISTS moon_phase;"

INSERT_SHARK_INCIDENT = "INSERT INTO shark_incidents (victim_survived, date, moon_phase, wound, next_to, beach, city) VALUES (%s, %s, %s, %s, %s, %s, %s)"

SELECT_SHARK_INCIDENTS = "SELECT id, victim_survived, date, moon_phase, wound, next_to, beach, city FROM shark_incidents;"

SELECT_NEAREST_AGENT_OUTPOST = """
    SELECT
        name,
        latitude,
        longitude,
        ST_Distance(location, 'SRID=4326;Point(%s %s)'::geography) as distance
    FROM agent_outposts ORDER BY distance LIMIT 1;
    """
