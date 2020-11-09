import { Button, CircularProgress, Theme } from '@material-ui/core';
import { orange } from '@material-ui/core/colors';
import { makeStyles } from '@material-ui/styles';
import React from 'react';

export interface LoadingButtonProps {
  label: string;
  loading: boolean;
  onClick: () => void;
}
const LoadingButton = (props: LoadingButtonProps) => {
  const { label, loading, onClick } = props;
  const classes = useStyles();

  return (
    <div className={classes.buttonWrapper}>
      <Button onClick={onClick} color="primary" variant="outlined" disabled={loading}>
        {label}
      </Button>
      {loading && <CircularProgress size={24} className={classes.buttonProgress} />}
    </div>
  );
};

export default LoadingButton;

const useStyles = makeStyles((theme: Theme) => ({
  buttonWrapper: {
    margin: theme.spacing(1),
    position: 'relative',
  },
  buttonProgress: {
    color: orange[500],
    position: 'absolute',
    top: '50%',
    left: '50%',
    marginTop: -12,
    marginLeft: -12,
  },
}));
