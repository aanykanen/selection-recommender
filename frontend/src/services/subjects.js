import axios from 'axios'
const baseUrl = 'http://localhost:5000/api'

const getAll = async () => {
  const response = await axios.get(`${baseUrl}/subjects/`)
  return response.data
}

const getOne = async id => {
  const response = await axios.get(`${baseUrl}/subjects/${id}`)
  return response.data
}

export default { getAll, getOne }