import React, { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'

import Container from '@material-ui/core/Container'

import ActionSelect from './ActionSelect'
import ItemForm from './ItemForm'
import ItemDashboard from './ItemDashboard'
import RecommenderDashboard from './RecommenderDashboard'
import RecommenderForm from './RecommenderForm'

import { initAuthors } from '../reducers/authorReducer'
import { initGenres } from '../reducers/genreReducer'
import { initSeries } from '../reducers/seriesReducer'
import { initSubjects } from '../reducers/subjectReducer'
import { initPublishers } from '../reducers/publisherReducer'
import { resetItem } from '../reducers/itemReducer'

const App = (props) => {
  const dispatch = useDispatch()
  const item = useSelector(state => state.item)

  useEffect(() => {
    dispatch(initAuthors())
    dispatch(initGenres())
    dispatch(initPublishers())
    dispatch(initSeries())
    dispatch(initSubjects())
    dispatch(resetItem())
  }, [dispatch])

  const recommenderModule = () => {
    if (item === null) {
      return (
        <React.Fragment>
          <RecommenderForm />
        </React.Fragment>
      )
    } else {
      return(
        <React.Fragment>
          <RecommenderDashboard />
        </React.Fragment>
      )
    }
  }

  const itemStatModule = () => {
    if (item === null) {
      return(
        <React.Fragment>
          <ItemForm />
        </React.Fragment>
      )
    } else {
      return (
        <React.Fragment>
          <ItemDashboard />
        </React.Fragment>
      )
    }
  }

  const recommenderTypeSelect = () => {
    return (
      <React.Fragment>
        <ActionSelect />
      </React.Fragment>
    )
  }

  return (
    <Container className='app'>
      <Router>
        <Switch>
          <Route path='/selection' render={() =>
            recommenderModule()
          } />
          <Route path='/itemstat' render={() =>
            itemStatModule()
          } />
          <Route path='/' render={() =>
            recommenderTypeSelect()
          } />
        </Switch>
      </Router>
    </Container>
  )
}

export default App
