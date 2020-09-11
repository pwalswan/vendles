import json
import uuid
import psycopg2

from load_properties import load_etl_properties


def process(text):
    print(f'Status, {text}')

    with open('input.json') as input_file:
        for line in input_file:
            json_line = json.loads(line)

            eventId = uuid.uuid4()
            insertEvent(json_line, eventId)
            insertCustomer(json_line)
            insertAddresses(json_line, 'billing_address')
            insertAddresses(json_line, 'shipping_address')
            insertLineItem(json_line, eventId)


def insertEvent(json_line, eventId):

    s_insert = "INSERT INTO event ("
    s_values = " VALUES ("
    s_insert += " id, event_type, customer_id, " \
                "event_version, currency, financial_status, " \
                "total_discounts, total_tax, discount_codes, buyer_accepts_marketing, " \
                " event_date, "
    s_values += " '" + str(eventId) + "', " + " '" + json_line['event_type'] + "', '" + json_line['lovevery_user_id'] + "', " + \
                " '" + json_line['event_version'] + "', '" + json_line['currency'] + "', '" + json_line[
                    'financial_status'] + "', " + \
                " '" + str(json_line['total_discounts']) + "', '" + str(json_line['total_tax']) + "', '" + \
                json_line['discount_codes'] + "', " + \
                " '" + str(json_line['buyer_accepts_marketing']) + "', " + \
                " '" + json_line['event_date'] + "', "

    s_insert = s_insert[:-2] + ")"
    s_values = s_values[:-2] + ")"

    s_insert += s_values
    print(s_insert)

    insertRecord(s_insert)


def insertCustomer(json_line):
    s_insert = "INSERT INTO customer ("
    s_values = " VALUES ("

    s_insert += " lovevery_user_id, email, " \
                "first_name, last_name, "
    s_values += " '" + json_line['lovevery_user_id'] + "', '" + json_line['email'] + "', " + \
                " '" + json_line['first_name'] + "', '" + json_line['last_name'] + "', "

    s_insert = s_insert[:-2] + ")"
    s_values = s_values[:-2] + ")"

    s_insert += s_values
    print(s_insert)

    insertRecord(s_insert)


def insertAddresses(json_line, addressType):
    s_insert = "INSERT INTO address ("
    s_values = " VALUES ("

    s_insert += " customer_id, address1, " \
                "address2, city, " \
                "province, country, zip, phone, " \
                "address_type, "
    s_values += " '" + json_line['lovevery_user_id'] + "', '" + json_line[addressType]['address1'] + "', " + \
                " '" + json_line[addressType]['address2'] + "', '" + json_line[addressType]['city'] + "', " + \
                " '" + json_line[addressType]['province'] + "', '" + json_line[addressType]['country'] + "', " + \
                " '" + json_line[addressType]['zip'] + "', '" + json_line[addressType]['phone'] + "', " + \
                " '" + addressType + "', "

    s_insert = s_insert[:-2] + ")"
    s_values = s_values[:-2] + ")"

    s_insert += s_values
    print(s_insert)

    insertRecord(s_insert)

def insertLineItem(json_line, eventId):
    s_insert = "INSERT INTO line_items ("
    s_values = " VALUES ("

    s_insert += " event_id, " \
                "quantity, product_id, "
    s_values += " '" + str(eventId) + "', '" + json_line['line_items'][0]['quantity'] + "', " + \
                " '" + json_line['line_items'][0]['id'] + "', "

    s_insert = s_insert[:-2] + ")"
    s_values = s_values[:-2] + ")"

    s_insert += s_values
    print(s_insert)

    insertRecord(s_insert)


def insertRecord(s_insert, x=None):
    cursor = conn.cursor()

    try:
        cursor.execute(s_insert)
        cursor.execute("commit;")
        print("Insert successful.")
    except Exception as err:
        print(err)


if __name__ == '__main__':
    global etlp
    etlp = load_etl_properties('etl.properties', ';', '#')

    global conn_info
    conn_info = {'host': etlp['postgresJdbcUrl'],
                 'port': int(etlp['postgresPort']),
                 'user': etlp['postgresJdbcUser'],
                 'password': etlp['postgresPassword'],
                 'database': etlp['postgresDatabase']}

    global conn
    conn = psycopg2.connect(**conn_info)
    print(f'Connected to', conn_info['host'])

    process('Running..')
