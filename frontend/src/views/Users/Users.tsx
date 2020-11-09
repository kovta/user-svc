import { Theme } from '@material-ui/core';
import { makeStyles } from '@material-ui/styles';
import React from 'react';
import { UserList, UserToolbar } from './components';

const Users = () => {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <UserToolbar />
      <div className={classes.content}>
        <UserList />
      </div>
    </div>
  );
};

export default Users;

const useStyles = makeStyles((theme: Theme) => ({
  root: {
    padding: theme.spacing(3),
  },
  content: {
    marginTop: theme.spacing(2),
  },
}));
