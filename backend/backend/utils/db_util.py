from bson import ObjectId
from backend.database import database


def populate_ref_array(original_list, ref_col, key):
    ref_col = database[ref_col]

    for record in original_list:
        ids = []

        for ref in record[key]:
            ids.append(ref['_id'])

        ref_array = list(ref_col.find({'_id': {'$in': ids}}))

        record[key] = ref_array

    return original_list


def populate_single_ref_array(original_record, ref_col, key):
    ids = []
    ref_col = database[ref_col]

    for ref in original_record[key]:
        ids.append(ref['_id'])

    ref_array = list(ref_col.find({'_id': {'$in': ids}}))

    original_record[key] = ref_array

    return original_record


def populate_array_ref(original_list, ref_col, key):
    ref_col = database[ref_col]

    for record in original_list:
        if record[key]:
            ref = ref_col.find_one({'_id': ObjectId(record[key]['_id'])})

            record[key] = ref

    return original_list


def populate_ref(original_record, ref_col, key):
    ref_col = database[ref_col]

    if original_record[key]:
        ref = ref_col.find_one({'_id': ObjectId(original_record[key]['_id'])})

        original_record[key] = ref

    return original_record
