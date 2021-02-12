import React from 'react'
import { useDispatch } from 'react-redux'

import { makeStyles } from '@material-ui/core/styles'
import Button from '@material-ui/core/Button'
import Box from '@material-ui/core/Box'
import Card from '@material-ui/core/Card'
import CardActionArea from '@material-ui/core/CardActionArea'
import CardContent from '@material-ui/core/CardContent'
import CardHeader from '@material-ui/core/CardHeader'
import Grid from '@material-ui/core/Grid'

import Rating from '@material-ui/lab/Rating'
import Typography from '@material-ui/core/Typography'

import RobotIcon from '../icons/robot01'
import ThumbUp from '@material-ui/icons/ThumbUp'
import ThumbDown from '@material-ui/icons/ThumbDown'
import ThumbsUpDown from '@material-ui/icons/ThumbsUpDown'

import { resetItem } from '../reducers/itemReducer'

const useStyles = makeStyles({
  recommendationDiv: {
    textAlign: 'center',
    paddingBottom: '3em'
  },
  robotFont: {
    fontFamily: 'PixelOperator'
  },
  thumbUp: {
    fill: 'green'
  },
  thumbDown: {
    fill: 'red'
  },
  twoThumbs: {
    fill: 'blue'
  }
})

const RecommendationCard = ({ stats }) => {
  const dispatch = useDispatch()
  const classes = useStyles()

  const calculateStatsFeatures = (stats) => {
    let numFeatures = 0

    if(stats.author) {
      numFeatures += 1
    }
    if(stats.series) {
      numFeatures += 1
    }
    if(stats.publisher) {
      numFeatures += 1
    }
    if(stats.genres) {
      numFeatures += stats.genres.length
    }
    if(stats.subjects) {
      numFeatures += stats.subjects.length
    }

    return numFeatures
  }

  const getRobotRating = (type, stars) => {
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

  const getMlThumb = (value) =>  {
    return(
      <Box component="fieldset" mb={3} borderColor="transparent">
        <Typography component="legend">{'ML prediction'.toUpperCase()}</Typography>
        <div id={'MLpredictionRatingDiv'} style={{ textAlign: 'center' }}>
          {value === 1 && <ThumbUp className={classes.thumbUp} /> }
          {value === 0 && <ThumbsUpDown className={classes.thumbDown}/>}
          {value === -1 && <ThumbDown className={classes.twoThumbs}/>}
        </div>
      </Box>
    )
  }

  const getRobotRecommendationString = (stats) => {
    const score = stats.recommendation_score

    if(calculateStatsFeatures(stats) < 5) {
      return (
        <Typography variant='h4' className={classes.robotFont}>
          So few features are available that I&apos;m unable to make recommendation.
        </Typography>
      )
    }

    if(score >= 3) {
      return (
        <Typography variant='h4' className={classes.robotFont}>
          I recommend this purchase. Many of your users will surely enjoy it.
        </Typography>
      )
    } else if(score > 1) {
      return(
        <Typography variant='h4' className={classes.robotFont}>
          I recommend this purchase. Some of your users will probably enjoy it.
        </Typography>
      )
    } else if(score === 0 || score === 1) {
      return (
        <Typography variant='h4' className={classes.robotFont}>
          I recommend to consider this purchase thoroughly. My robot brains can&apos;t decide on this.
        </Typography>
      )
    } else if(score > -3) {
      return (
        <Typography variant='h4' className={classes.robotFont}>
          I don&apos;t recommend this purchase. I think users would not necessarily be interested in it.
        </Typography>
      )
    } else {
      return (
        <Typography variant='h4' className={classes.robotFont}>
          I don&apos;t recommend this purchase at all. I think it will just gather dust and take up shelf space.
        </Typography>
      )
    }
  }


  const getRecommendation = () => {
    return (
      <React.Fragment>
        <Grid container alignContent='center' justify='center'>

          <Grid item md={12} xs={12} className={classes.recommendationDiv}>
            {getRobotRecommendationString(stats)}
          </Grid>

          {stats.author && getRobotRating('author', stats.author.score.stars)}
          {stats.series && getRobotRating('series', stats.series.score.stars)}
          {stats.publisher && getRobotRating('publisher', stats.publisher.score.stars)}
          {stats.genres && getRobotRating('genres', stats.genres.score.stars)}
          {stats.subjects && getRobotRating('subjects', stats.subjects.score.stars)}
          {stats.ml && getMlThumb(stats.ml.prediction)}
          {!stats.ml && getRobotRating('ML prediction', null)}

        </Grid>
      </React.Fragment>
    )
  }

  return (
    <Card>

      <CardHeader avatar={ <RobotIcon width='128px' height='128px' /> }
        title="HA-1-APU"
        subheader="Selection process assistant"
      />

      <CardContent>
        {getRecommendation()}
      </CardContent>

      <CardActionArea onClick={() => dispatch(resetItem())}>
        <Button component='span'>
          Back to form
        </Button>
      </CardActionArea>

    </Card>
  )
}

export default RecommendationCard