import React, { useState } from 'react'

import { makeStyles } from '@material-ui/core/styles'
import Card from '@material-ui/core/Card'
import CardContent from '@material-ui/core/CardContent'
import IconButton from '@material-ui/core/IconButton'
import Tooltip from '@material-ui/core/Tooltip'
import Typography from '@material-ui/core/Typography'

import NewReleasesIcon from '@material-ui/icons/NewReleases'
import SwapHoriz from '@material-ui/icons/SwapHoriz'

import { ResponsiveBar } from '@nivo/bar'
import { ResponsiveLine } from '@nivo/line'

const useStyles = makeStyles({
  card: {
    height: '100%'
  },
  heading: {
    marginTop: '20px'
  },
  newContentDiv: {
    textAlign: 'center',
    paddingTop: '2em'
  },
  newContentFont: {
    paddingTop: '1em'
  },
  newContentIcon: {
    width: '5em',
    height: '5em',
    color:'green'
  },
  title: {
    fontSize: 14,
  },
  tooltip: {
    float: 'right'
  },
  sequenceDiv: {
    height:'10em',
    paddingBottom: '4em'
  },
  sequenceFont: {
    paddingBottom: '1em',
    paddingTop: '1em'
  },
  statisticsHeader: {
    paddingTop: '1em'
  },
  statisticsBar: {
    height:'1.5em',
    display: 'flex',
    paddingBottom: '1em'
  }

})

const BasicStatsCard = ({ statistics, type }) => {
  const [statisticsView, setStatisticsView] = useState(true)
  const classes = useStyles()

  const switchViewIcon = () => {
    return(
      <React.Fragment>
        <Tooltip title='Switch view' className={classes.tooltip}>
          <IconButton aria-label='switch view' onClick={() => statisticsView ? setStatisticsView(false) : setStatisticsView(true)}>
            <SwapHoriz width='32px' height='32px' />
          </IconButton>
        </Tooltip>
      </React.Fragment>
    )
  }

  const getTrend = () => {
    const id = 'trend'
    const data = statistics.normalized_trend.map((t, i) => { return { x: i, y: t }})
    return { id, data }
  }

  const getStatisticsView = () => {
    // Fixes use of -1 as default symbol for deleted item for edge cases
    const shownCirculation = statistics.historical_circulation >= 0 ? statistics.historical_circulation : 0

    return (
      <React.Fragment>

        <Typography variant="body1" className={classes.statisticsHeader}>
            Number of items (available / deleted)
        </Typography>

        <div className={classes.statisticsBar}>
          <ResponsiveBar
            data={[{ id: 'itemcount', available: statistics.current_itemcount, deleted: statistics.historical_itemcount - statistics.current_itemcount }]}
            keys={['available', 'deleted']}
            indexBy='id'
            layout='horizontal'
            isInteractive={false}
            borderColor={'#000000'}
            borderWidth={1}
            borderRadius={1}
            colors={{ 'scheme':'dark2' }}
            labelTextColor={'#ffffff'}
          />
        </div>

        <Typography variant="body1">
            Historical circulation
        </Typography>

        <div className={classes.statisticsBar}>
          <ResponsiveBar
            data={[{ id: 'circulation', value: shownCirculation }]}
            keys={['value']}
            indexBy='id'
            layout='horizontal'
            isInteractive={false}
            borderColor={'#000000'}
            borderWidth={1}
            borderRadius={1}
            colors={{ 'scheme':'dark2' }}
            labelTextColor={'#ffffff'}
          />
        </div>

        <Typography variant="body1">
            Rank among {type}s
        </Typography>

        <div>
          <Typography variant="body2">
              Item count: {statistics.historical_itemcount_rank} / {statistics.total}
          </Typography>
          <Typography variant="body2">
              Circulation (total): {statistics.historical_circulation_rank} / {statistics.total}
          </Typography>
          <Typography variant="body2">
              Circulation (normalized): {statistics.historical_circulation_normalized_rank} / {statistics.total}
          </Typography>
        </div>

      </React.Fragment>
    )
  }

  const getSequenceView = () => {
    return (
      <React.Fragment>
        <div className={classes.sequenceDiv}>
          <Typography variant="body1" className={classes.sequenceFont}>
            Trend (past 12 months)
          </Typography>

          <ResponsiveLine
            data={[getTrend()]}
            colors={{ 'scheme':'dark2' }}
            lineWidth={3}
            enablePoints={true}
            enableArea={true}
            yScale={{ type: 'linear' }}
            yFormat={value => Number(value)}
            margin={{ top: 10, right: 0, bottom: 5, left: 50 }}
          />
        </div>
      </React.Fragment>
    )
  }

  const getNonNewContent = () => {
    return (
      <React.Fragment>
        { statisticsView && getStatisticsView() }
        { !statisticsView && getSequenceView() }
      </React.Fragment>
    )
  }

  const getNewContent = () => {
    return (
      <React.Fragment>
        <div className={classes.newContentDiv}>
          <NewReleasesIcon className={classes.newContentIcon} />
          <Typography className={classes.newContentFont}>
            NEW FEATURE!
          </Typography>
        </div>

      </React.Fragment>
    )
  }

  return (
    <Card className={classes.card}>
      <CardContent>
        <Typography className={classes.title} color="textSecondary" gutterBottom>
          {type.toUpperCase()} {!statistics.new && switchViewIcon()}
        </Typography>

        <Typography variant="h5" component="h2" className={classes.heading}>
          {statistics.heading.replace(/-/g, ' ').toUpperCase()}
        </Typography>
        {statistics.new && getNewContent()}
        {!statistics.new && getNonNewContent()}

      </CardContent>
    </Card>
  )
}

export default BasicStatsCard