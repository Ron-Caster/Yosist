# Application Launcher Chatbot (As of Now)

The Application Launcher Chatbot is a Python script that allows users to interact with a chatbot to open various applications based on their prompts. The chatbot utilizes the Groq API client to generate responses and facilitate the opening of specified applications.

## Project Overview

The chatbot provides a conversational interface where users can input the name of an application they want to open, and the chatbot will attempt to launch the specified application. The script includes a predefined mapping of application names to their respective executable paths for seamless application launching.

## Features

- User-friendly chatbot interface for opening applications
- Integration with the Groq API for natural language processing
- Customizable application mapping for easy addition of new applications
- Error handling for unsupported applications or launch failures

## Getting Started

To get started with the Application Launcher Chatbot, ensure you have Python 3.x installed along with the necessary dependencies. Update the `app_map` dictionary in the script with the paths to the applications you wish to be able to open. Run the script and start interacting with the chatbot by providing the name of the application you want to open.

## Dependencies

- Python 3.x
- Groq API client library
- Required applications installed on the system

## Usage

1. Run the script and follow the prompts to interact with the chatbot.
2. Input the name of the application you want to open when prompted.
3. The chatbot will make an attempt to open the specified application based on the provided name.

## Contributing

Contributions to the Application Launcher Chatbot project are welcome. Feel free to fork the repository, make improvements, and submit a pull request with your changes.

## License

This project is licensed under the [MIT License](LICENSE).