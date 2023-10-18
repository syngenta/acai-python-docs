from acai_aws.s3.requirements import requirements


@requirements(
    operations=['created', 'deleted'],
    get_object=True,
    data_type='json'
)
def handle(event):
    for record in event.records:
        print(record)
        print(record.body)