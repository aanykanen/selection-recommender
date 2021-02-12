import React, { useEffect, useState } from 'react'
import { useSelector } from 'react-redux'

import { makeStyles } from '@material-ui/core/styles'
import Grid from '@material-ui/core/Grid'

import PacmanLoader from 'react-spinners/PacmanLoader'

import RecommendationCard from './RecommendationCard'
import BasicStatsCard from './BasicStatsCard'

import recommendationService from '../services/recommendation'
import { Typography } from '@material-ui/core'

const useStyles = makeStyles({
  loaderContainer: {
    minHeight: '100vh'
  },
  errorDisplay: {
    paddingTop: '10vh'
  }
})

const RecommenderDashboard = () => {
  const classes = useStyles()
  const item = useSelector(state => state.item)

  const [stats, setStats] = useState(null)
  const [loadingStats, setLoadingStats] = useState(true)

  const fetchStats = async () => {
    try {
      const statistics = await recommendationService.getRecommendation(item, 'selection')
      setStats(statistics)
    } catch(err) {
      console.log('API did not respond')
    }
  }

  useEffect(() => {
    fetchStats().then(() => {
      setLoadingStats(false)
    })
    // eslint-disable-next-line
  }, [])

  if(loadingStats) {
    return (
      <React.Fragment>
        <Grid container spacing={0} alignItems="center" justify="center" className={classes.loaderContainer}>
          <PacmanLoader />
        </Grid>
      </React.Fragment>
    )
  } else {
    if(stats !== null) {
      return (
        <React.Fragment>
          <Grid container justify='center' spacing={3} alignItems='stretch'>
            <Grid item md={12} xs={12} >
              <RecommendationCard stats={stats} />
            </Grid>

            {stats.author &&
          <Grid item md={4} xs={12} >
            <BasicStatsCard statistics={stats.author} type={'author'}/>
          </Grid>
            }

            {stats.series &&
          <Grid item md={4} xs={12} >
            <BasicStatsCard statistics={stats.series} type={'serie'}/>
          </Grid>
            }

            {stats.publisher &&
          <Grid item md={4} xs={12}>
            <BasicStatsCard statistics={stats.publisher} type={'publisher'}/>
          </Grid>
            }

            {stats.genres && stats.genres.items.map((g, i) => {
              return (
                <Grid key={i} item md={4} xs={12}>
                  <BasicStatsCard statistics={g} type={'genre'}/>
                </Grid>
              )
            })}

            {stats.subjects && stats.subjects.items.map((s, i) => {
              return (
                <Grid key={i} item md={4} xs={12}>
                  <BasicStatsCard statistics={s} type={'subject'}/>
                </Grid>
              )
            })}
          </Grid>
        </React.Fragment>
      )
    } else {
      return (
        <React.Fragment>
          <Grid container justify='center' alignItems='stretch'>
            <Typography className={classes.errorDisplay}>
              There was a <b>major</b> error with the application. Contact the system administrator.
            </Typography>
          </Grid>
        </React.Fragment>
      )
    }
  }
}

export default RecommenderDashboard