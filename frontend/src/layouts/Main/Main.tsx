import { Theme, useMediaQuery } from '@material-ui/core';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import clsx from 'clsx';
import React, { ReactNode, useState } from 'react';
import { Footer } from './components';

interface LayoutProps {
  children: ReactNode;
}
const Main = ({ children }: LayoutProps) => {
  const classes = useStyles();
  const theme = useTheme();
  const [openSidebar, setOpenSidebar] = useState(false);

  const isDesktop = useMediaQuery(theme.breakpoints.up('lg'), {
    defaultMatches: true,
  });

  return (
    <div
      className={clsx({
        [classes.root]: true,
      })}
    >
      <main className={classes.content}>
        {children}
        <Footer />
      </main>
    </div>
  );
};

export default Main;

const useStyles = makeStyles((theme: Theme) => ({
  root: {
    height: '100%',
    marginLeft: theme.spacing(50),
    marginRight: theme.spacing(50),
  },
  shiftContent: {
    paddingLeft: 240,
  },
  content: {
    height: '100%',
  },
}));
