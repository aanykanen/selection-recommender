# Frontend
The frontend has been constructed using React and Material-UI. By default the API connections are made to localhost:5000 which also is where the development API runs by default. The connection to Annif is left on by default and it uses the Finnish ontology. If the language of the metadata in your library is either Swedish or English you're in luck as Annif does also support these languages. Make sure you switch to using the proper language by altering the config. You may also just delete/disable the description field from the RecommenderForm component if you don't wish to use Annif or Annif does not support your language.

Regarding the install there isn't much more to do than run npm install and npm start after building the backend service. The PixelOperatorMono-Bold font is not included to the repository and must be downloaded separately and placed to src/fonts/ folder.

## Frontend dependencies

- Name: @material-ui/core
    - License: <a href="https://github.com/mui-org/material-ui/blob/next/LICENSE">MIT license</a>

- Name: @material-ui/icons
    - License: <a href="https://github.com/mui-org/material-ui/blob/next/LICENSE">MIT license</a>

- Name: @material-ui/lab
    - License: <a href="https://github.com/mui-org/material-ui/blob/next/LICENSE">MIT license</a>

- Name: @nivo/bar
    - License: <a href="https://github.com/plouc/nivo/blob/master/LICENSE.md">MIT license</a>

- Name: @nivo/line
    - License: <a href="https://github.com/plouc/nivo/blob/master/LICENSE.md">MIT license</a>

- Name: @testing-library/jest-dom
    - License: <a href="https://github.com/testing-library/jest-dom/blob/main/LICENSE">MIT license</a>

- Name: @testing-library/react
    - License: <a href="https://github.com/testing-library/react-testing-library/blob/master/LICENSE">MIT license</a>

- Name: @testing-library/user-event
    - License: <a href="https://github.com/testing-library/user-event/blob/master/LICENSE">MIT license</a>

- Name: axios
    - License: <a href="https://github.com/axios/axios/blob/master/LICENSE">MIT license</a>

- Name: querystring
    - License: <a href="https://github.com/Gozala/querystring/blob/master/LICENSE">MIT license</a>

- Name: react
    - License: <a href="https://github.com/facebook/react/blob/master/LICENSE">MIT license</a>

- Name: react-dom
    - License: <a href="https://github.com/facebook/react/blob/master/LICENSE">MIT license</a>

- Name: react-promise-tracker
    - License: <a href="https://github.com/Lemoncode/react-promise-tracker/blob/master/LICENSE">MIT license</a>

- Name: react-redux
    - License: <a href="https://github.com/reduxjs/react-redux/blob/master/LICENSE.md">MIT license</a>

- Name: react-router-dom
    - License: <a href="https://github.com/ReactTraining/react-router/blob/master/LICENSE">MIT license</a>

- Name: react-scripts
    - License: <a href="https://github.com/facebook/create-react-app/blob/master/LICENSE">MIT license</a>

- Name: react-spinners
    - License: <a href="https://github.com/davidhu2000/react-spinners/blob/master/LICENSE">MIT license</a>

- Name: redux
    - License: <a href="https://github.com/reduxjs/redux/blob/master/LICENSE.md">MIT license</a>

- Name: redux-thunk
    - License: <a href="https://github.com/reduxjs/redux-thunk/blob/master/LICENSE.md">MIT license</a>


### Devdependencies

- Name: @svgr/cli
    - License: <a href="https://github.com/gregberge/svgr/blob/main/packages/cli/README.md">MIT license</a>

- Name: redux-devtools-extension
    - License: <a href="https://github.com/zalmoxisus/redux-devtools-extension/blob/master/LICENSE">MIT license</a>

## Known issues
- NiVo figures act slowly if you change between mobile view/desktop view in developer mode
- Tested only with Firefox 81.0 / Ubuntu. I've no idea what breaks with other browsers but I'm sure something will.
