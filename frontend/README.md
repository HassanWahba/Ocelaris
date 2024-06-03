# OCEL2.0 Extractor Frontend

## Project Structure
The project is structured as follows:
```
OCEL2.0ExtractorFrontend
├───public
└───src
    ├───api
    ├───assets
    │   └───css
    ├───components
    │   ├───DBConnection
    │   ├───Extractor
    │   │   ├───ChangeLogs
    │   │   └───Meta
    │   ├───Loader
    │   ├───SharedComponents
    │   │   ├───Diagram
    │   │   │   └───Modals
    │   │   └───Tables
    │   └───Transformer
    │       ├───Events
    │       ├───Objects
    │       └───Processes
    ├───store
    │   └───modules
    └───views
```

Each directory has a specific purpose:

- `public/`: Contains the public assets of the application, including the main HTML file.
- `src/`: Contains the source code of the application.
  - `api/`: Contains the API calls.
  - `assets/css/`: Contains the CSS files.
  - `components/`: Contains the Vue components used in the application.
  - `store/`: Contains the Vuex store modules.
  - `views/`: Contains the Vue components that represent entire views or pages in the application.m

## Source Code

The source code in the src/ directory is organized into several components and utilities. Some of the key files include:

- src/app.js: This is the main JavaScript file that initializes the Vue application and registers global components.
- src/components/Loader/IOHandler.vue: This Vue component handles file input and output operations.
- src/components/Transformer/Processes/EditProcess.vue: This Vue component provides an interface for editing processes.

## Building and Running the Project

### Install Dependencies

```
npm i
```

### HotReload with own WebServer

```
npm run serve
```

### Build & Bundle Frontend

```
npm run build
```

## License
The project is licensed under the MIT License. For more details, see the LICENSE file.

## Author
This project was created by Hassan Wahba. For more information, please contact the author.
