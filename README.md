# ExtractDataV0

The application described in the provided code is a FastAPI-based system that allows users to upload PDF files, extract tabular data from those PDF files, and return the extracted data in JSON format.

Here is a summary of the main features and functionalities of the application:

HTML Home Page: The application has an HTML home page accessible at the root ("/") route. This page displays a form that allows users to upload PDF files.

PDF File Upload: Users can select and upload PDF files through the form on the home page. The application verifies that the uploaded file is a PDF before processing it.

PDF Processing: Once a PDF file is uploaded, the application saves the file to the system and uses the "tabula" library to extract tabular data from the PDF. The extracted tables are converted into JSON format.

Rounding of Values: The application includes a function to round floating-point values in the resulting JSON to two decimal places. This is done to properly format the data.

Dockerization: The application is designed to run in a Docker container. A Dockerfile is provided to set up the runtime environment and necessary dependencies. A docker-compose.yml file is also provided to simplify the building and running of the container.

In summary, the application allows users to upload PDF files, process them to extract tabular data, and return the extracted data in JSON format. This application could be useful in scenarios where automated extraction of tabular data from PDF documents, such as invoices or reports, is required.
