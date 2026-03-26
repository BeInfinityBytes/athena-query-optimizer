from aws.aws_client import glue_client

def get_table_schema(database, table):

    response = glue_client.get_table(
        DatabaseName=database,
        Name=table
    )

    columns = response["Table"]["StorageDescriptor"]["Columns"]

    return [col["Name"] for col in columns]