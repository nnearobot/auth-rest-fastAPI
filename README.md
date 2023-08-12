# Video Storage API

This is a simple video storage API that implements a functions listed below:

1. List all the files
2. Upload a video file
3. Download a video file by providing its fileId
3. Delete a file by providing its fileId


## Production server building

To quick launch the production version we use the Docker container on a **python3.11** image. The API production server listens to a 8080 port.


### The very first launch

For building an image at the first time:

```
make build
```


### To stop the server

```
make stop
```


### To start server again

```
make start
```

## Testing endpoints

FastAPI automatically generates API documentation that is interactive, making it easy to test an API directly from the documentation page: [http://localhost:8080/docs](http://localhost:8080/docs).



## Versioning

Sometimes we need to change a functionality, so the prevoius functionally is totally breaks. We must to provide a reliable and efficient service for users. That is why we always should be sure that our API is up-to-date and bug-free. This is why we use versioning in our API.


### Why Versioning is Important

1. **Backwards Compatibility**: By versioning our API, we are able to ensure that previous versions of the API will continue to work as expected. This means that if a user is using an older version of the API (i.e. an older version ov CLI application), they will not be affected by any changes made to the newer versions.

2. **Testing**: Versioning allows us to test new features and changes in a controlled environment before releasing them to the public. This means that we can ensure that the new version of the API is stable and reliable before making it available to our users.

### How to implement versioning in this API

One way to achieve this is by creating a new router.py and schemas.py files. For example, if we are creating version 2 of the API, we should create a new files router_v2.py and schemas_v2.py within the *app/files* directory. Additionally we should add some directives to ./main.py file.

This allows us to keep the new version separate from the previous version, making it easy to maintain and test.


## About this API

### Why Python?

According to [StackOverflow analysis](https://survey.stackoverflow.co/2022/#technology-most-popular-technologies), Python is one of the fastest-growing programming languages nowadays. More and more libraries are being developed for a wide variety of needs. This makes Python a great tool for solving a wide range kinds of problems.

### Why FastAPI?

FastAPI is a modern, fast, and easy-to-use web framework for building APIs with Python. It is gaining popularity in the Python community due to its performance, simplicity, and developer-friendly approach.

**Fast Performance**

FastAPI is built on top of the Starlette web framework and uses Pydantic for request and response data validation. This combination makes it incredibly fast and efficient. According to benchmarks, FastAPI can handle more than 50,000 requests per second, which is faster than most Python web frameworks.

**Easy to Learn and Use**

FastAPI has a very intuitive and easy-to-use API, making it easy for developers to get started quickly. It comes with a comprehensive and well-documented user guide that covers all the essential features of the framework. Additionally, it uses type hints to ensure that your code is easy to read and understand.

**Automatic API Documentation**

FastAPI automatically generates API documentation based on your code's type hints and function signatures. This feature makes it easy to understand how your API works, what parameters it accepts, and what responses it returns. The generated documentation is interactive, making it easy to test your API directly from the documentation page.

**Robust Features**

FastAPI comes with many useful features out-of-the-box, such as data validation, request parsing, response serialization, and more. It also supports WebSocket APIs, background tasks, and file uploads, making it a versatile framework for building APIs.

**Scalable Architecture**

FastAPI uses ASGI, a standard for asynchronous web servers and applications, making it highly scalable. It can handle multiple requests concurrently, making it an ideal choice for building high-performance APIs that can handle large traffic volumes.


## What may be improved

When we upload a file, its checksum is stored in a database. We can use it to check if the file is corrupted or not before downloading. 


## Developing mode

For developing purpose we should run `pipenv install` for dependency managing.
Then from the application root directory run:
```
./bootstrap.sh
```
Developing server works on 8000 port: [http://localhost:8000/docs](http://localhost:8000/docs)


## Testing

There are unit tests within the directory **tests**, which testing endpoints.
For testing run from a project root:

```
pytest -v tests/
```
