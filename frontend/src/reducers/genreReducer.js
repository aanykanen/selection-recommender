import genreService from '../services/genres'

const genreReducer = (state = [], action) => {
  switch (action.type) {
  case 'INIT_GENRES':
    return action.data
  default:
    return state
  }
}

export const initGenres = () => {
  return async dispatch => {
    try {
      const genres = await genreService.getAll()

      dispatch({
        type: 'INIT_GENRES',
        data: genres
      })
    } catch (err) {
      dispatch({
        type: 'INIT_GENRES',
        data: []
      })
    }
  }
}

export default genreReducer