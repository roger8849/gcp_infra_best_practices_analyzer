import time
from markdown import markdown
import pdfkit

report_template = """

# Google Cloud Network Configuration Analysis Report

## Introduction

This report provides a comprehensive analysis of your Google Cloud network configuration, focusing on Virtual Private Clouds (VPCs), firewall rules, subnets, and VPN connectivity. It aims to identify potential areas for improvement by comparing your current setup against Google Cloud's best practices.

The report is structured as follows:

- **Network Configuration:**  Details of your existing VPCs, firewall rules, subnets, and VPN connections.
- **Best Practices:**  A summary of Google Cloud's recommended best practices for VPC and VPN configuration.
- **Analysis:**  Evaluation of your current configuration in light of the best practices.
- **Next Steps:**  Suggested actions to optimize your network setup and enhance security.

## Network Configuration

This section presents the details of your current network configuration.

### VPCs

| VPC Name | Description | Auto-Create Subnets | Routing Mode | MTU | Firewall Policy |
|---|---|---|---|---|---|
| vpc-1 | Default VPC | True | REGIONAL | 1460 | deny-all-ingress | 
| vpc-2 | Production VPC | False | GLOBAL | 1460 | allow-internal-only | 
| ... | ... | ... | ... | ... | ... |

{vpc_config}

### Firewall Rules

| Firewall Rule Name | Direction | Action | Priority | Source | Destination | Protocols/Ports |
|---|---|---|---|---|---|---|
| allow-ssh | Ingress | Allow | 1000 | 0.0.0.0/0 | 10.10.10.0/24 | tcp:22 |
| deny-all-ingress | Ingress | Deny | 65534 | 0.0.0.0/0 | all | all |
| ... | ... | ... | ... | ... | ... | ... |

{firewall_rules_config}

### Subnets

| Subnet Name | VPC | Region | IP CIDR Range | Purpose |
|---|---|---|---|---|
| subnet-1 | vpc-1 | us-central1 | 10.10.10.0/24 | Application servers |
| subnet-2 | vpc-2 | europe-west1 | 192.168.1.0/24 | Database servers |
| ... | ... | ... | ... | ... |

{subnets_config}


### VPN Connectivity

| VPN Gateway | Region | Connected to | Description |
|---|---|---|---|
| vpn-gateway-1 | us-central1 | On-premises network | Site-to-site VPN |
| ... | ... | ... | ... |

{vpn_config}

## Best Practices

This section outlines Google Cloud's best practices for VPC and VPN configuration.

### VPC Best Practices

*   **Plan your network topology:** Design your VPC network with clear separation of resources and environments (e.g., development, test, production).
*   **Use custom mode VPCs:**  For greater control over IP address ranges and subnets.
*   **Optimize firewall rules:** Use the principle of least privilege, granting only necessary access.
*   **Use hierarchical firewall policies:** For centralized management and enforcement of firewall rules.
*   **Implement network security best practices:**  Such as DDoS protection, security scanning, and intrusion detection.

{vpc_best_practices}

### VPN Best Practices

*   **Secure your VPN connections:** Use strong encryption and authentication protocols.
*   **High availability:** Configure redundant VPN tunnels for failover.
*   **Monitor VPN performance:** Track throughput, latency, and connection stability.

{vpn_best_practices}

## Analysis

This section analyzes your current network configuration based on the best practices outlined above.

*   **VPC Analysis:**
    *   **VPC "vpc-1" uses auto-create subnets, which might not be ideal for granular control.** Consider switching to custom subnets for better management.
    *   **Firewall policy "deny-all-ingress" on "vpc-1" is a good security practice.** Ensure all necessary ingress rules are explicitly defined.
    *   **"vpc-2" has a global routing mode.** Evaluate if this is necessary or if regional routing would be more efficient.

*   **Firewall Rule Analysis:**
    *   **Firewall rule "allow-ssh" allows SSH access from any source (0.0.0.0/0).** Consider restricting the source IP ranges to only trusted sources.
    *   **Review all firewall rules to ensure they adhere to the principle of least privilege.**

*   **Subnet Analysis:**
    *   **Document the purpose of each subnet clearly.** This helps with network management and troubleshooting.
    *   **Consider using subnet aliases for internal DNS resolution.**

{vpc_action_items}


*   **VPN Analysis:**
    *   **Review the VPN configuration to ensure strong encryption and authentication are used.**
    *   **If critical, consider implementing redundant VPN tunnels for high availability.**
{vpn_action_items}

## Next Steps

Based on the analysis, the following next steps are recommended:

*   **Review and optimize VPC configurations:** Consider using custom mode VPCs and regional routing where appropriate.
*   **Refine firewall rules:** Restrict source IP ranges and ensure the principle of least privilege is followed.
*   **Document subnet purpose and consider using aliases.**
*   **Review and enhance VPN security and availability.**
*   **Regularly review and update your network configuration to align with Google Cloud's best practices and your evolving needs.**



"""


def generate_filename() -> str:
    timestr = time.strftime("%Y%m%d-%H%M%S")
    return f"final_report_{timestr}.md"


def markdown_to_pdf(markdown_file, pdf_file):
    """
    Converts a Markdown file to a PDF file.

    Args:
      markdown_file: Path to the Markdown file.
      pdf_file: Path to the output PDF file.
    """

    try:
        # Read the Markdown content
        with open(markdown_file, "r") as f:
            markdown_text = f.read()

        # Convert Markdown to HTML
        html = markdown(markdown_text)

        # Convert HTML to PDF using pdfkit
        pdfkit.from_string(html, pdf_file)

        print(f"Successfully converted {markdown_file} to {pdf_file}")

    except Exception as e:
        print(f"Error converting Markdown to PDF: {e}")


if __name__ == "__main__":
    markdown_file = "report.md"  # Replace with your Markdown file path
    pdf_file = "report.pdf"  # Replace with your desired PDF file path
    markdown_to_pdf(markdown_file, pdf_file)
