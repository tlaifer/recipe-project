import React, {Component} from "react";
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Link from '@material-ui/core/Link';
import FavoriteIcon from '@material-ui/icons/Favorite';

import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import axios from 'axios'


const submitButtonText = 'Search'

/**
 * All possible ingredient options
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

/**
 * This is the array of recipes that meet the user's results.
 * Comes from call to search API.
 */
let recipes = [
  {
    id: '1',
    name: 'recipe name',
    ingredients: ['a', 'list', 'of', 'things'],
    techniques: ['a', 'list', 'of', 'things'],
    rating: 4.7,
    cookTime: 35,
    ingredientCount: 5,
    extraCount: 2,
    techniqueCount: 1
  }
];
class Search extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedIngredients: '',
      searchResults: '',
      display: this.props.display,
    }
  };

  handleSearch = () => {
    this.makeApiCall(this.state.selectedIngredients); /** removed var results =  */
    /** this.setState({ searchResults: results}); */
    this.setState({ display: 'results' });
  }

  handleIngredientChange = (event, value, reason) => {
    this.setState({ selectedIngredients: value });
  };

  handleBack = () => {
    this.setState({ display: 'search' })
  }

  /** searchInput parameter is the collection of ingredients entered by the user */
  makeApiCall = (searchInput) => {
    axios.post('http://localhost:5000/api/oneRecipe/', { /** TODO replace oneRecipe with search */
      userId: 1, 
      ingredientInput: searchInput
    }, {
      headers: {
          'Content-Type': 'application/json'
      }
    }).then((response) => {
      console.log("SUCCESS", response);
      this.setState({ searchResults: response.data.recipeArray });
    }).catch(error => {
      console.log(error)
    });
    return;
  }

  saveFavorite = (recipeId) => {
    return;
    /**
     * TODO: call favorite API
     */
  }

  render() {
    if (this.state.display === 'search') {
      return (
        <div className = 'body'>
          <h1> Ready to search for your next meal? </h1>
          <div>
            <Autocomplete
              multiple
              id="tags-standard"
              style={{ alignContent: "left" }}
              options={ingredients.map(ingredient => ingredient.name)}
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
          <Button variant="contained" color="primary" onClick={this.handleBack}>New Search</Button>
          <TableContainer component={Paper}>
            <Table className="table" aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell>Recipe Name</TableCell>
                  <TableCell align="right">Ingredients</TableCell>
                  <TableCell align="right">Techniques</TableCell>
                  <TableCell align="right">Cooking Time</TableCell>
                  <TableCell align="right">Average Rating</TableCell>
                  <TableCell align="right">Add to Favorites</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {recipes.map((row) => ( /** TODO replace recipes with this.state.searchResults */
                  <TableRow key={row.id}>
                    <TableCell component="th" scope="row">
                      <Link href={"/recipes/" + row.id}>{row.name}</Link>
                    </TableCell>
                    <TableCell align="right">{row.ingredients.join(', ')}</TableCell>
                    <TableCell align="right">{row.techniques.join(', ')}</TableCell>
                    <TableCell align="right">{row.cookTime}</TableCell>
                    <TableCell align="right">{row.rating}</TableCell>
                    <TableCell align="center">
                      <Button onClick={this.saveFavorite(row.id)}>
                        <FavoriteIcon/>
                      </Button>
                    </TableCell>
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