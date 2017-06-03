import React from 'react';
import PropTypes from 'prop-types';
import { Redirect } from 'react-router-dom';
import headerImage from 'images/header.png';
import { withStyles, createStyleSheet } from 'material-ui/styles';
import LoginCard from 'containers/login/LoginCard';

const styleSheet = createStyleSheet('LoginPage', theme => ({
  '@global': {
    body: {
      height: '100%',
      width: '100%',
      backgroundColor: theme.palette.background.contentFrame,
      fontFamily: 'Roboto',
    },
    a: {
      textDecoration: 'none',
    },
  },
  logo: {
    background: `transparent url(${headerImage}) no-repeat center`,
    minHeight: 90,
  },
}));

const LoginPage = ({ classes, redirectToReferrer, location }) => {
  const { from } = location.state || { from: { pathname: '/' } };

  if (redirectToReferrer) {
    return (
      <Redirect to={from} />
    );
  }

  return (
    <div>
      <div className={classes.logo} />
      <LoginCard />
    </div>
  );
};

LoginPage.propTypes = {
  classes: PropTypes.object.isRequired,
  location: PropTypes.object.isRequired,
  redirectToReferrer: PropTypes.bool.isRequired,
};

export default withStyles(styleSheet)(LoginPage);