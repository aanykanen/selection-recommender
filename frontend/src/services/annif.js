import axios from 'axios'
import qs from 'querystring'

const apiUrl = 'https://api.annif.org/v1/projects/yso-fi/suggest'

const getSuggestions = async text => {
  const response = await axios.post(apiUrl, qs.stringify({ text }))
  return response.data
}

export default { getSuggestions }