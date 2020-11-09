import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  TextField,
  Theme,
  Typography,
} from '@material-ui/core';
import { makeStyles } from '@material-ui/styles';
import React, { Dispatch, useState } from 'react';
import { LoadingButton } from '../../../../../../components';
import UserPayload from '../../../../../../models/user/user.payload';
import { useMutation } from '../../../../../../services/web';

export interface CreateDialogProps {
  isOpen: boolean;
  handleClose: () => void;
  setStatus: Dispatch<React.SetStateAction<boolean | undefined>>;
}
const CreateDialog = (props: CreateDialogProps) => {
  const { isOpen, handleClose, setStatus } = props;
  const classes = useStyles();

  const [loading, setLoading] = useState(false);
  const [nameError, setNameError] = useState(false);

  const [name, setName] = useState<string>('');
  const [email, setEmail] = useState<string>('');

  const handleSave = async () => {
    if (isBlank(name)) {
      setNameError(true);
    } else {
      setLoading(true);
      const { ok } = await useMutation<UserPayload>({
        path: 'users',
        payload: {
          name: name,
          email: email,
        },
        revalidate: ['users'],
      });
      setLoading(false);
      handleClose();
      setStatus(ok);
    }
  };
  const isBlank = (str: string | undefined) => !str || str.length === 0 || !str.trim();

  return (
    <Dialog fullWidth open={isOpen} onClose={handleClose}>
      <DialogTitle>
        <Typography variant="subtitle1">New User</Typography>
      </DialogTitle>
      <DialogContent>
        <form className={classes.form} noValidate>
          <FormControl fullWidth variant="filled">
            <TextField
              required
              fullWidth
              error={nameError}
              helperText={name && 'Non blank name is required'}
              value={name}
              onChange={(event) => {
                const value = event.target.value;
                setName(value);
                !isBlank(value) && setNameError(false);
              }}
              className={classes.commentField}
              label="Name"
              variant="filled"
            />
            <TextField
              fullWidth
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              className={classes.commentField}
              label="Email"
              variant="filled"
            />
          </FormControl>
        </form>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} color="inherit" disabled={loading}>
          Cancel
        </Button>
        <LoadingButton label="Save" loading={loading} onClick={handleSave} />
      </DialogActions>
    </Dialog>
  );
};

export default CreateDialog;

const useStyles = makeStyles((theme: Theme) => ({
  tabs: {
    borderBottom: `1px solid ${theme.palette.divider}`,
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    margin: 'auto',
    width: '100%',
  },
  commentField: {
    marginTop: theme.spacing(1),
  },
}));
