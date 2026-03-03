def map_compliance(findings):

    cis_controls = []
    pci_requirements = []

    for finding in findings:

        if "Public Sensitive Exposure" in finding:
            cis_controls.append("CIS 4.1 - Restrict Inbound Traffic")
            pci_requirements.append("PCI DSS 1.2 - Restrict Inbound Traffic")

        if "Unrestricted Outbound" in finding:
            cis_controls.append("CIS 4.2 - Restrict Outbound Traffic")
            pci_requirements.append("PCI DSS 1.3 - Control Outbound Traffic")

        if "Suspicious Rule" in finding:
            cis_controls.append("CIS 1.1 - Review Security Configurations")
            pci_requirements.append("PCI DSS 2.2 - Secure Configurations")

    if not cis_controls:
        cis_controls.append("Compliant")

    if not pci_requirements:
        pci_requirements.append("Compliant")

    return ", ".join(set(cis_controls)), ", ".join(set(pci_requirements))
