import { CircularProgress, makeStyles } from '@material-ui/core';
import clsx from 'clsx';
import React from 'react';

const CenteredSpinner = () => {
  const classes = useStyles();

  return (
    <div className={clsx(classes.centered, classes.centeredSpinner)}>
      <CircularProgress />
    </div>
  );
};

export default CenteredSpinner;

const useStyles = makeStyles((_) => ({
  centered: {
    margin: 0,
    position: 'absolute',
    top: '50%',
    left: '50%',
    marginRight: '-50%',
  },
  centeredSpinner: {
    transform: 'translate(250%, -50%)',
  },
}));
