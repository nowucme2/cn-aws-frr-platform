import boto3
import pandas as pd

def fetch_security_groups():

    ec2 = boto3.client("ec2")

    response = ec2.describe_security_groups()

    records = []

    for sg in response["SecurityGroups"]:
        sg_id = sg["GroupId"]

        for perm in sg["IpPermissions"]:
            from_port = perm.get("FromPort", "All")
            for ip_range in perm.get("IpRanges", []):
                records.append({
                    "Security Group": sg_id,
                    "Rule Type": "inbound",
                    "Port Range": str(from_port),
                    "Source/Destination": ip_range["CidrIp"]
                })

    return pd.DataFrame(records)
