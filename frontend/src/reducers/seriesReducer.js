import seriesService from '../services/series'

const seriesReducer = (state = [], action) => {
  switch (action.type) {
  case 'INIT_SERIES':
    return action.data
  default:
    return state
  }
}

export const initSeries = () => {
  return async dispatch => {
    try {
      const series = await seriesService.getAll()

      dispatch({
        type: 'INIT_SERIES',
        data: series
      })
    } catch (err) {
      dispatch({
        type: 'INIT_SERIES',
        data: []
      })
    }
  }
}

export default seriesReducer