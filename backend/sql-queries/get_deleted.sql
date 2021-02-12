

SELECT 
  b.biblionumber AS bib_id, 
  di.itemnumber AS item_id, 
  b.author AS author,
  b.title AS title,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][1]/subfield[@code="a"]') AS subject_1,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][1]/subfield[@code="x"]') AS subject_1_source,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][2]/subfield[@code="a"]') AS subject_2,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][2]/subfield[@code="x"]') AS subject_2_source,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][3]/subfield[@code="a"]') AS subject_3,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][3]/subfield[@code="x"]') AS subject_3_source,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][4]/subfield[@code="a"]') AS subject_4,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][4]/subfield[@code="x"]') AS subject_4_source,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][5]/subfield[@code="a"]') AS subject_5,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][5]/subfield[@code="x"]') AS subject_5_source,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][6]/subfield[@code="a"]') AS subject_6,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][6]/subfield[@code="x"]') AS subject_6_source,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][7]/subfield[@code="a"]') AS subject_7,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][7]/subfield[@code="x"]') AS subject_7_source,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][8]/subfield[@code="a"]') AS subject_8,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][8]/subfield[@code="x"]') AS subject_8_source,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][9]/subfield[@code="a"]') AS subject_9,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][9]/subfield[@code="x"]') AS subject_9_source,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][10]/subfield[@code="a"]') AS subject_10,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][10]/subfield[@code="x"]') AS subject_10_source,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][11]/subfield[@code="a"]') AS subject_11,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][11]/subfield[@code="x"]') AS subject_11_source,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][12]/subfield[@code="a"]') AS subject_12,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][12]/subfield[@code="x"]') AS subject_12_source,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][13]/subfield[@code="a"]') AS subject_13,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][13]/subfield[@code="x"]') AS subject_13_source,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][14]/subfield[@code="a"]') AS subject_14,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][14]/subfield[@code="x"]') AS subject_14_source,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][15]/subfield[@code="a"]') AS subject_15,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="650"][15]/subfield[@code="x"]') AS subject_15_source,
  ExtractValue(biblio_metadata.metadata,'//datafield[@tag="830"]/subfield[@code="a"]') AS series,
  di.itemcallnumber AS genre,
  bi.isbn AS isbn,
  b.copyrightdate AS pub_year,
  di.dateaccessioned AS acquired,
  di.datelastborrowed AS last_borrowed,
  di.issues AS issues,
  di.renewals AS renewals,
  di.timestamp AS date_deleted
FROM deleteditems di
LEFT JOIN biblioitems bi ON di.biblioitemnumber=bi.biblioitemnumber
LEFT JOIN biblio b ON bi.biblionumber=b.biblionumber
LEFT JOIN biblio_metadata ON b.biblionumber=biblio_metadata.biblionumber
WHERE
  (di.itemcallnumber LIKE <ITEMCALLNUMBER HERE>) AND
  di.itype='KI'
INTO OUTFILE '/tmp/iteminfo_deleted.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
