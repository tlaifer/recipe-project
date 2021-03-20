import React, {Component} from "react";
import config from "./config.json";
import axios from 'axios'


class Search extends Component {
  state = {
    searchValue: '',
  };

  handleOnChange = event => {
    this.setState({ searchValue: event.target.value });
  };

  handleSearch = () => {
    this.makeApiCall(this.state.searchValue);
  }

  makeApiCall = searchInput => {
    var searchUrl = `${config.SERVER_URL}/api/user/${searchInput}`
    fetch(searchUrl).then(response => {
      return response.json()
    }).then(jsonData => {
      console.log(jsonData)
    })
  }

  render() {
    return (
      <div>
        <h1> Ready to search for your next meal? </h1>
        <input
          name='text'
          type='text'
          placeHolder='Search'
          onChange={event => this.handleOnChange(event)}
          value= {this.state.searchValue}
        />
        <button onClick={this.handleSearch}> Search </button>
      </div>
    )
  }
}

export default Search;