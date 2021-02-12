import React, { useState } from 'react'
import { useDispatch } from 'react-redux'
import { Link } from 'react-router-dom'

import { makeStyles } from '@material-ui/core/styles'
import Button from '@material-ui/core/Button'
import Grid from '@material-ui/core/Grid'
import TextField from '@material-ui/core/TextField'
import Typography from '@material-ui/core/Typography'

import { updateItem } from '../reducers/itemReducer'
import itemService from '../services/items'

const useStyles = makeStyles((theme) => ({
  form: {
    width: '100%',
    marginTop: theme.spacing(1),
  },
  inputHeaderDiv: {
    paddingTop: '25vh'
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  }
}))

const ItemForm = () => {
  const dispatch = useDispatch()
  const classes = useStyles()

  const [itemId, setItemId] = useState('')
  const [errorText, setErrorText] = useState('')

  const handleForm = async (event) => {
    event.preventDefault()

    if(itemId === '') {
      setErrorText('Please input item id to continue')
    } else if(isNaN(itemId)) {
      setErrorText('Item id must be a number')
    } else {
      try {
        const res = await itemService.getOne(itemId)
        if(res.status) {
          setErrorText('Item id does not exist')
        } else {
          setErrorText('')
          dispatch(updateItem(res))
        }
      } catch (e) {
        setErrorText('There was a major error. Please contact system administrator.')
      }
    }

  }

  const header = (title) => {
    return (
      <React.Fragment>
        <Typography align='center' color='primary' variant='h3'>
          {title}
        </Typography>
      </React.Fragment>
    )
  }

  const idForm = () => {
    return (
      <React.Fragment>
        <form className={classes.form} onSubmit={handleForm}>
          <Grid container spacing={3} alignItems="center" justify="center">

            <Grid item xs={12} sm={12} md={12} lg={12}>
              <TextField
                onChange={(e) => setItemId(e.target.value)}
                error={errorText !== ''}
                helperText={errorText !== '' ? errorText : ''}
                variant="outlined"
                margin="normal"
                fullWidth
                id="itemid"
                name="item id"
              />
            </Grid>

            <Grid item xs={12} sm={4} md={4} lg={4}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                className={classes.submit}
                fullWidth
              >
                Show statistics
              </Button>
            </Grid>

            <Grid item xs={12} sm={4} md={4} lg={4}>
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
      </React.Fragment>
    )
  }

  return (
    <React.Fragment>
      <div className={classes.inputHeaderDiv}>
        {header('Input item id')}
      </div>

      <div className="RemovalForm">
        {idForm()}
      </div>
    </React.Fragment>
  )
}

export default ItemForm
