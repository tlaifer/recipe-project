import './App.css';
import SideMenu from "./SideMenu";
import React, {Component, useEffect, useState } from 'react';

import routes from "./Router/routes";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";


class NavLayout extends Component {
  render() {
    return (
      <Router>
        <SideMenu items={routes} />
        <main>
          {routes.map((route, index) => (
            <Route
              key={index}
              path={route.path}
              exact={route.exact}
              component={route.main}
            />
          ))}
        </main>
      </Router>
    )
  }
}

export default NavLayout;
