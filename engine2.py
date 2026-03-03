import pandas as pd
import ipaddress
from collections import defaultdict, deque
from compliance import map_compliance

SENSITIVE_PORTS = [
    "3306", "5432", "5439", "1433",
    "6379", "22", "3389",
    "9200", "6443"
]

def safe(v):
    if pd.isna(v):
        return ""
    return str(v).strip()

def is_public(cidr):
    try:
        return not ipaddress.ip_network(cidr, strict=False).is_private
    except:
        return False

def normalize_columns(df):
    df.columns = df.columns.str.strip()
    return df

def calculate_score(rule_type, port, source):
    score = 0

    if port in SENSITIVE_PORTS:
        score += 4

    if rule_type == "inbound":
        score += 2

    if source == "0.0.0.0/0":
        score += 4
    elif "/" in source and is_public(source):
        score += 3

    return min(score, 10)

def classify(score):
    if score >= 8:
        return "Critical"
    elif score >= 6:
        return "High"
    elif score >= 3:
        return "Medium"
    return "Low"

def build_graph(df):
    graph = defaultdict(list)

    for _, row in df.iterrows():
        rule_type = safe(row.get("Rule Type")).lower()
        source = safe(row.get("Source/Destination"))
        dest = safe(row.get("Security Group"))

        if rule_type == "inbound":
            graph[source].append(dest)

    return graph

def find_attack_chains(graph):
    attack_chains = []
    entry_points = ["0.0.0.0/0"]

    for entry in entry_points:
        queue = deque([[entry]])

        while queue:
            path = queue.popleft()
            current = path[-1]

            if current not in graph:
                continue

            for neighbor in graph[current]:
                new_path = path + [neighbor]

                if len(new_path) > 5:
                    continue

                if any(keyword in neighbor.lower() for keyword in ["db","redis","ldap","rds"]):
                    attack_chains.append(" → ".join(new_path))
                else:
                    queue.append(new_path)

    return attack_chains

def analyze(df):

    df = normalize_columns(df)
    graph = build_graph(df)

    results = []

    for _, row in df.iterrows():

        rule_type = safe(row.get("Rule Type")).lower()
        port = safe(row.get("Port Range"))
        source = safe(row.get("Source/Destination"))
        desc = safe(row.get("Description")).lower()

        score = calculate_score(rule_type, port, source)
        severity = classify(score)

        findings = []

        if is_public(source) and port in SENSITIVE_PORTS:
            findings.append("Public Sensitive Exposure")

        if rule_type == "outbound" and source == "0.0.0.0/0":
            findings.append("Unrestricted Outbound")

        if any(x in desc for x in ["delete", "tmp", "test"]):
            findings.append("Suspicious Rule")

        if not findings:
            findings.append("No Immediate Risk")

        cis, pci = map_compliance(findings)

        results.append({
            **row,
            "Risk Score (0-10)": score,
            "Severity": severity,
            "Findings": ", ".join(findings),
            "CIS Control": cis,
            "PCI DSS Requirement": pci
        })

    analyzed_df = pd.DataFrame(results)

    attack_chain_df = pd.DataFrame({
        "Attack Chain": find_attack_chains(graph)
    })

    return analyzed_df, attack_chain_df
