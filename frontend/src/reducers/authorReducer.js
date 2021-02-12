import authorService from '../services/authors'

const authorReducer = (state = [], action) => {
  switch (action.type) {
  case 'INIT_AUTHORS':
    return action.data
  default:
    return state
  }
}

export const initAuthors = () => {
  return async dispatch => {

    try {
      const authors = await authorService.getAll()

      dispatch({
        type: 'INIT_AUTHORS',
        data: authors
      })
    } catch (err) {
      dispatch({
        type: 'INIT_AUTHORS',
        data: []
      })
    }
  }
}

export default authorReducer