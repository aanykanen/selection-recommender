import React from 'react'
import { useDispatch } from 'react-redux'

import { makeStyles } from '@material-ui/core/styles'
import Button from '@material-ui/core/Button'
import Box from '@material-ui/core/Box'
import Card from '@material-ui/core/Card'
import CardActionArea from '@material-ui/core/CardActionArea'
import CardContent from '@material-ui/core/CardContent'
import Grid from '@material-ui/core/Grid'
import Rating from '@material-ui/lab/Rating'
import Typography from '@material-ui/core/Typography'

import { ResponsiveLine } from '@nivo/line'

import { resetItem } from '../reducers/itemReducer'

const useStyles = makeStyles({
  centerText: {
    textAlign: 'center'
  },
  infoCardDiv: {
    paddingTop: '3vh'
  },
  infoCardGrid: {
    textAlign: 'center',
    paddingBottom: '3em',
    paddingTop: '3em'
  },
  robotFont: {
    fontFamily: 'PixelOperator'
  },
  sequenceDiv: {
    height:'20em',
    paddingTop: '2em'
  }
})

const ItemCard = ({ stats, item }) => {
  const dispatch = useDispatch()
  const classes = useStyles()

  const getRating = (type, stars) => {
    return (
      <Box component="fieldset" mb={3} borderColor="transparent">
        <Typography component="legend">{type.toUpperCase()}</Typography>
        <div id={`${type}RatingDiv`}>
          {stars && <Rating name="read-only" value={stars} readOnly /> }
          {!stars && <Typography className={classes.robotFont}>[ NOT AVAILABLE ]</Typography>}
        </div>
      </Box>
    )
  }

  const getTrend = () => {
    const id = 'trend'
    const data = item.circulation_sequence.map((t, i) => { return { x: i, y: t }})
    return { id, data }
  }

  const getSequenceView = () => {
    return (
      <React.Fragment>
        <div className={classes.sequenceDiv}>
          <ResponsiveLine
            data={[getTrend()]}
            colors={{ 'scheme':'dark2' }}
            lineWidth={3}
            enablePoints={true}
            enableArea={true}
            yScale={{ type: 'linear' }}
            yFormat={value => Number(value)}
            margin={{ top: 50, right: 10, bottom: 50, left: 50 }}
            axisLeft={{
              orient: 'right',
              legend: 'Loans (renewals not included)',
              legendPosition: 'middle',
              legendOffset: -40,
              format: e => Math.floor(e) === e && e
            }}
            axisBottom={{
              'orient': 'bottom',
              'tickSize': 0,
              'tickPadding': 5,
              'tickRotation': 0,
              'format': () => null,
            }}
          />
        </div>
      </React.Fragment>
    )
  }

  const getInfoCard = () => {
    return (
      <React.Fragment>
        <Grid container alignContent='center' justify='center' className={classes.infoCardDiv}>
          <Typography variant='h4' className={classes.centerText}>
            {item.title ? item.title.toUpperCase() : 'UNKNOWN TITLE'} ({item.pub_year ? item.pub_year : 'n.d.'})
          </Typography>

          <Grid item md={12} xs={12} className={classes.infoCardGrid}>
            <Typography variant='body1'>
              Acquired: <b>{item.acquired}</b>
            </Typography>
            <Typography variant='body1'>
              Total circulation: <b>{item.circulation_sequence.reduce((a, b) => a + b, 0)}</b>
            </Typography>

            <Typography variant='body1'>
              Last borrowed: <b>{item.last_borrowed ? item.last_borrowed : '??'}</b>
            </Typography>

            {window.screen.width >= 768 && getSequenceView()}
          </Grid>
          {stats.author && getRating('author', stats.author.score.stars)}
          {stats.series && getRating('series', stats.series.score.stars)}
          {stats.publisher && getRating('publisher', stats.publisher.score.stars)}
          {stats.genres && getRating('genres', stats.genres.score.stars)}
          {stats.subjects && getRating('subjects', stats.subjects.score.stars)}
        </Grid>
      </React.Fragment>
    )
  }

  return (
    <Card>
      <CardContent>
        {getInfoCard()}
      </CardContent>
      <CardActionArea
        onClick={() => dispatch(resetItem())}>
        <Button component='span'>
          Back to form
        </Button>
      </CardActionArea>
    </Card>
  )
}

export default ItemCard