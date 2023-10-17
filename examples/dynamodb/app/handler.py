from acai_aws.dynamodb.requirements import requirements


@requirements(operations=['created', 'deleted'])
def handle(event):
    for record in event.records:
        print(record)