import React from 'react'
import { Link } from 'react-router-dom'

import Button from '@material-ui/core/Button'
import Card from '@material-ui/core/Card'
import CardActions from '@material-ui/core/CardActions'
import CardHeader from '@material-ui/core/CardHeader'
import Grid from '@material-ui/core/Grid'
import Typography from '@material-ui/core/Typography'
import Container from '@material-ui/core/Container'
import { makeStyles } from '@material-ui/core/styles'

const useStyles = makeStyles(() => ({
  bottomContainer: {
    minHeight: '20vh'
  },
  cardHeader: {
    backgroundColor: '#eeeeee'
  },
  headerText: {
    textAlign: 'center',
    fontSize: '3vw'
  },
  topContainer: {
    marginTop: '10vh',
    marginBottom: '10vh'
  }
}))

const options = [
  {
    title: 'Recommender system',
    buttonText: 'Get recommendation',
    buttonVariant: 'contained',
    link: '/selection'
  },
  {
    title: 'Item viewer',
    buttonText: 'Show statistics',
    buttonVariant: 'contained',
    link: '/itemstat'
  }
]

const RecommenderTypeSelect = () => {
  const classes = useStyles()

  return (
    <React.Fragment>
      <Container maxWidth="lg" component="main">

        <Grid container alignItems="center" justify="center" className={classes.topContainer}>
          <Typography variant='h1' className={classes.headerText}>COLLECTION DEVELOPMENT HELPER</Typography>
        </Grid>

        <Grid container spacing={6} alignItems="center" justify="center" className={classes.bottomContainer}>
          {options.map((option) => (
            <Grid item key={option.title} xs={12} sm={6} md={6}>
              <Card>

                <CardHeader
                  title={option.title}
                  subheader={option.subheader}
                  titleTypographyProps={{ align: 'center' }}
                  subheaderTypographyProps={{ align: 'center' }}
                  className={classes.cardHeader}
                />

                <CardActions>
                  <Button
                    component={Link}
                    fullWidth
                    variant={option.buttonVariant}
                    to={option.link}
                    color="primary">
                    {option.buttonText}
                  </Button>
                </CardActions>

              </Card>
            </Grid>
          ))}
        </Grid>

      </Container>
    </React.Fragment>
  )
}

export default RecommenderTypeSelect
