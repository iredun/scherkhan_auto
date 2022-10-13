import setuptools

prod_dependencies = ["pydantic", "requests", "websocket-client", "rel"]
test_dependencies = ["pytest", "pytest-env", "pytest-cov", "requests-mock"]
lint_dependencies = ["flake8", "flake8-docstrings", "black", "isort"]
docs_dependencies = []
dev_dependencies = (
    test_dependencies + lint_dependencies + docs_dependencies + prod_dependencies
)
deploy_dependencies = []


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scherkhan_auto",
    author="Ivan Redun",
    author_email="redunivan@yandex.ru",
    description="Scher-Khan Auto API client",
    keywords="scherkhan, api client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iredun/scherkhan_auto",
    project_urls={
        "Documentation": "https://github.com/iredun/scherkhan_auto",
        "Bug Reports": "https://github.com/iredun/scherkhan_auto/issues",
        "Source Code": "https://github.com/iredun/scherkhan_auto",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=prod_dependencies,
    extras_require={
        "production": prod_dependencies,
        "test": test_dependencies,
        "lint": lint_dependencies,
        "docs": dev_dependencies,
        "dev": dev_dependencies,
        "deploy": deploy_dependencies,
    },
    include_package_data=True,
    zip_safe=False,
)
