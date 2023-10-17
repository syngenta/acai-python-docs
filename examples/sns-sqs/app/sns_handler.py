from acai_aws.sns.requirements import requirements


@requirements()
def handle(event):
    for record in event.records:
        print(record)