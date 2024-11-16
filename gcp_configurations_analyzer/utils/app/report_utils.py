import time

from aiohttp.web_routedef import static
from markdown import markdown
import pdfkit
class ReportUtils:
    @staticmethod
    def get_report_template() -> str:
        return \
"""
        
# Google Cloud Network Configuration Analysis Report

## Introduction

This report provides a comprehensive analysis of your Google Cloud network configuration, focusing on Virtual Private Clouds (VPCs), firewall rules, subnets, and VPN connectivity. It aims to identify potential areas for improvement by comparing your current setup against Google Cloud's best practices.

The report is structured as follows:

- **Network Configuration:**  Details of your existing VPCs, firewall rules, subnets, and VPN connections.
- **Best Practices:**  A summary of Google Cloud's recommended best practices for VPC and VPN configuration.
- **Analysis:**  Evaluation of your current configuration in light of the best practices.

## Network Configuration

This section presents the details of your current network configuration.

### VPCs
      
```

{vpc_config}

```

### Firewall Rules
     
```

{firewall_rules_config}

```

### Subnets



```

{subnets_config}

```


### VPN Connectivity



```

{vpn_config}

```

## Best Practices

This section outlines Google Cloud's best practices for VPC and VPN configuration.

### VPC Best Practices

{vpc_best_practices}

### VPN Best Practices

{vpn_best_practices}

## Analysis

This section analyzes your current network configuration based on the best practices outlined above.

### VPC Analysis

{vpc_action_items}


### VPN Analysis:
**Review the VPN configuration to ensure strong encryption and authentication are used.**
**If critical, consider implementing redundant VPN tunnels for high availability.**


{vpn_action_items}



"""
    @staticmethod
    def generate_filename() -> str:
        timestr = time.strftime("%Y%m%d-%H%M%S")
        return f"final_report_{timestr}.md"
    @staticmethod
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
# if __name__ == "__main__":
#     markdown_file = "report.md"  # Replace with your Markdown file path
#     pdf_file = "report.pdf"  # Replace with your desired PDF file path
#     markdown_to_pdf(markdown_file, pdf_file)