import React, {Component} from "react";
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

import config from "../config.json";
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import axios from 'axios'


const submitButtonText = 'Search'

/**
 * TODO: replace with DB call to UserTechniques
 */
 let techniques = [
  {
    name: 'tec1',
    value: false
  },
  {
    name: 'tec2',
    value: false
  }
];

/**
 * TODO: replace with DB call to Ingredients & UserIngredients
 */
let ingredients = [
  {
    name: 'tomatoes',
    value: false
  },
  {
    name: 'bread',
    value: false
  }
]

let recipes = [
  {
    id: '1',
    ingredients: ['a', 'list', 'of', 'things'],
    techniques: ['a', 'list', 'of', 'things'],
    rating: 4.7,
    cookTime: 35
  }
];
function createData(name, calories, fat, carbs, protein) {
  return { name, calories, fat, carbs, protein };
}

let rows = [
  createData('Frozen yoghurt', 159, 6.0, 24, 4.0),
  createData('Ice cream sandwich', 237, 9.0, 37, 4.3),
  createData('Eclair', 262, 16.0, 24, 6.0),
  createData('Cupcake', 305, 3.7, 67, 4.3),
  createData('Gingerbread', 356, 16.0, 49, 3.9),
]

class Search extends Component {
  state = {
    selectedIngredients: '',
    display: 'search',
  };

  componentDidMount () {
    this.setState({ display: 'search' })
  }

  handleSearch = () => {
    var results = this.makeApiCall(this.state.searchValue);
    this.setState({ searchResults:  rows});
    this.setState({ display: 'results'});
  }

  handleIngredientChange = (event, value, reason) => {
    this.setState({ selectedIngredients: value });
  };

  makeApiCall = (searchInput) => {
    // var searchUrl = `${config.SERVER_URL}/api/user/${searchInput}`
    // fetch(searchUrl).then(response => {
    //   return response.json()
    // }).then(jsonData => {
    //   console.log(jsonData)
    // })
    return recipes;
  }

  render() {
    if (this.state.display == 'search') {
      return (
        <div className = 'body'>
          <h1> Ready to search for your next meal? </h1>
          <div>
            <Autocomplete
              multiple
              id="tags-standard"
              style={{ alignContent: "left" }}
              options={ingredients.map(ingredient => ingredient.name)}
              // defaultValue={[state.ingredients[0].name]}
              getOptionLabel={(option) => option}
              onChange={(event,value, reason) => this.handleIngredientChange(event, value, reason)}
              renderInput={(params) => (
                <TextField
                  {...params}
                  variant="standard"
                  placeholder="What do you want to cook with today?"
                />
              )}
            />
          </div>
          <div >
            <Button variant="contained" color="primary" onClick={this.handleSearch}>{submitButtonText}</Button>
          </div>
        </div>
      )
    } else {
      return (
        <div className = 'body'>
          <TableContainer component={Paper}>
            <Table className="table" aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell>Recipe Name</TableCell>
                  <TableCell align="right">Ingredients</TableCell>
                  <TableCell align="right">Techniques</TableCell>
                  <TableCell align="right">Cooking Time</TableCell>
                  <TableCell align="right">Average Rating</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {rows.map((row) => (
                  <TableRow key={row.name}>
                    <TableCell component="th" scope="row">
                      {row.name}
                    </TableCell>
                    <TableCell align="right">{row.calories}</TableCell>
                    <TableCell align="right">{row.fat}</TableCell>
                    <TableCell align="right">{row.carbs}</TableCell>
                    <TableCell align="right">{row.protein}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </div>
      )
    }
  }
}

export default Search;