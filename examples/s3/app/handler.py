from acai_aws.s3.requirements import requirements


@requirements(operations=['created', 'deleted'])
def handle(event):
    for record in event.records:
        print(record)