from setuptools import setup, find_packages

setup(
    name="versa_core",
    version="1.0.0",
    description="Versa ERP Core Platform: Governance, Multi-Level Approvals, Credit Policies & Tenant Isolation",
    author="Versa ERP Platform Team",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=["frappe", "erpnext"],
)
