import boto3

CLIENT = boto3.client("lambda")


def clean_old_version(function) -> None:
    all_versions = CLIENT.list_versions_by_function(
        FunctionName=function["FunctionArn"], MaxItems=400
    )["Versions"]
    highest_version = max((version["Version"] for version in all_versions))
    to_delete = [
        version
        for version in all_versions
        if version["Version"] not in (highest_version, function["Version"])
    ]
    print(function["FunctionName"])
    for version in to_delete:
        arn = version["FunctionArn"]
        print(f"delete_function(FunctionName={arn})")
        CLIENT.delete_function(FunctionName=arn)


def clean_old_lambda_versions():
    marker = ""
    while marker is not None:
        if marker:
            functions = CLIENT.list_functions(Marker=marker)
        else:
            functions = CLIENT.list_functions()

        for function in functions["Functions"]:
            clean_old_version(function)

        marker = functions.get("NextMarker")


if __name__ == "__main__":
    clean_old_lambda_versions()
