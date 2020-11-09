import {
  Card,
  CircularProgress,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Theme,
} from '@material-ui/core';
import { makeStyles } from '@material-ui/styles';
import React from 'react';
import User from '../../../../models/user/user.response';
import { useRequest } from '../../../../services/web';

const UserList = () => {
  const { data = [], isValidating } = useRequest<User[]>({ path: 'users' });
  const classes = useStyles();

  return (
    <Card>
      {isValidating ? (
        <div className={classes.centered}>
          <CircularProgress />
        </div>
      ) : (
        <TableContainer component={Paper}>
          <Table aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Id</TableCell>
                <TableCell align="right">Name</TableCell>
                <TableCell align="right">Email</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((user) => (
                <TableRow key={user.id}>
                  <TableCell component="th" scope="row">
                    {user.id}
                  </TableCell>
                  <TableCell align="right">{user.name}</TableCell>
                  <TableCell align="right">{user.email}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Card>
  );
};

export default UserList;

const useStyles = makeStyles((theme: Theme) => ({
  itemTitle: {
    paddingRight: '24px',
  },
  drawerPaper: {
    width: '250px',
    height: '100%',
    position: 'relative',
    overflow: 'scroll',
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  centered: {
    margin: 0,
    position: 'absolute',
    top: '50%',
    left: '50%',
    marginRight: '-50%',
    transform: 'translate(-50%, -50%)',
  },
}));
