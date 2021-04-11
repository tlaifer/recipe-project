import './App.css';
import NavLayout from "./NavLayout";
import React, { useEffect, useState } from 'react';
import axios from 'axios';


function App(props, state) {
  const [getMessage, setGetMessage] = useState({})

  useEffect(()=>{
    axios.get('http://sp21-cs411-13.cs.illinois.edu:5000').then(response => {
      console.log("SUCCESS", response)
      setGetMessage(response)
    }).catch(error => {
      console.log(error)
    })

  }, [])
  return (
    <div className="App">
      <NavLayout/>
    </div>
  );
}

export default App;
