import axios from 'axios'
const baseUrl = 'http://localhost:5000/api'

const getRecommendation = async (item, type) => {
  let request = baseUrl
  if(type==='selection') {
    request += '/recommendation/selection?'
  }

  if(item.author) {
    if(typeof item.author === 'string') {
      request += `author=${item.author.replace(/\s/g, '-')}&`
    } else {
      request += `author=${item.author}&`
    }

  }

  if(item.publisher) {
    if(typeof item.publisher === 'string') {
      request += `publisher=${item.publisher.replace(/\s/g, '-')}&`
    } else {
      request += `publisher=${item.publisher}&`
    }

  }

  if(item.series) {
    if(typeof item.series === 'string') {
      request += `series=${item.series.replace(/\s/g, '-')}&`
    } else {
      request += `series=${item.series}&`
    }

  }

  if(item.genres && item.genres.length > 0) {
    request += `genres=${item.genres.map(g => {
      if(typeof g === 'string') {
        return g.replace(/\s/g, '-')
      } else {
        return g
      }
    }).join('+')}&`
  }

  if(item.subjects && item.subjects.length > 0) {
    request += `subjects=${item.subjects.map(s => {
      if(typeof s === 'string') {
        return s.replace(/\s/g, '-')
      } else {
        return s
      }

    }).join('+')}`
  }

  const response = await axios.get(request)
  return response.data
}

export default { getRecommendation }