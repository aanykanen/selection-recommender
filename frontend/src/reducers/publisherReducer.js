import publisherService from '../services/publishers'

const publisherReducer = (state = [], action) => {
  switch (action.type) {
  case 'INIT_PUBLISHERS':
    return action.data
  default:
    return state
  }
}

export const initPublishers = () => {
  return async dispatch => {
    try {
      const subjects = await publisherService.getAll()

      dispatch({
        type: 'INIT_PUBLISHERS',
        data: subjects
      })
    } catch (err) {
      dispatch({
        type: 'INIT_PUBLISHERS',
        data: []
      })
    }
  }
}

export default publisherReducer