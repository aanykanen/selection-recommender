#!/bin/bash
ITEM_AVAILABLE=`dirname $0`"/iteminfo_available.csv"
ITEM_DELETED=`dirname $0`"/iteminfo_deleted.csv"
CIRC_AVAILABLE=`dirname $0`"/circulation_available.csv"
CIRC_DELETED=`dirname $0`"/circulation_deleted.csv"

if [ ! -f "$ITEM_AVAILABLE" ]; then
    echo "Item info regarding available items does not exist!"
    exit 0
fi

if [ ! -f "$ITEM_DELETED" ]; then
    echo "Item info regarding deleted items does not exist!"
    exit 0
fi

if [ ! -f "$CIRC_AVAILABLE" ]; then
    echo "Circulation info regarding available items does not exist!"
    exit 0
fi

if [ ! -f "$CIRC_DELETED" ]; then
    echo "Circulation info regarding available items does not exist!"
    exit 0
fi

cat "$ITEM_AVAILABLE" | perl -pe 's/$/\,\"\"/' > `dirname $0`"/foo"
cat `dirname $0`"/foo" "$ITEM_DELETED" > `dirname $0`"/bar"
perl -pe 's/\\\"//g' `dirname $0`"/bar" > `dirname $0`"/items.csv"
cat "$CIRC_AVAILABLE" "$CIRC_DELETED" > `dirname $0`"/circulation.csv"
rm `dirname $0`"/foo" `dirname $0`"/bar"

echo "Item and circulation files concatenated successfully!"
