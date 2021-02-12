import React, { useState } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { Link } from 'react-router-dom'

import { Autocomplete, createFilterOptions } from '@material-ui/lab'
import { makeStyles } from '@material-ui/core/styles'
import Button from '@material-ui/core/Button'
import Grid from '@material-ui/core/Grid'
import TextField from '@material-ui/core/TextField'
import Typography from '@material-ui/core/Typography'

import { updateItem } from '../reducers/itemReducer'
import annifService from '../services/annif'

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%',
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}))

const defaultFilterOptions = createFilterOptions()
const filterOptions = (options, state) => defaultFilterOptions(options, state).slice(0, 100)

const RecommenderForm = () => {
  const dispatch = useDispatch()

  const [itemAuthor, setItemAuthor] = useState(null)
  const [itemSeries, setItemSeries] = useState(null)
  const [itemPublisher, setItemPublisher] = useState(null)
  const [itemGenres, setItemGenres] = useState(null)
  const [itemSubjects, setItemSubjects] = useState(null)
  const [itemDescription, setItemDescription] = useState(null)

  const authors = useSelector(state => state.authors)
  const genres = useSelector(state => state.genres)
  const publishers = useSelector(state => state.publishers)
  const series = useSelector(state => state.series)
  const subjects = useSelector(state => state.subjects)

  const classes = useStyles()

  const handleForm = async (event) => {
    event.preventDefault()
    const extendedSubjects = itemSubjects ? [...itemSubjects] : []

    if(itemDescription) {
      try {
        const suggestions = await annifService.getSuggestions(itemDescription)

        if(suggestions.results) {
          suggestions.results.forEach(r => {
            if(r.score >= 0.01) {
              const subject = r.label.toLowerCase()
              const newSubject = subjects.find(x => x.label === subject)
              if(newSubject) {
                extendedSubjects.push(newSubject.id)
              } else {
                extendedSubjects.push(subject)
              }
            }
          })
        }
      } catch (err) {
        console.log('Annif did not respond')
      }
    }

    const recommendSearchItem = {
      author: itemAuthor,
      series: itemSeries,
      publisher: itemPublisher,
      genres: itemGenres,
      subjects: [...new Set(extendedSubjects)]
    }
    dispatch(updateItem(recommendSearchItem))
  }

  const handleFieldChange = (v, type) => {
    if(type === 'author') {
      const a = authors.find(x => x.name === v)
      if(a) {
        setItemAuthor(a.id)
      } else {
        setItemAuthor(v)
      }

    } else if(type === 'publisher') {
      const p = publishers.find(x => x.name === v)
      if(p) {
        setItemPublisher(p.id)
      } else {
        setItemPublisher(v)
      }

    } else if(type === 'series') {
      const s = series.find(x => x.label === v)
      if(s) {
        setItemSeries(s.id)
      } else {
        setItemSeries(v)
      }

    } else if(type === 'genre') {
      const newGenres = []

      v.forEach(g => {
        const newGenre = genres.find(x => x.label === g)
        if(newGenre) {
          newGenres.push(newGenre.id)
        } else {
          newGenres.push(g)
        }

      })

      setItemGenres(newGenres)
    } else if(type === 'subject') {
      const newSubjects = []

      v.forEach(s => {
        const newSubject = subjects.find(x => x.label === s)
        if(newSubject) {
          newSubjects.push(newSubject.id)
        } else {
          newSubjects.push(s)
        }
      })

      setItemSubjects(newSubjects)
    }
  }

  return (
    <React.Fragment>
      <div style={{ paddingTop: '10vh' }}>
        <Typography align='center' color='primary' variant='h3'>
        Book information
        </Typography>
      </div>

      <div className="BookForm">
        <form className={classes.form} onSubmit={handleForm}>
          <Autocomplete
            freeSolo
            autoSelect
            onChange={(e, v) => handleFieldChange(v, 'author')}
            filterOptions={filterOptions}
            noOptionsText='Author unknown'
            options={authors.map(a => a.name)}
            renderInput={(params) =>
              <TextField
                {...params}
                variant="outlined"
                margin="normal"
                fullWidth
                id="author"
                label="Author"
                name="author"
                autoFocus
              />
            } />

          <Autocomplete
            freeSolo
            autoSelect
            onChange={(e, v) => handleFieldChange(v, 'publisher')}
            filterOptions={filterOptions}
            noOptionsText='Publisher unknown'
            options={publishers.map(p => p.name)}
            renderInput={(params) =>
              <TextField
                {...params}
                variant="outlined"
                margin="normal"
                fullWidth
                id="publisher"
                label="Publisher"
                name="publisher"
              />
            } />

          <Autocomplete
            freeSolo
            autoSelect
            onChange={(e, v) => handleFieldChange(v, 'series')}
            filterOptions={filterOptions}
            noOptionsText='Series unknown'
            options={series.map(s => s.label)}
            renderInput={(params) =>
              <TextField
                {...params}
                variant="outlined"
                margin="normal"
                fullWidth
                label="Series"
                name="series"
              />
            } />

          <Autocomplete
            freeSolo
            autoSelect
            onChange={(e, v) => handleFieldChange(v, 'genre')}
            multiple
            filterOptions={filterOptions}
            noOptionsText='Genre unknown'
            options={genres.map(g => g.label)}
            renderInput={(params) =>
              <TextField
                {...params}
                variant="outlined"
                margin="normal"
                fullWidth
                id="genres"
                label="Genres"
                name="genres"
              />
            } />

          <Autocomplete
            freeSolo
            autoSelect
            onChange={(e, v) => handleFieldChange(v, 'subject')}
            multiple
            filterOptions={filterOptions}
            noOptionsText='Subject unknown'
            options={subjects.map(s => s.label)}
            renderInput={(params) =>
              <TextField
                {...params}
                variant="outlined"
                margin="normal"
                fullWidth
                id="subjects"
                label="Subjects"
                name="subjects"
              />
            } />

          <TextField
            onChange={(e) => setItemDescription(e.target.value)}
            variant="outlined"
            margin="normal"
            fullWidth
            id="description"
            label="Description"
            name="description"
            multiline
            rows={4}
            rowsMax={20}
          />
          <Grid container spacing={3} alignItems="center" justify="center">
            <Grid item xs={8} sm={8} md={4} lg={4}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                className={classes.submit}
                fullWidth
              >
                Recommend
              </Button>
            </Grid>
            <Grid item xs={8} sm={8} md={4} lg={4}>
              <Button
                variant="contained"
                color="primary"
                className={classes.submit}
                fullWidth
                component={Link}
                to='/'
              >
                Go back
              </Button>
            </Grid>
          </Grid>

        </form>
      </div>
    </React.Fragment>
  )
}

export default RecommenderForm
