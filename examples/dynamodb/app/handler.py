from acai_aws.dynamodb.requirements import requirements


@requirements(operations=['created', 'deleted'])
def stream(event):
    for record in event.records:
        print(record)