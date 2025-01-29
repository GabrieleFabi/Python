
from vins import fetch_vins_from_db

def test_vin_discrepancies():
    """Check for discrepancies in VINs between vins.txt and the database"""

    # load VINs from database
    vins_db = fetch_vins_from_db()

    # Load VINs from text file
    vins_file = open('vins.txt', 'r')
    vins_txt = vins_file.read().splitlines()

    # Convert to sets for easy comparison
    vins_db = set(vins_db)
    vins_txt = set(vins_txt)

    # Check for VINs in db not in txt and vice versa
    vins_db_not_tx = vins_db - vins_txt
    vins_txt_not_db = vins_txt - vins_db

    assert len(vins_db_not_tx) == 0 and len(vins_txt_not_db) == 0, \
        f"VIN discrepancies found!\n" \
        f"VINs in database not in vins.txt: {vins_db_not_tx}\n" \
        f"VINs in vins.txt not in database: {vins_txt_not_db}"

