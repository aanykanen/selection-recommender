

SELECT 
  di.itemnumber AS item_id,
  s.datetime as action_date,
  s.type AS circ_type
FROM statistics s
LEFT JOIN deleteditems di ON (s.itemnumber=di.itemnumber)
WHERE
  s.type IN ('issue', 'renew') AND
  (di.itemcallnumber LIKE <ITEMCALLNUMBER HERE>) AND
  di.itype='KI'
INTO OUTFILE '/tmp/circulation_deleted.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'; 
