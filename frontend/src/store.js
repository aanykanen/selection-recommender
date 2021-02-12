import { createStore, combineReducers, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import { composeWithDevTools } from 'redux-devtools-extension'

import authorReducer from './reducers/authorReducer'
import genreReducer from './reducers/genreReducer'
import itemReducer from './reducers/itemReducer'
import publisherReducer from './reducers/publisherReducer'
import seriesReducer from './reducers/seriesReducer'
import subjectReducer from './reducers/subjectReducer'


const reducer = combineReducers({
  authors: authorReducer,
  genres: genreReducer,
  series: seriesReducer,
  subjects: subjectReducer,
  item: itemReducer,
  publishers: publisherReducer
})

const store = createStore(reducer,
  composeWithDevTools(
    applyMiddleware(thunk)
  )
)

export default store