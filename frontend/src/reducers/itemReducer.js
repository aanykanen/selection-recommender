const itemReducer = (state = null, action) => {
  switch (action.type) {
  case 'RESET_ITEM':
    return null
  case 'UPDATE_ITEM':
    return action.data
  default:
    return state
  }
}

export const updateItem = (item) => {
  return dispatch => {
    dispatch({
      type: 'UPDATE_ITEM',
      data: item
    })
  }
}

export const resetItem = () => {
  return dispatch => {
    dispatch({
      type: 'RESET_ITEM'
    })
  }
}

export default itemReducer