import axios from 'axios'
const baseUrl = 'http://localhost:5000/api/items'

const getOne = async id => {
  try {
    const response = await axios.get(`${baseUrl}/${id}`)
    return response.data
  } catch(e) {
    return e.response
  }
}

export default { getOne }