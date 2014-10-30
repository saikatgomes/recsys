PRAGMA foreign_keys=OFF;
PRAGMA synchronous=OFF;
BEGIN TRANSACTION;
CREATE TABLE allData(key varchar(128), value varchar(2048));
CREATE INDEX keyIndex on allData (key);
COMMIT;
