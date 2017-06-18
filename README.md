# SoManyDevices

## Optimizer

To install:

 * From the repository root:
    * Navigate to subfolder `simple-websocket-server`
    * Run `sudo python setup.py install`
    * Navigate to subfolder `optimization`
    * Run `python run_server.py`

## Webstrates

[Webstrates](https://github.com/Webstrates/Webstrates) is a research prototype enabling collaborative editing of websites through DOM manipulations realized by [Operational Transformation](http://en.wikipedia.org/wiki/Operational_transformation) using [ShareDB](https://github.com/share/sharedb). Webstrates observes changes to the DOM using [MutationObservers](https://developer.mozilla.org/en/docs/Web/API/MutationObserver).

Webstrates itself is a webserver and transparent web client that persists and synchronizes any changes done to the Document Object Model (DOM) of any page served between clients of the same page, including changes to inlined JavaScript or CSS. By using [transclusions](https://en.wikipedia.org/wiki/Transclusion) through iframes, we achieve an application-to-document-like relationship between two webstrates. With examples built upon Webstrates, we have demonstrated how transclusion combined with the use of CSS injection and the principles of [instrumental interaction](https://www.lri.fr/~mbl/INSTR/eintroduction.html) can allow multiple users to collaborate on the same webstrate through highly personalized and extensible editors. You can find the academic paper and videos of Webstrates in action at [webstrates.net](http://www.webstrates.net).

### Installation

Requirements:

 * [MongoDB](http://www.mongodb.org)
    * Install and run MongoDB
 * [NodeJS](http://nodejs.org)
    * Install node >= 6.2.0 (version 6.2.0 is recommended)

To install:

 * Clone this repository.
 * From the repository root:
    * Navigate to Webstrates folder `cd ./Webstrates`
    * Copy `config-sample.json` to `config.json` and modify it.
    * Run `npm install`.
    * Run `npm run build-babel`.
    * Run `npm start`.
    * Navigate to `http://localhost:7007/` in your browser and start using Webstrates!
    * When requested use `web` as username and `strate` as password 

To set up webstrate documents:

 * For each file in folder `ui` navigate to `http://localhost:7007/<filename>` with your browser
 * Copy file contents, open browser developer tools, and replace DOM content with the content of the file
 * To run demo navigate to `http://localhost:7007/adaptive-ui-manager/` and `http://localhost:7007/adaptive-ui-viewer/`
