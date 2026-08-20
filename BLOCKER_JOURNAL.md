\# BLOCKER JOURNAL — The Meridian Pivot



\## Day 1–2: GraphQL Mini-Prototype



\### Blocker 1 — Flask-GraphQL Dependency Error



\*\*Date:\*\* 18 August 2026



\#### Exact Error



When I initially tried to run the Flask GraphQL application, the application failed during startup with the following error:



```text

ImportError: cannot import name 'get\_default\_backend' from 'graphql'

The error occurred while Flask-GraphQL was importing its GraphQL backend dependencies.



What I Tried

I initially installed the required packages globally using pip:

Flask

Flask-GraphQL

Graphene

Requests

The application still failed because the installed GraphQL-related packages were not compatible with the version expected by Flask-GraphQL.

I created a project-specific Python virtual environment using:

python -m venv .venv

I activated the virtual environment:

.\\.venv\\Scripts\\Activate.ps1

I verified that the virtual environment was being used with:

python --version

where.exe python

I installed compatible package versions inside the virtual environment.

What Fixed It



The problem was fixed by isolating the project dependencies inside the .venv virtual environment and using compatible versions of the GraphQL packages.



The working versions were:



Flask==2.3.3

Flask-GraphQL==2.0.1

graphene==2.1.9

requests==2.34.2



I then verified that the required packages could be imported successfully with:



python -c "import flask; import graphene; import requests; import flask\_graphql; print('ALL IMPORTS SUCCESSFUL')"



The result was:



ALL IMPORTS SUCCESSFUL



After fixing the environment, the Flask application started successfully and became available at:



http://localhost:5000/graphql

Time to Resolution



Approximately: \[ENTER YOUR ACTUAL TIME]



Key Concepts Learned

Python virtual environments isolate project dependencies from the global Python installation.

Installing packages successfully does not always mean that their versions are compatible with each other.

Using python -m pip helps ensure that packages are installed into the Python environment currently being used.

Flask-GraphQL depends on compatible versions of the underlying GraphQL packages.

Dependency management is an important part of building and maintaining a Python application.

Day 1–2: GraphQL Implementation

Progress



After resolving the environment issue, I implemented and tested the GraphQL mini-prototype.



The prototype contains:



A hardcoded warehouse stock data source.

A Product GraphQL type.

Product fields including SKU, product name, stock count, warehouse location, last updated time, and stock status.

A resolver for determining whether a product is in stock.

A product query for retrieving a product by SKU.

An allProducts query for retrieving all products.

An outOfStock query for retrieving products with zero stock.

A Flask /graphql endpoint using GraphiQL.

GraphQL Testing



I successfully tested the required GraphQL queries:



Product lookup by SKU.

Out-of-stock product query.

All-products query.



The queries returned the expected data successfully.



The GraphQL endpoint was tested through:



http://localhost:5000/graphql

Key GraphQL Concepts Learned



The Day 1–2 prototype helped me understand the relationship between:



Schema → Query → Resolver → Data → GraphQL Response



I learned that:



The schema defines the structure and types of data available through GraphQL.

A query specifies the data requested by the client.

A resolver contains the logic used to obtain the requested data.

GraphQL allows the client to request only the fields it needs.

GraphQL provides a typed interface between the client and the underlying data source.

Time Log

Activity	Time Spent

Environment setup	\[ENTER TIME]

Dependency troubleshooting	\[ENTER TIME]

GraphQL schema implementation	\[ENTER TIME]

Resolver implementation	\[ENTER TIME]

GraphQL query testing	\[ENTER TIME]

Blocker documentation	\[ENTER TIME]

Total	\[ENTER TOTAL]

Self-Assessment

Day 1–2 Status: Completed



I successfully completed the Day 1–2 GraphQL mini-prototype.



The main blocker was a dependency compatibility issue between Flask-GraphQL and the installed GraphQL packages. I resolved the issue by creating an isolated virtual environment and installing compatible dependency versions.



I can now explain the basic GraphQL concepts of:



Schema

Query

Resolver

GraphQL type

Field selection

Flask GraphQL endpoint



The prototype is running successfully and all required Day 1–2 queries have been tested.



What I Need to Improve



I need to become more comfortable with Python dependency management and understanding how packages depend on specific versions of other packages.



I also want to improve my ability to diagnose dependency errors independently rather than relying on trial and error.

