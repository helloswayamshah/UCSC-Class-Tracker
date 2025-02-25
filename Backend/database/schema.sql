CREATE TABLE IF NOT EXISTS Users(
  guid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(320) NOT NULL UNIQUE,
  password VARCHAR(100) NOT NULL,
  phoneNo BYTEA NOT NULL,
  pingMedium CHAR(1) NOT NULL
);

CREATE TABLE IF NOT EXISTS Trackers(
  guid UUID PRIMARY KEY REFERENCES Users(guid),
  courses jsonb DEFAULT '[]',
  term VARCHAR(20),
  cache jsonb DEFAULT '{}'
);
