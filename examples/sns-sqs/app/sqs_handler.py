from acai_aws.sqs.requirements import requirements


@requirements()
def handle(event):
    for record in event.records:
        print(record)