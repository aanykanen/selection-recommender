

SELECT 
  i.itemnumber AS item_id,
  s.datetime as action_date,
  s.type AS circ_type
FROM statistics s
LEFT JOIN items i ON (s.itemnumber=i.itemnumber)
WHERE
  s.type IN ('issue', 'renew') AND
  (i.itemcallnumber LIKE <ITEMCALLNUMBER HERE>) AND
  i.itype='KI'
INTO OUTFILE '/tmp/circulation_available.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'; 
