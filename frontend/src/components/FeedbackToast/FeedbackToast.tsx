import { Snackbar } from '@material-ui/core';
import { Alert } from '@material-ui/lab';
import React, { Dispatch, Fragment } from 'react';

export interface FeedbackToastProps {
  status: boolean | undefined;
  setStatus: Dispatch<React.SetStateAction<boolean | undefined>>;
  label: string;
  errorLabel: string;
}
const FeedbackToast = (props: FeedbackToastProps) => {
  const { status, setStatus, label, errorLabel } = props;

  return (
    <>
      {status !== undefined ? (
        <Snackbar
          open={status !== undefined}
          autoHideDuration={6000}
          anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
          onClose={() => setStatus(undefined)}
        >
          {status ? (
            <Alert severity="success" color="info" variant="outlined">
              {label}
            </Alert>
          ) : (
            <Alert severity="error" variant="outlined">
              {errorLabel}
            </Alert>
          )}
        </Snackbar>
      ) : (
        <Fragment />
      )}
    </>
  );
};

export default FeedbackToast;
