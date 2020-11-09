import { Button, Theme } from '@material-ui/core';
import AddIcon from '@material-ui/icons/AddOutlined';
import { makeStyles } from '@material-ui/styles';
import React, { useState } from 'react';
import { FeedbackToast } from '../../../../components';
import UserCreateDialog from './components/UserCreateDialog';

const UserToolbar = () => {
  const classes = useStyles();
  const [open, setOpen] = useState(false);
  const [status, setStatus] = useState<boolean | undefined>();

  return (
    <div>
      <FeedbackToast
        status={status}
        setStatus={setStatus}
        label="User saved successfully!"
        errorLabel="Oops! Something went wrong."
      />
      <div className={classes.row}>
        <h1 className={classes.title}>Users</h1>
        <span className={classes.spacer} />
        <Button onClick={() => setOpen(true)} startIcon={<AddIcon />} color="primary" variant="outlined">
          New User
        </Button>
        <UserCreateDialog handleClose={() => setOpen(false)} isOpen={open} setStatus={setStatus} />
      </div>
    </div>
  );
};

export default UserToolbar;

const useStyles = makeStyles((theme: Theme) => ({
  title: {
    textTransform: 'capitalize',
  },
  row: {
    height: '42px',
    display: 'flex',
    alignItems: 'center',
    marginTop: theme.spacing(1),
  },
  spacer: {
    flexGrow: 1,
  },
  padder: {
    paddingRight: 10,
  },
  icon: {
    width: 24,
    height: 24,
    display: 'flex',
    alignItems: 'center',
    marginRight: theme.spacing(1),
    marginBottom: '3px',
  },
  feedLink: {
    paddingRight: '24px',
  },
  exportButton: {
    marginRight: theme.spacing(1),
  },
}));
