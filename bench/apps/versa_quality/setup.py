from setuptools import setup, find_packages

setup(
    name="versa_quality",
    version="0.1.0",
    description="Versa ERP Quality: Multi-Tier Textile QA/QC, Versioned Specifications, Multi-Point Measurements & Quality Gates",
    author="Versa ERP Platform Team",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=["frappe", "erpnext", "versa_core"],
)
