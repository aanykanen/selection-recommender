import React, { useEffect, useState } from 'react'
import { useSelector } from 'react-redux'

import { makeStyles } from '@material-ui/core/styles'
import Grid from '@material-ui/core/Grid'

import PacmanLoader from 'react-spinners/PacmanLoader'

import BasicStatsCard from './BasicStatsCard'
import ItemCard from './ItemCard'

import recommendationService from '../services/recommendation'


const useStyles = makeStyles({
  loaderContainer: {
    minHeight: '100vh'
  }
})

const ItemDashboard = () => {
  const classes = useStyles()
  const item = useSelector(state => state.item)

  const [stats, setStats] = useState(null)
  const [loadingStats, setLoadingStats] = useState(true)

  const fetchStats = async () => {
    const statistics = await recommendationService.getRecommendation(item, 'selection')
    setStats(statistics)
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
    return (
      <React.Fragment>
        <Grid container justify='center' spacing={3} alignItems='stretch'>
          <Grid item md={12} xs={12} >
            <ItemCard stats={stats} item={item} />
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
  }
}

export default ItemDashboard