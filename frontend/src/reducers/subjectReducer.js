import subjectService from '../services/subjects'

const subjectReducer = (state = [], action) => {
  switch (action.type) {
  case 'INIT_SUBJECTS':
    return action.data
  default:
    return state
  }
}

export const initSubjects = () => {
  return async dispatch => {
    try {
      const subjects = await subjectService.getAll()

      dispatch({
        type: 'INIT_SUBJECTS',
        data: subjects
      })
    } catch (err) {
      dispatch({
        type: 'INIT_SUBJECTS',
        data: []
      })
    }
  }
}

export default subjectReducer