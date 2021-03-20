import logo from './logo.svg';
import './App.css';
import SideMenu from "./SideMenu";
import Search from "./Search";
import React, { useEffect, useState } from 'react';
import axios from 'axios'

function App(props, state) {
  const [getMessage, setGetMessage] = useState({})

  useEffect(()=>{
    axios.get('http://localhost:5000/').then(response => {
      console.log("SUCCESS", response)
      setGetMessage(response)
    }).catch(error => {
      console.log(error)
    })

  }, [])
  return (
    <div className="App">
      <SideMenu />
      <Search />
    </div>
  );
}

export default App;
